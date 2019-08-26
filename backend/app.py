from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import json
from bson import json_util
import re
import urllib
import requests
import base64
import pandas as pd 
import numpy as np 
import unidecode
from datetime import datetime

RUN_LOCALLY = True

hostname = 'localhost' if RUN_LOCALLY else '3.86.203.151'

app = Flask(__name__)
CORS(app)
users = {}
artist_genres = {} #{artist_id:{"name":"bob smith","genres":["genre1","genre2","genre3"]}}
client_id = '81d7431ddf80433585d18cca9c08c815'
client_secret = '8292e805c93c4d0daed64d4856e88965'
scope = ' '.join([  'user-top-read',
                    'user-read-recently-played',
                    'user-read-playback-state',
                    'user-read-currently-playing',
                    'user-modify-playback-state',
                    'user-library-modify',
                    'user-library-read',
                    'streaming',
                    'app-remote-control',
                    'user-read-private',
                    'user-read-email',
                    'user-follow-modify',
                    'user-follow-read',
                    'playlist-modify-public',
                    'playlist-read-collaborative',
                    'playlist-read-private',
                    'playlist-modify-private'])
redirect_uri = 'http://' + hostname + ':3000/home'
login_url = 'https://accounts.spotify.com/authorize?' + urllib.urlencode({
                  'response_type': 'code',
                  'client_id': client_id,
                  'scope': scope,
                  'redirect_uri': redirect_uri
                })
token_url = 'https://accounts.spotify.com/api/token' 
auth_str = '{}:{}'.format(client_id,client_secret)
b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
token_headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": "Basic {}".format(b64_auth_str)}

create_playlist_url = 'https://api.spotify.com/v1/users/{}/playlists'
add_to_playlist_url = 'https://api.spotify.com/v1/playlists/{}/tracks'

audio_features = ["duration_ms",
  "key",
  "mode",
  "time_signature",
  "acousticness",
  "danceability",
  "energy",
  "instrumentalness",
  "liveness",
  "loudness",
  "speechiness",
  "valence",
  "tempo"]

@app.route('/login', methods=['GET','POST'])
def login():
    return redirect(login_url)

@app.route('/get_token', methods=['GET','POST'])
def get_token(): 
    data = json.loads(request.data)
    code = data['code']#'AQCe64RPWN8DBFB-XbvC9nLkSVSbh7x6zydsRIuDL0gdqIreFdxbx-b4jZgAjkU4WLDVWYSEBiOnJm4wtLtrj07vT9OMerWLwMILkXcpo6k_BcW8y_03HIsncRbeDff4GHh1fLoLyurl-W9P9WNUnADzvTgJz9eYDws7TbNI-AvppQ9zj93sVXaBM7eoMB9KGyq0sbs8ojuRJEuBOflMtyiFEeth7ebkDg-TEsBTCHDRFlLmBPIklpnug1-fo2gWUgxBBa_f'
    params = {
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":redirect_uri#,
            # 'client_id':client_id,
            # 'client_secret':client_secret 
    }
    res = requests.post(token_url, params=params, headers=token_headers)
    return jsonify(res.json())

@app.route('/compile_recently_played',methods=['GET','POST'])
def compile_recently_played():
    data = json.loads(request.data)
    print(data)
    read_from_temp_csv = False
    if read_from_temp_csv:
        #TODO: this
        print('hi')
        #users[data['uid']] = {"recently_played":pd.read_csv('charlie_liked_songs_verbose.csv')}
    elif data['uid'] not in users.keys() or "recently_played" not in users[data['uid']].keys():
        df = pd.DataFrame()
        recently_played_url = '	https://api.spotify.com/v1/me/player/recently-played?' + urllib.urlencode(
                {
                    "limit":50
                })
        print(recently_played_url)
        response = requests.get(recently_played_url, headers={"Authorization":"Bearer " + data['access_token'],
                                                    "Content-Type":"application/json"}).json()
        def replace(string):
            return unidecode.unidecode(string)
        song_counter = 0
        while True:
            print(response)
            if not response["items"]:
                print('no items in response')
                break
            for song in response['items']:
                entry = {
                    "name":song["track"]["name"],
                    "id":song["track"]["id"],
                    "artists":', '.join([artist["name"] for artist in song["track"]["artists"]]),
                    "artist_ids":', '.join([artist["id"] for artist in song["track"]["artists"]]),
                    #"added_at":song["added_at"], #this doesnt exist or mean anything in play history
                    "release_date":song["track"]["album"]["release_date"]
                }
                for key in entry.keys():
                    entry[key] = replace(entry[key])
                df = df.append(entry, ignore_index=True)
                song_counter = song_counter + 1
                ARBITRARY_TESTING_LIMIT = 1000
                if song_counter > ARBITRARY_TESTING_LIMIT:
                    break
            if response["next"] is None:
                print('response has no next field')
                break
            response = requests.get(response['next'], headers={"Authorization":"Bearer " + data['access_token'],
                                                               "Content-Type":"application/json"}).json()
        print(df.to_string())
        df.to_csv('charlie_recently_played_songs.csv')

        #TODO: this
        advanced_params = False
        if advanced_params:

            def get_advanced_params(row):
                #print(row)
                response = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(row['id']),headers={"Authorization":"Bearer " + data['access_token'],
                                                               "Content-Type":"application/json"}).json()
                for feature in audio_features:
                    row[feature] = response[feature]
                
                return row

            df = df.apply(get_advanced_params,axis=1)
            df.to_csv('charlie_liked_songs_verbose.csv')

        if data['uid'] not in users.keys():
            print('this should never happen but it happened; liked songs should always be compiled first')
            users[data['uid']] = {"recently_played_songs":df}
        users[data['uid']]['recently_played'] = df
    print(users.keys(),'users.keys')
    return {'hello':'world'}

@app.route('/compile_liked_songs',methods=['GET','POST'])
def compile_liked_songs():
    data = json.loads(request.data)
    print(data)
    read_from_temp_csv = True
    if read_from_temp_csv:
        users[data['uid']] = {"liked_songs":pd.read_csv('charlie_liked_songs_verbose.csv')}
    elif data['uid'] not in users.keys():
        df = pd.DataFrame()
        songs_url = 'https://api.spotify.com/v1/me/tracks?' + urllib.urlencode(
                {
                    "limit":50
                })
        print(songs_url)
        response = requests.get(songs_url, headers={"Authorization":"Bearer " + data['access_token'],
                                                    "Content-Type":"application/json"}).json()
        def replace(string):
            return unidecode.unidecode(string)
        song_counter = 0
        while True:
            if not response["items"]:
                break
            for song in response['items']:
                entry = {
                    "name":song["track"]["name"],
                    "id":song["track"]["id"],
                    "artists":', '.join([artist["name"] for artist in song["track"]["artists"]]),
                    "artist_ids":', '.join([artist["id"] for artist in song["track"]["artists"]]),
                    "added_at":song["added_at"],
                    "release_date":song["track"]["album"]["release_date"]
                }
                for key in entry.keys():
                    entry[key] = replace(entry[key])
                df = df.append(entry, ignore_index=True)
                song_counter = song_counter + 1
                ARBITRARY_TESTING_LIMIT = 10000
                if song_counter > ARBITRARY_TESTING_LIMIT:
                    break
            if response["next"] is None:
                break
            response = requests.get(response['next'], headers={"Authorization":"Bearer " + data['access_token'],
                                                               "Content-Type":"application/json"}).json()
        print(df.to_string())
        df.to_csv('charlie_liked_songs.csv')

        advanced_params = True
        if advanced_params:

            def get_advanced_params(row):
                #print(row)
                feature_response = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(row['id']),headers={"Authorization":"Bearer " + data['access_token'],
                                                               "Content-Type":"application/json"}).json()
                for feature in audio_features:
                    row[feature] = feature_response[feature]
                
                row_genres = []
                for artist_id in row['artist_ids'].split(", "):
                    #update running list of artists' genres
                    if artist_id not in artist_genres.keys():
                        artist_response = requests.get('https://api.spotify.com/v1/artists/{}'.format(artist_id),headers={"Authorization":"Bearer " + data['access_token'],
                                                               "Content-Type":"application/json"}).json()
                        artist_genres[artist_id] = {"name":artist_response["name"],
                                                    "genres":artist_response["genres"]}
                    
                    row_genres += artist_genres[artist_id]["genres"]
                row["genres"] = ', '.join(row_genres)

                return row

            df = df.apply(get_advanced_params,axis=1)
            df = df.fillna("none")
            df.to_csv('charlie_liked_songs_verbose.csv')

        users[data['uid']] = {"liked_songs":df}
    print(users.keys(),'users.keys')
    return {'hello':'world'}

@app.route('/create_playlist',methods=['GET','POST'])
def create_playlist():
    data = json.loads(request.data)
    df = users[data['uid']]["liked_songs"]
    artists = data['params']['artists'].split(', ')
    subset = df
    subset = subset[subset['artists'].str.contains('|'.join(artists))]
    
    genres = data['params']['genres'].split(', ')
    subset = subset[subset['genres'].str.contains('|'.join(genres))]
    
    def normalize_date(date):
        if len(date) < 10:
            date = date + '-01-01'
        return datetime.strptime(date,'%Y-%m-%d')
    if 'release_date' in data['params']['ranged']:
        subset['release_date_as_datetime'] = subset['release_date'].apply(normalize_date)
        subset = subset[(subset['release_date_as_datetime'] < data['params']['ranged']['release_date']['upper']) & (subset['release_date_as_datetime'] > data['params']['ranged']['release_date']['lower'])]
    if 'liked_date' in data['params']['ranged']:
        subset['added_at_as_datetime'] = subset['added_at'].apply(lambda date: normalize_date(date[:10]))
        subset = subset[(subset['added_at_as_datetime'] < data['params']['ranged']['liked_date']['upper']) & (subset['added_at_as_datetime'] > data['params']['ranged']['liked_date']['lower'])]
    for param in data['params']['ranged'].keys():
        if param in ['release_date','liked_date']:
            continue
        subset = subset[(subset[param] < float(data['params']['ranged'][param]['upper'])) & (subset[param] > float(data['params']['ranged'][param]['lower']))]
    
    ids = subset['id'].values
    print(data)

    #TODO: create playlist in increments, not just first 100
    if len(ids) > 100:
        ids = ids[:100]

    #response from create_playlist_url
    response = requests.post(create_playlist_url.format(data['uid']),
                            headers={"Authorization":"Bearer " + data['access_token'],
                                     "Content-Type":"application/json"},
                            json={"name":"API: Artists: {}. Genres: {}.".format(data['params']['artists'], data['params']['genres'])}).json()
    #print(response)

    #response from add_to_playlist_url
    response = requests.post(add_to_playlist_url.format(response['id']),
                             headers={"Authorization":"Bearer " + data['access_token'],
                                     "Content-Type":"application/json"},
                            json={"uris":["spotify:track:{}".format(id_) for id_ in ids]}).json()

    print(response)
    return jsonify(response)

# @app.route('/analyze', methods=['GET','POST'])
# def analyze():
#     data = json.loads(request.data)
#     df = users[data['uid']]['liked_songs']
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
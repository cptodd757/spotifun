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

app = Flask(__name__)
CORS(app)
users = {}
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
redirect_uri = 'http://localhost:3000/home'
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

@app.route('/compile_liked_songs',methods=['GET','POST'])
def compile_liked_songs():
    data = json.loads(request.data)
    print(data)
    read_from_temp_csv =False
    if read_from_temp_csv:
        users[data['uid']] = pd.read_csv('charlie_liked_songs_verbose.csv')
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
                response = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(row['id']),headers={"Authorization":"Bearer " + data['access_token'],
                                                               "Content-Type":"application/json"}).json()
                for feature in audio_features:
                    row[feature] = response[feature]
                
                return row

            df = df.apply(get_advanced_params,axis=1)
            df.to_csv('charlie_liked_songs_verbose.csv')

        users[data['uid']] = df
    print(users.keys(),'users.keys')
    return {'hello':'world'}

@app.route('/create_playlist',methods=['GET','POST'])
def create_playlist():
    data = json.loads(request.data)
    df = users[data['uid']]
    artists = data['params']['artists'].split(', ')
    subset = df
    subset = subset[subset['artists'].str.contains('|'.join(artists))]
    
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

    response = requests.post(create_playlist_url.format(data['uid']),
                            headers={"Authorization":"Bearer " + data['access_token'],
                                     "Content-Type":"application/json"},
                            json={"name":"API: {}".format(data['params']['artists'])}).json()
    #print(response)

    response = requests.post(add_to_playlist_url.format(response['id']),
                             headers={"Authorization":"Bearer " + data['access_token'],
                                     "Content-Type":"application/json"},
                            json={"uris":["spotify:track:{}".format(id_) for id_ in ids]}).json()

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=359)
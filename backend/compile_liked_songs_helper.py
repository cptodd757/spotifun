import urllib
import pandas as pd
import requests
import unidecode

import config

def compile_liked_songs_helper(data):  
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

    
    if config.advanced_params:

        def get_advanced_params(row):
            #print(row)
            feature_response = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(row['id']),headers={"Authorization":"Bearer " + data['access_token'],
                                                            "Content-Type":"application/json"}).json()
            for feature in config.audio_features:
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

    return df
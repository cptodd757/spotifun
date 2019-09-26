import datetime
import pandas as pd
import requests

import config

def create_playlist_helper(data, df):
    artists = data['params']['artists'].split(', ')
    subset = df
    subset = subset[subset['artists'].str.contains('|'.join(artists))]
    
    genres = data['params']['genres'].split(', ')
    subset = subset[subset['genres'].str.contains('|'.join(genres))]
    
    def normalize_date(date):
        if len(date) < 8: #aka, it aint a full date
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
    response = requests.post(config.create_playlist_url.format(data['uid']),
                            headers={"Authorization":"Bearer " + data['access_token'],
                                     "Content-Type":"application/json"},
                            json={"name":"API: Artists: {}. Genres: {}.".format(data['params']['artists'], data['params']['genres'])}).json()
    #print(response)

    #response from add_to_playlist_url
    response = requests.post(config.add_to_playlist_url.format(response['id']),
                             headers={"Authorization":"Bearer " + data['access_token'],
                                     "Content-Type":"application/json"},
                            json={"uris":["spotify:track:{}".format(id_) for id_ in ids]}).json()

    return response
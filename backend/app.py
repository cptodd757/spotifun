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

import config
from get_token_helper import get_token_helper
from compile_liked_songs_helper import compile_liked_songs_helper
from create_playlist_helper import create_playlist_helper
from analyze_helper import analyze_helper

#BEFORE RUNNING: Ensure RUN_LOCALLY is set to the appropriate state in config.py


#RUN_LOCALLY = True
app = Flask(__name__)
CORS(app)
users = {}
artist_genres = {} #{artist_id:{"name":"bob smith","genres":["genre1","genre2","genre3"]}}

hostname = config.hostname
client_id = config.client_id
client_secret = config.client_secret
scope = config.scope
redirect_uri = config.redirect_uri
login_url = config.login_url
token_url = config.token_url 
auth_str = config.auth_str
b64_auth_str = config.b64_auth_str
token_headers = config.token_headers
create_playlist_url = config.create_playlist_url
add_to_playlist_url = config.add_to_playlist_url
audio_features = config.audio_features

#Prompt the user to login to Spotify.
@app.route('/login', methods=['GET','POST'])
def login():
    return redirect(login_url)

#With the authorization code granted by user's login to Spotify, obtain an API Key.
@app.route('/get_token', methods=['GET','POST'])
def get_token(): 
    return jsonify(get_token_helper(request))

#Compile a DataFrame of a given user's liked songs.
@app.route('/compile_liked_songs',methods=['GET','POST'])
def compile_liked_songs():
    data = json.loads(request.data)
    
    if config.read_from_temp_csv:
        users[data['uid']] = {"liked_songs":pd.read_csv('charlie_liked_songs_verbose.csv')}
    elif data['uid'] not in users.keys():
        df = compile_liked_songs_helper(data)
        users[data['uid']] = {"liked_songs":df}
    #print(users.keys(),'users.keys')
    return {'hello':'world'}

#Create a playlist from user's liked songs, based on additional specified parameters.
@app.route('/create_playlist',methods=['GET','POST'])
def create_playlist():
    data = json.loads(request.data)
    df = users[data['uid']]["liked_songs"]
    response = create_playlist_helper(data, df)
    print(response)
    return jsonify(response)

#A work in progress.  Basic analysis of user's liked songs.
@app.route('/analyze', methods=['GET','POST'])
def analyze():
    data = json.loads(request.data)
    df = users[data['uid']]['liked_songs']

    analyze_helper(data, df)
    return 'analyze response'

#NOT USED. Recently played song data not expansive enough for practical use.
@app.route('/compile_recently_played',methods=['GET','POST'])
def compile_recently_played():
    return {'hello':'world'}
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
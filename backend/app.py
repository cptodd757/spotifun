from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import json
from bson import json_util
import re
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
import urllib

import requests

import base64



app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['GET','POST'])
def login():
    #return jsonify({"key":"Hello World!"})
    client_id = '81d7431ddf80433585d18cca9c08c815'
    scope = 'user-read-private user-read-email user-top-read'
    redirect_uri = 'http://localhost:3000/home'
    url = 'https://accounts.spotify.com/authorize?' + urllib.urlencode({
                  'response_type': 'code',
                  'client_id': client_id,
                  'scope': scope,
                  'redirect_uri': redirect_uri
                })
    print(url)
    return redirect(url)

@app.route('/get_token', methods=['GET','POST'])
def get_token(): 
    print(request.data)
    data = json.loads(request.data)
    code = data['code']#'AQCe64RPWN8DBFB-XbvC9nLkSVSbh7x6zydsRIuDL0gdqIreFdxbx-b4jZgAjkU4WLDVWYSEBiOnJm4wtLtrj07vT9OMerWLwMILkXcpo6k_BcW8y_03HIsncRbeDff4GHh1fLoLyurl-W9P9WNUnADzvTgJz9eYDws7TbNI-AvppQ9zj93sVXaBM7eoMB9KGyq0sbs8ojuRJEuBOflMtyiFEeth7ebkDg-TEsBTCHDRFlLmBPIklpnug1-fo2gWUgxBBa_f'
    redirect_uri = 'http://localhost:3000/home'
    client_id = '81d7431ddf80433585d18cca9c08c815'
    client_secret = '8292e805c93c4d0daed64d4856e88965'
    url = 'https://accounts.spotify.com/api/token' 
    params =    {
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":redirect_uri#,
            # 'client_id':client_id,
            # 'client_secret':client_secret 
        }

    auth_str = '{}:{}'.format(client_id,client_secret)
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": "Basic {}".format(b64_auth_str)}
    print(headers)
    print(params)
    
    res = requests.post(url, params=params, headers=headers)
    print(res.content)
    return jsonify(res.json())

@app.route('/compile_liked_songs',methods=['GET','POST'])
def compile_liked_songs():
    data = json.loads(request.data)
    print(data)
    return {'key':'value'}

@app.route('/create_playlist',methods=['GET','POST'])
def create_playlist():
    data = json.loads(request.data)
    print(data)
    return {'key':'value'}

if __name__ == '__main__':
    app.run(port=359)
import urllib
import base64

RUN_LOCALLY = True
read_from_temp_csv = True
advanced_params = True

hostname = 'localhost' if RUN_LOCALLY else '3.86.203.151'
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
import config
import json
import requests

def get_token_helper(request):
    data = json.loads(request.data)
    code = data['code']
    params = {
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":config.redirect_uri
    }
    res = requests.post(config.token_url, params=params, headers=config.token_headers)
    return res.json()
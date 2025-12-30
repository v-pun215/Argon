import base64
import json
import urllib.request
import requests as re
import wget

key = "msk_vbErfWTw_ASPIcgIAAoN5y8c8et5COZZICh_xgPxKxcwP8oehV8HnOG5jRggWheEnLWlPVMk0"
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
def get_skin_texture_hash(username, skinPath):
    with open(skinPath, 'rb') as file:
        response = re.post(
            url='https://api.mineskin.org/generate/upload',
            data={"name": username, "visibility": 0},
            files={"file": (skinPath, file, 'text/x-spam')},
            headers={"User-Agent": useragent,"Authorization": "Bearer " + key}
        )

        encoded_value =response.json()['data']['texture']['value']
    
    decoded_json = json.loads(base64.b64decode(encoded_value).decode("utf-8"))
    skin_url = decoded_json["textures"]["SKIN"]["url"]
    texture_hash = skin_url.split("/")[-1]
    return texture_hash

def render_head(username, skinPath):
    texture_hash = get_skin_texture_hash(username, skinPath)
    nickac_url = f"https://nmsr.nickac.dev/head/{texture_hash}"
    wget.download(nickac_url, out=f"img/user/ely-{username}.png")

def render_body(username, skinPath):
    texture_hash = get_skin_texture_hash(username, skinPath)
    nickac_url = f"https://nmsr.nickac.dev/fullbody/{texture_hash}"
    wget.download(nickac_url, out=f"img/user/ely-{username}-skin.png")
import os
import json
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "X-Real-IP": "211.161.244.70"}

def get_music_u():
    music_u = os.environ.get("MUSIC_U", None)
    assert music_u is not None, "Set MUSIC_U in environment variables first!"
    return music_u

def handler(event, context):
    try:
        music_u = get_music_u()
    except AssertionError as e:
        print(str(e))
        return str(e)
    
    s = requests.Session()
    s.cookies.set("MUSIC_U", music_u, domain=".music.163.com")
    print(f"MUSIC_U: {music_u[0:20]}")
    r = s.get("https://music.163.com/discover/toplist", headers=headers)
    html = BeautifulSoup(r.text, "html.parser")
    songs = json.loads(html.find(id="song-list-pre-data").text)
    try:
        assert len(songs), "Failed to obtain toplist!"
    except AssertionError as e:
        print(str(e))
        return str(e)
    
    r = s.post("https://music.163.com/weapi/login/token/refresh")
    print("res status code: " + str(r.status_code))
    return r.status_code

if __name__ == "__main__":
    handler()
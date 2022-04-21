#데이터 베이스 생성

import os
DB_FILEPATH = os.path.join(os.path.dirname(__file__), 'kwangya.db')
import sqlite3
conn = sqlite3.connect(DB_FILEPATH)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS kwangya")
cursor.execute("""CREATE TABLE kwangya(
id INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
track VARCHAR(100),
artist VARCHAR(20),
acousticness REAL,
danceability REAL,
energy REAL,
instrumentalness REAL,
key INTEGER,
liveness REAL,
loudness REAL,
mode INTEGER,
speechiness REAL,
tempo REAL,
valence REAL)""")

#토큰 발급 
import requests
import base64
import json

client_id = "3837af8d370642ed88284060e558b1ad"
client_secret = "009c7f29c86345e1acd399dbe6bb2128"
endpoint = "https://accounts.spotify.com/api/token"

# python 3.x 버전
encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')
headers = {"Authorization": "Basic {}".format(encoded)}
payload = {"grant_type": "client_credentials"}
response = requests.post(endpoint, data=payload, headers=headers)
access_token = json.loads(response.text)['access_token']

#일단 함
headers = {"Authorization": "Bearer {}".format(access_token)}

## Spotify Search API
params = {
    "q": "BTS",
    "type": "artist",
    "limit": "1"
}

r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)

print(r.status_code)

# 데이터 삽입
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
client_id = '3837af8d370642ed88284060e558b1ad'
client_secret = '009c7f29c86345e1acd399dbe6bb2128'

#데이터 베이스 구축 아티스트들 다 포함 
aespa = '5LtZnAGm43uue7ZyjNBQ9J'
redvel='37i9dQZF1DX4NMZ4UC3NCh'
gg = '37i9dQZF1DZ06evO0s79KM'
boa = '0gvcnN0lKtpsbsjf0MOWVB'

candidate = [aespa, redvel,gg , boa]



track_uris =  []
playlist_uris = []

for artist_key in candidate:
    playlist_link = f'https://open.spotify.com/playlist/{artist_key}'
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    playlist_uris.append(playlist_URI)

    client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
    sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)
    

    for x in sp.playlist_tracks(playlist_URI)["items"]:
        track_uris.append(x["track"]["uri"])




track_keys = []
artist_list = []

for x in playlist_uris :
    track = sp.playlist_tracks(x)["items"]
    for j in track:
        track_name = j["track"]["name"]
        artist_name = j["track"]["artists"][0]["name"]
        artist_list.append([track_name, artist_name])




    for i in track:
        track_keys.append(i["track"]["uri"])


#audio feauture
track_list =[]
for k in track_keys:
    feature = sp.audio_features(k)[0]
    acousticness = feature["acousticness"]
    danceability = feature["danceability"]
    energy = feature["energy"]
    instrumentalness = feature["instrumentalness"]
    key = feature["key"]
    liveness = feature["liveness"]
    loudness = feature["loudness"]
    mode = feature["mode"]
    speechiness = feature["speechiness"]
    tempo = feature["tempo"]
    valence = feature["valence"]

    track_list.append([acousticness, danceability, energy,
            instrumentalness, key, liveness, loudness,
            mode, speechiness, tempo, valence])


music_features = []

for i in range(len(artist_list)):
    sum = artist_list[i] +  track_list[i]
    sum = tuple(sum)
    music_features.append(sum)


    

cursor.executemany("""INSERT INTO kwangya(track, artist,acousticness, danceability, energy,
            instrumentalness, key, liveness, loudness,
            mode, speechiness, tempo, valence) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",music_features)


conn.commit()
conn.close()



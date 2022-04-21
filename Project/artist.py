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

songs = []
artist = []

for artist_key in candidate:
    playlist_link = f'https://open.spotify.com/playlist/{artist_key}'
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
    sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        #URI
        track_uri = track["track"]["uri"]
    
        #Track name
        track_name = track["track"]["name"]
    
        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
    
        #Name, popularity, genre
        artist_name = track["track"]["artists"][0]["name"]
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]
    
        #Album
        album = track["track"]["album"]["name"]
    
        #Popularity of the track
        track_pop = track["track"]["popularity"]

        artist.append(sp.artist(artist_uri))


from pymongo import MongoClient

HOST = 'cluster0.dwyua.mongodb.net'
USER = 'kingjiwoo'
PASSWORD = '1q2w3e4r'
DATABASE_NAME = 'kwangya'
COLLECTION_NAME = 'artist'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"


client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

collection = database[COLLECTION_NAME]

collection.insert_many(artist)

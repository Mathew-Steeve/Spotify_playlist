import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_Secret"]
redirect_uri = 'https://example.com'
scope = "playlist-modify-private"


date = input("Which year do you want to travel to? Type the date in the format YYYY-MM-DD:")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
website = response.content
soup = BeautifulSoup(website, "lxml")
all_songs = soup.select("li h3#title-of-a-story")
all_song = [song.get_text().strip() for song in all_songs]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               redirect_uri=redirect_uri, cache_path="Token.txt"))
user = sp.current_user()
# print(user)
user_id = user["id"]
# print(user_id)
song_uri_ls = []
# pprint.pp(song_uri_ls)
new_playlist = sp.user_playlist_create(user_id, name=f"{date} Billboard 100", public=False)
playlist_id = new_playlist["id"]
year = date.split("-")[0]
for track in all_song:
    res = sp.search(q=f"track:{track} year:{year}", type="track")
# pprint.pp(song_uri_ls[0])
    try:
        uri = res["tracks"]["items"][0]["uri"]
        song_uri_ls.append(uri)
    except IndexError:
        print(f"{track} doesn't exist.")

sp.playlist_add_items(playlist_id, song_uri_ls)

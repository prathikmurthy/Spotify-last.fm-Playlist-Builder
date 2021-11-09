import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json
import os
from dotenv import load_dotenv

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'prathikm'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = os.getenv('LASTFM_KEY')
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

scope = "playlist-modify-public"
user='pmurthy20'

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIFY_API_KEY'), client_secret=os.getenv('SPOTIFY_API_SECRET'), scope=scope, redirect_uri='http://example.com'))

playlist_name = 'last.fm Liked Songs-TEST'
playlist_desc = 'This playlist is automatically updated using a Python script whenever a new song is liked on last.fm :)'

results=sp.user_playlists(user=user)

playlist_list = []
for idx, item in enumerate(results['items']):
    if item['name'] == playlist_name:
        playlist_list.append((item['name'], item['id']))

if len(playlist_list) == 0:
    sp.user_playlist_create(user='pmurthy20', name=playlist_name, public=True, description=playlist_desc)

r = lastfm_get({
    'method': 'user.getLovedTracks',
    'user': 'prathikm'
})

# jprint(r.json())

loved_tracks = []
for idx, item in enumerate(r.json()['lovedtracks']['track']):
    track_name = item['name']
    track_artist = item['artist']['name']
    loved_tracks.append((track_name, track_artist))

spotify_playlist_items = sp.playlist_items(playlist_id=playlist_list[0][1])['items']
spotify_playlist_names = []
for track in spotify_playlist_items:
    jprint(track['track']['name'])
    spotify_playlist_names.append(track['track']['name'])

for x in loved_tracks:
    results= sp.search('track:'+str(x[0])+' artist:'+str(x[1]), type='track', limit=1)
    if len(results['tracks']['items']) > 0:
        if results['tracks']['items'][0]['name'] not in spotify_playlist_names:
            sp.playlist_add_items(playlist_id=playlist_list[0][1], items=[results['tracks']['items'][0]['uri'][14:]])

        # sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_list[0][1], items=[results['tracks']['items'][0]['uri'][14:]])
    else:
        results= sp.search(str(x[0]), type='track', limit=1)
        if len(results['tracks']['items']) > 0:
                if results['tracks']['items'][0]['name'] not in spotify_playlist_names:
                    sp.playlist_add_items(playlist_id=playlist_list[0][1], items=[results['tracks']['items'][0]['uri'][14:]])

                # sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_list[0][1], items=[results['tracks']['items'][0]['uri'][14:]])
        

quit()
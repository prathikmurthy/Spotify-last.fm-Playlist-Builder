import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json
import os

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'prathikm'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = os.environ.get('LASTFM_KEY')
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

scope = "playlist-modify-public"
user='pmurthy20'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIFY_API_KEY'), client_secret=os.environ.get('SPOTIFY_SECRET_KEY'), scope=scope, redirect_uri='http://example.com'))



# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# sp.user_playlist_create(user='pmurthy20', name='test', public=True, description='test')

# sp.user_playlist_create(user='pmurthy20', name='last.fm Liked Songs-TEST', public=True, description='This playlist is automatically updated using a Python script whenever a new song is liked on last.fm :)')


results=sp.user_playlists(user=user)

playlist_list = []
for idx, item in enumerate(results['items']):

    # if item['name'] == 'last.fm Liked Songs':
    #     playlist_list.append((item['name'], item['id']))

    if item['name'] == 'last.fm Liked Songs':
        playlist_list.append((item['name'], item['id']))

# Needs to be reimplemented at some point
# if 'test' not in playlist_list:





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

# print(loved_tracks)

spotify_playlist_items = sp.playlist_items(playlist_id=playlist_list[0][1])['items']
spotify_playlist_names = []
for track in spotify_playlist_items:
    jprint(track['track']['name'])
    spotify_playlist_names.append(track['track']['name'])

# jprint(spotify_playlist_names)


# for x in range(len(loved_tracks)):

# print('track:'+loved_tracks[x][0]+' artist:'+loved_tracks[x][1])
for x in loved_tracks:
    results= sp.search('track:'+str(x[0])+' artist:'+str(x[1]), type='track', limit=1)
    if len(results['tracks']['items']) > 0:
        # if results['tracks']['items'][0]['name'] not in spotify_playlist_names:
            # sp.playlist_add_items(playlist_id=playlist_list[0][1], items=[results['tracks']['items'][0]['uri'][14:]])

        sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_list[0][1], items=[results['tracks']['items'][0]['uri'][14:]])
    else:
        print('Unable to add to Playlist: ' + 'track:'+str(x[0]) + ' last.fm artist: ' +str(x[1]))
        
    


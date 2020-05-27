import sys
import spotipy
import spotipy.util as util
import pandas as pd

#----------------SetUp Spotify------------------#
scope = 'user-library-read'


token = util.prompt_for_user_token('alberto.mrtn',scope, client_id='23c9bd477825415f935a01597ebab104',client_secret='a810f4eae19f40f6af6b12c35a1d58bd', redirect_uri='http://localhost:8888/callback/')

sp = spotipy.Spotify(auth=token)

#----------------------------------#


if token:
    print("Connexion OK")

    results = sp.playlist_tracks('37i9dQZEVXbIPWwFssbupI')
    id_songs = []

    #audio_features
    for item in results['items']:
        track = item['track']
        #print(track)
        #id_songs = results = track['']
        #print(track['name'] + ' - ' + track['id'])
        id_songs.append(track['id'])
    #print(id_songs)
    feautures_of_songs = sp.audio_features(id_songs)
    print(feautures_of_songs)
else:
    print("Can't get token for", 'alberto.mrtn')
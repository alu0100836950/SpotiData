import sys
import spotipy
import spotipy.util as util
import pandas as pd
import csv

#----------------SetUp Spotify------------------#
scope = 'user-library-read'
token = util.prompt_for_user_token('alberto.mrtn',scope, client_id='23c9bd477825415f935a01597ebab104',client_secret='a810f4eae19f40f6af6b12c35a1d58bd', redirect_uri='http://localhost:8888/callback/')
sp = spotipy.Spotify(auth=token)
#----------------------------------#


def getFeature(items):
    idList = []
    for item in items:
        track = item['track']
        idList.append(track['id'])
    featuresList = sp.audio_features(idList)

    result = []
    for feature in featuresList:
        track_id = feature['track_href']
        title = sp.track(track_id)['name'].replace(',', ' ')
        danceability = feature['danceability']
        energy = feature['energy']
        speechiness = feature['speechiness']
        valence = feature['valence']
        mode = feature['mode']
        acousticness = feature['acousticness']
    
        result.append({'title': title, 'danceability': danceability, 'energy': energy, 'speechiness': speechiness, 'valence': valence, 'mode': mode, 'acousticness': acousticness})
    return result



#------- Programa principal -------#

if token:
    print("Connection OK")


    PLAYLIST_ID = '37i9dQZEVXbLoATJ81JYXz'
    items = sp.playlist_tracks(PLAYLIST_ID)['items']


    features = getFeature(items)

    with open('features.csv', mode='w') as f:
        f.write('title,danceability,acousticness,energy,speechiness,valence,mode\n')
        for feature in features:
            f.write(feature['title'].encode('utf-8') + ',' + str(feature['danceability']) + ',' + str(feature['acousticness'])
            + ',' + str(feature['energy']) + ',' + str(feature['speechiness']) + ',' + str(feature['valence']) + ','
            + str(feature['mode']) + '\n')


    df = pd.read_csv('features.csv')
    print(df)
    print(df.describe())


else:
    print("Can't get token")




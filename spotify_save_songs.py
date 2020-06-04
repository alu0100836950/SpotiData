import sys
import spotipy
import spotipy.util as util
import pandas as pd
import csv
import seaborn as sns
import matplotlib.style as style
import matplotlib.pyplot as plt
import numpy as np

#----------------SetUp Spotify------------------#
scope = 'user-library-read'
token = util.prompt_for_user_token('alberto.mrtn',scope, client_id='23c9bd477825415f935a01597ebab104',client_secret='a810f4eae19f40f6af6b12c35a1d58bd', redirect_uri='http://localhost:8888/callback/')
sp = spotipy.Spotify(auth=token)
#----------------------------------#

def show_pairplot(df, audio_feature_headers):
    
    
    # Seaborn style
    sns.set(style="white")
    style.use('seaborn-poster') #sets the size of the charts
    style.use('ggplot')


    g =sns.pairplot(df[audio_feature_headers],height = 5, aspect = 0.5)
    plt.show()

def show_heatmap(df, audio_feature_headers):
    
    corr = df[audio_feature_headers].corr()

    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(11,9))

    cmap = sns.diverging_palette(220,10, as_cmap=True)

    sns_plot = sns.heatmap(corr, mask=mask, cmap=cmap, vmax =.6, vmin=-.4, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    sns_plot.figure.savefig("./img_graphs/HeatMap.png")
    
    plt.show()
  

def show_relation(df):

    # De esta forma tambien podemos ver los histogramas

    #sns.jointplot(x='energy', y='valence', data=df, kind='reg')
    #sns.jointplot(x='danceability', y='valence', data=df, kind='reg')

    # Otra forma de ver la relacion de dos variables
    sns.regplot(x='energy', y='acousticness', data=df)
    plt.show()

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

    audio_feature_headers = ['danceability', 'energy', 'speechiness', 'valence', 'mode','acousticness']

    features = getFeature(items)

    with open('features.csv', mode='w') as f:
        f.write('title,danceability,acousticness,energy,speechiness,valence,mode\n')
        for feature in features:
            f.write(feature['title'] + ',' + str(feature['danceability']) + ',' + str(feature['acousticness']) #.encode('utf-8') a mi me peta si se lo pongo al title
            + ',' + str(feature['energy']) + ',' + str(feature['speechiness']) + ',' + str(feature['valence']) + ','
            + str(feature['mode']) + '\n')


    df = pd.read_csv('features.csv')
    df = df.dropna()
    print(df)
    print(df.describe())

#   ********mostramos las gráficas************

    #show_pairplot(df, audio_feature_headers)
    show_heatmap(df,audio_feature_headers)
    #show_relation(df)

else:
    print("Can't get token")




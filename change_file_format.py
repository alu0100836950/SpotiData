import sys
import spotipy
import spotipy.util as util
import pandas as pd
import csv
import seaborn as sns
import matplotlib.style as style
import matplotlib.pyplot as plt
import numpy as np
from sys import argv
import os


#----------------SetUp Spotify------------------#
scope = 'user-library-read'
token = util.prompt_for_user_token('alberto.mrtn',scope, client_id='23c9bd477825415f935a01597ebab104',client_secret='a810f4eae19f40f6af6b12c35a1d58bd', redirect_uri='http://localhost:8888/callback/')
sp = spotipy.Spotify(auth=token)
#----------------------------------#




if token:


    print("Connection OK")
    print("Obteniendo y transformando datos...")

    read_file = argv[1]

    df = pd.read_csv(read_file)
    df = df.dropna()

    print(df.shape)

    name_file = read_file.rpartition('/')[2] # return -> top_200_spain.csv
    name_file_end = os.path.splitext(name_file)[0] # nos quedamos sin la extension

    def features_to_csv(id_song):
        featuresList = sp.audio_features(id_song)[0]
        
        string_features = str(featuresList['danceability']) + ',' + str(featuresList['energy']) + ',' + str(featuresList['speechiness']) + ',' + str(featuresList['valence']) + ',' + str(featuresList['mode']) + ','+ str(featuresList['acousticness']) + ','+ str(featuresList['tempo']) + ',' + str(featuresList['duration_ms']) + ',' + str(featuresList['loudness']) + '\n'
        
        return string_features


    with open('./data_format/'+name_file_end + '_format'+'.csv', mode='w') as f:
        f.write('position,track_name,title_author,danceability,energy,speechiness,valence,mode,acousticness,tempo,duration_ms,loudness\n')
        for i,linea in df.iterrows():
            
            f.write(str(linea['Position']) + ','+ str(linea['Track_Name']).replace(',','-') + ','+ str(linea['Artist']).replace(',','-') + ','+ features_to_csv(linea['URL'].rpartition('/')[2]))


else:
    print("Can't get token")        
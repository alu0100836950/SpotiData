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
#****************************************************************************************
    sns_plot = sns.jointplot(x='energy', y='valence', data=df, kind='reg')
    #sns_plot = sns.jointplot(x='danceability', y='valence', data=df, kind='reg')
    #name_graph = ""
    #sns_plot.figure.savefig("./img_graphs/relations" + name_graph +".png")

    plt.show()




#------- Programa principal -------#

if token:
    print("Connection OK")
    print("Calculando datos...")

    read_file = argv[1]

    df = pd.read_csv(read_file)
    df = df.dropna()

    print(df.shape)
   
   
    audio_feature_headers = ['danceability', 'energy', 'speechiness', 'valence', 'mode','acousticness']

    id_songs = []
    featuresList = []
    result = []

    name_file = read_file.rpartition('/')[2] # return -> top_200_spain.csv
    name_file_end = os.path.splitext(name_file)[0] # nos quedamos sin la extension


    def features_to_csv(id_song):
        featuresList = sp.audio_features(id_song)[0]
        
        string_features = str(featuresList['danceability']) + ',' + str(featuresList['energy']) + ',' + str(featuresList['speechiness']) + ',' + str(featuresList['valence']) + ',' + str(featuresList['mode']) + ','+ str(featuresList['acousticness']) + '\n'
        
        return string_features


    with open('./data_format/'+name_file_end + '_format'+'.csv', mode='w') as f:
        f.write('date,position,track_name,title_author,danceability,energy,speechiness,valence,mode,acousticness\n')
        for i,linea in df.iterrows():
            
            f.write(str(linea['Fecha']) + ','+ str(linea['Position']) + ','+ str(linea['Track_Name']).replace(',','-') + ','+ str(linea['Artist']).replace(',','-') + ','+features_to_csv(linea['URL'].rpartition('/')[2]))

    


    
    df_format = pd.read_csv('./data_format/'+name_file_end +'_format.csv')
    #df = df.dropna()

    print(df_format.describe())

#   ********mostramos las gráficas************

    #show_pairplot(df, audio_feature_headers)
    show_heatmap(df_format,audio_feature_headers)
    show_relation(df_format)

#   ******** COMPROBAMOS ALGUNAS COSAS *************

    #comprobamos que las canciones mas energicas son bailables y su valor de acoustico es muy pobre
    #lo mostramos en consola una pequeña tabla
    #high_vs_acoustic = df[(df['energy'] > 0.8) & (df['acousticness'] < 0.2)][['energy', 'acousticness', 'danceability']] # Low-acousticness - High-energy
    #print(high_vs_acoustic.head(5))

else:
    print("Can't get token")

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

read_file = argv[1]

audio_feature_headers = ['danceability', 'energy', 'speechiness', 'valence', 'mode','acousticness']


df_format = pd.read_csv(read_file)
#df = df.dropna()

print(df_format.describe())

#   ********mostramos las gráficas************

#show_pairplot(df, audio_feature_headers)
show_heatmap(df_format,audio_feature_headers)
show_relation(df_format)

#   ******** COMPROBAMOS ALGUNAS COSAS *************

#comprobamos que las canciones mas energicas son bailables y su valor de acoustico es muy pobre
#lo mostramos en consola una pequeña tabla
high_vs_acoustic = df_format[(df_format['energy'] > 0.8) & (df_format['acousticness'] < 0.2)][['energy', 'acousticness', 'danceability']] # Low-acousticness - High-energy
print(high_vs_acoustic.head(5))



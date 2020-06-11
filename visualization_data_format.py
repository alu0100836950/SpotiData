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
    sns_plot.figure.savefig('./img_graphs_'+ country + '/HeatMap.png')
    
    plt.show()
  

def show_relation(df):

    # De esta forma tambien podemos ver los histogramas
#****************************************************************************************
    sns_plot = sns.jointplot(x='energy', y='valence', data=df, kind='reg')
    #sns_plot = sns.jointplot(x='danceability', y='valence', data=df, kind='reg')
    
    sns_plot.savefig('./img_graphs_'+ country + '/relations.png')
    plt.show()


def show_top_position_min(df):
    songs_grouped = df.groupby('URL').min()
    songs_grouped_ranges = songs_grouped.groupby(pd.cut(songs_grouped["position"], np.arange(0, 51, 5))).count()
    f, ax = plt.subplots(figsize=(15, 5))
    sns_plot = sns.barplot(x=songs_grouped_ranges.index.values, y=songs_grouped_ranges["position"])
    ax.set(title="prueba", ylabel="count")
    sns_plot.figure.savefig('./img_graphs_'+ country + '/BarMin.png')


def show_top_position_mean(df):
    songs_grouped = df.groupby('URL').mean()
    songs_grouped_ranges = songs_grouped.groupby(pd.cut(songs_grouped["position"], np.arange(0, 51, 5))).count()
    f, ax = plt.subplots(figsize=(15, 5))
    sns_plot = sns.barplot(x=songs_grouped_ranges.index.values, y=songs_grouped_ranges["position"])
    ax.set(title="prueba", ylabel="count")
    sns_plot.figure.savefig('./img_graphs_'+ country + '/BarMean.png')


def tempo_to_rythm(tempo):
    if tempo < 66:
        return 'lento'
    if 66 <= tempo < 76:
        return 'adagio'
    if 76 <= tempo < 108:
        return 'andante'
    if 108 <= tempo < 168:
        return 'allegro'
    if 168 <= tempo:
        return 'presto' 


def show_pie(df):
    songs_grouped = df.groupby('URL').min()
    gsongs = songs_grouped
    gsongs['rythm'] = gsongs['tempo'].transform(tempo_to_rythm)
    fig, ax = plt.subplots(figsize = (8, 8))
    ax.pie(gsongs['rythm'].value_counts(), labels = gsongs['rythm'].value_counts().axes[0], autopct = '%1.1f%%', shadow = True, textprops = {'fontsize': 16})
    ax.set_title('Ritmo')
    ax.figure.savefig('./img_graphs_'+ country + '/Pie.png')
    plt.show()


#------- Programa principal -------#

read_file = argv[1]

audio_feature_headers = ['danceability', 'energy', 'speechiness', 'valence', 'mode','acousticness','tempo', 'duration_ms','loudness','key']


name_file = read_file.rpartition('/')[2] # return -> list_top_50_2020_x.csv
name_file_end = os.path.splitext(name_file)[0] # nos quedamos sin la extension
country = name_file_end.split('_')[4]



df_format = pd.read_csv(read_file)
df_format.dropna()

print(df_format.describe())



#   ********mostramos las gráficas************

#show_pairplot(df, audio_feature_headers)
show_heatmap(df_format,audio_feature_headers)
show_relation(df_format)
show_top_position_mean(df_format)
show_top_position_min(df_format)
show_pie(df_format)


#   ******** COMPROBAMOS ALGUNAS COSAS *************

#comprobamos que las canciones mas energicas son bailables y su valor de acoustico es muy pobre
#lo mostramos en consola una pequeña tabla
high_vs_acoustic = df_format[(df_format['energy'] > 0.8) & (df_format['acousticness'] < 0.2)][['energy', 'acousticness', 'danceability']] # Low-acousticness - High-energy
#print(high_vs_acoustic.head(5))



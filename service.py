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
from wordcloud import WordCloud, STOPWORDS
from flask import Flask
from flask import render_template, request
import json



app = Flask(__name__)



def get_dir(country):
    return 'data_format/list_top_50_2020_' + country + '_format.csv'


@app.route('/heatMap')
def show_heatmap():
    country = request.args.get('country')
    df_format = pd.read_csv(get_dir(country))
    df_format.dropna()
    df = df_format
    audio_feature_headers = ['danceability', 'energy', 'speechiness', 'valence', 'tempo', 'acousticness', 'duration_ms','loudness','key']
    corr = df[audio_feature_headers].corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(11,9))
    cmap = sns.diverging_palette(220,10, as_cmap=True)
    sns_plot = sns.heatmap(corr, mask=mask, cmap=cmap, vmax =.6, vmin=-.4, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    row_list = []
    for index, rows in corr.iterrows():
        corr_list = [rows.danceability, rows.energy, rows.speechiness, rows.valence, rows.tempo, rows.acousticness, rows.duration_ms, rows.loudness, rows.key]    
        row_list.append(corr_list)
    return json.dumps(row_list)


@app.route('/relation')
def show_relation():
    country = request.args.get('country')
    x = request.args.get('x')
    y = request.args.get('y')
    df_format = pd.read_csv(get_dir(country))
    df_format.dropna()
    df = df_format
    #sns_plot = sns.jointplot(x='energy', y='valence', data=df, kind='reg')
    return json.dumps({'x': df[x].values.tolist(), 'y': df[y].values.tolist()})


@app.route('/topmin')
def show_top_position_min():
    country = request.args.get('country')
    df_format = pd.read_csv(get_dir(country))
    df_format.dropna()
    df = df_format
    songs_grouped = df.groupby('URL').min()
    songs_grouped_ranges = songs_grouped.groupby(pd.cut(songs_grouped["position"], np.arange(0, 51, 5))).count()
    return json.dumps({'y': songs_grouped_ranges['position'].values.tolist()})
    #f, ax = plt.subplots(figsize=(15, 5))
    #sns_plot = sns.barplot(x=songs_grouped_ranges.index.values, y=songs_grouped_ranges["position"])
    #ax.set(title="prueba", ylabel="count")



def show_top_position_mean(country):
    df_format = pd.read_csv(get_dir(country))
    df_format.dropna()
    df = df_format
    songs_grouped = df.groupby('URL').mean()
    songs_grouped_ranges = songs_grouped.groupby(pd.cut(songs_grouped["position"], np.arange(0, 51, 5))).count()
    f, ax = plt.subplots(figsize=(15, 5))
    sns_plot = sns.barplot(x=songs_grouped_ranges.index.values, y=songs_grouped_ranges["position"])
    ax.set(title="prueba", ylabel="count")



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



@app.route('/pie')
def show_pie():
    country = request.args.get('country')
    df_format = pd.read_csv(get_dir(country))
    df_format.dropna()
    df = df_format
    songs_grouped = df.groupby('URL').min()
    gsongs = songs_grouped
    gsongs['rythm'] = gsongs['tempo'].transform(tempo_to_rythm)
    serie = gsongs['rythm'].value_counts().tolist()
    return json.dumps({'labels': gsongs['rythm'].value_counts().axes[0].values.tolist(), 'values': serie})


@app.route('/keys')
def distribution_key_songs():
    country = request.args.get('country')
    df_format = pd.read_csv(get_dir(country))
    df_format.dropna()
    df = df_format
    gsongs = df.groupby('URL').min()
    keys = np.array(['Do', 'Do#/Re♭', 'Re', 'Re#/Mi♭', 'Mi', 'Mi#/Fa♭', 'Fa', 'Fa#/Sol♭', 'Sol', 'Sol#/La♭', 'La', 'La#/Si♭', 'Si', 'Si#/Do♭'])
    keys_top10 = pd.Series(keys[gsongs[gsongs['position']<10]['key']])
    keys_count = keys_top10.value_counts()
    print(keys.tolist())
    print(keys_count.values.tolist())
    return json.dumps({'x': keys.tolist(), 'y': keys_count.values.tolist()})
    #f, ax = plt.subplots(figsize=(15,5))
    #sns.barplot(x=keys_count.axes[0], y=keys_count.values)
    #ax.set(title="Tonos mas repetidos en el top 10", label="Numero de canciones")



def words_used(country):
    df_format = pd.read_csv(country)
    df_format.dropna()
    df = df_format
    gsongs = df.groupby('URL').min()
    top_10_title = gsongs[gsongs["position"] <= 10]['track_name'].values
    wc = WordCloud(stopwords=STOPWORDS).generate(" ".join(top_10_title))
    plt.figure(figsize=(80,80))
    plt.subplot(1,2,2)
    plt.imshow(wc)
    plt.title('Palabras mas repetidas', fontsize=30)
    plt.axis("off")
    plt.show()


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)


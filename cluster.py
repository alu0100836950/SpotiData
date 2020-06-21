import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def get_dir(country):
    return 'data_format/list_top_50_2020_' + country + '_format.csv'



df_format = pd.read_csv(get_dir('spain'))
df_format.dropna()
df = df_format
songs_grouped = df.groupby('URL').min()
songs_grouped['success'] = songs_grouped['position'] < 15
songs_grouped['success'] = songs_grouped['success'].astype(int)



fig = px.scatter_matrix(songs_grouped,
    dimensions = ['acousticness', 'energy', 'loudness', 'danceability', 'valence'],
    color="success")
fig.show()



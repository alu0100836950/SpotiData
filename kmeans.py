import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans



def get_dir(country):
    return 'data_format/list_top_50_2020_' + country + '_format.csv'


df_format = pd.read_csv(get_dir('spain'))
df_format.dropna()
df = df_format

songs_grouped = df.groupby('URL').min()
songs_grouped['success'] = songs_grouped['position'] < 15
songs_grouped['success'] = songs_grouped['success'].astype(int)

print(songs_grouped)

X = np.array(songs_grouped[['acousticness', 'energy', 'duration_ms']])
Y = np.array(songs_grouped['success'])

#Mostramos las características
# fig = plt.figure()
# ax = Axes3D(fig)
# colors = ['blue', 'red']
# assign = []
# for row in Y:
#     assign.append(colors[row])
# ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=assign, s=60)


# Calculando la mejor K
# Nc = range(1,20)
# kmeans = [KMeans(n_clusters=i) for i in Nc]
# kmeans
# score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
# score
# plt.plot(Nc,score)
# plt.xlabel('Número de clusters')
# plt.ylabel('Score')
# plt.title('Curva')
# plt.show()

kmeans = KMeans(n_clusters = 2).fit(X)
centroids = kmeans.cluster_centers_
labels = kmeans.predict(X)

colors = ['blue', 'red']
assign = []
for row in labels:
    assign.append(colors[row])

print(centroids)

f1 = songs_grouped['energy'].values
f2 = songs_grouped['success'].values

plt.scatter(f1, f2, c=assign, s=70)
plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', c=colors, s=500)
plt.show()
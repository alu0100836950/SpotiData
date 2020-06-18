from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pylab as pl

from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification


from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import model_selection
from pandas.plotting import scatter_matrix


features = ['danceability', 'energy', 'speechiness', 'valence', 'mode', 'acousticness', 'tempo', 'duration_ms', 'loudness', 'key']
predict_header = ['success']

def get_dir(country):
    return 'data_format/list_top_50_2020_' + country + '_format.csv'



df_format = pd.read_csv(get_dir('spain'))
df_format.dropna()
df = df_format
songs_grouped = df.groupby('URL').min()
songs_grouped['success'] = songs_grouped['position'] < 15
songs_grouped['success'] = songs_grouped['success'].astype(int)
# sns.countplot(x="success", data=songs_grouped)
# plt.show()

# Hacemos una primera prueba con el algoritmo KNeighbours Classiffier
X_all = songs_grouped[features]
Y_all = songs_grouped[predict_header]


# X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)
# knn = KNeighborsClassifier(n_neighbors = 3)
# knn.fit(X_train, Y_train)
# prediction = knn.predict(X_test)
# print(knn.score(X_test, Y_test))
# labels = ['1', '0']
# cm = confusion_matrix(Y_test, prediction)
# sns.heatmap(cm, annot = True, cmap="Blues")
# plt.show()


# #Volvemos a probar eliminando algunos atributos
# X_all = songs_grouped[features]
# X_all = X_all.drop(['duration_ms', 'loudness', 'key', 'tempo', 'speechiness', 'mode'], axis = 1)
# X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)
# knn = KNeighborsClassifier(n_neighbors = 23)
# knn.fit(X_train, Y_train)
# prediction = knn.predict(X_test)
# print(knn.score(X_test, Y_test))
# cm = confusion_matrix(Y_test, prediction)
# sns.heatmap(cm, annot = True, cmap="Blues")
# plt.show()




# #Buscamos el mejor valor para el parámetro K
# X_all = songs_grouped[features]
# X_all = X_all.drop(['duration_ms', 'loudness', 'key', 'tempo', 'speechiness', 'mode'], axis = 1)

# X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)

# test_accuracy = []
# rg = np.arange(1, 25)

# for i, k in enumerate(rg):
#     knn = KNeighborsClassifier(n_neighbors=k)
#     knn.fit(X_train, Y_train)
#     test_accuracy.append(knn.score(X_test, Y_test))
    
# plt.figure(figsize=[13,8])
# plt.plot(rg, test_accuracy)
# plt.legend()
# plt.title('K VS Precisión')
# plt.xlabel('K')
# plt.ylabel('Precisión')
# plt.show()
# print("Mejor precision: {} con K = {}".format(np.max(test_accuracy),1+test_accuracy.index(np.max(test_accuracy))))    
# labels = ['1', '0']
# cm = confusion_matrix(Y_test, prediction)
# sns.heatmap(cm, annot = True, cmap="Blues")
# plt.show()







################# RED NEURONAL. MIRAR SI DA TIEMPO
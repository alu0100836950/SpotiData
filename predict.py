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

X_all = songs_grouped[features]
Y_all = songs_grouped[predict_header]

X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)
prediction = knn.predict(X_test)

print(knn.score(X_test, Y_test))


X_all = songs_grouped[features]
X_all = X_all.drop(['duration_ms', 'loudness', 'key', 'tempo', 'speechiness', 'mode'], axis = 1)
X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors = 2)
knn.fit(X_train, Y_train)
prediction = knn.predict(X_test)
print(knn.score(X_test, Y_test))

# labels = ['1', '0']
# cm = confusion_matrix(Y_test, prediction)
# sns.heatmap(cm, annot = True, cmap="Blues")
# plt.show()


################# RED NEURONAL. MIRAR SI DA TIEMPO

# X_all = songs_grouped[features]
# Y_all = songs_grouped[predict_header]
# X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)

# clf = MLPClassifier(hidden_layer_sizes=(100, 100, 100), max_iter=10000, alpha=0000.1,
#                      solver='adam', verbose=10,  random_state=42, tol=0.00000001, activation='relu')

# clf.fit(X_train, Y_train)
# prediction = clf.predict(X_test)

# cm = confusion_matrix(Y_test, prediction)
# sns.heatmap(cm, center=True)
# plt.show()

# print(accuracy_score(Y_test, prediction))
# print(prediction)

###############################################



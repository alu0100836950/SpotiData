from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import pylab as pl

from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier


features = ['danceability', 'energy', 'speechiness', 'valence', 'mode', 'acousticness', 'tempo', 'duration_ms', 'loudness', 'key']
predict_header = ['success']

def get_dir(country):
    return 'data_predict/list_top_50_2020_' + country + '_format.csv'



df_format = pd.read_csv(get_dir('spain'))
df_format.dropna()
df = df_format

songs_grouped = df.groupby('URL').min()

songs_grouped['success'] = songs_grouped['position'] < 15
songs_grouped['success'] = songs_grouped['success'].astype(int)


X_all = songs_grouped[features]
Y_all = songs_grouped[predict_header]
X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)
rfc = RandomForestClassifier(max_depth=25, random_state=43)
rfc.fit(X_train, Y_train.values.ravel())

df = pd.DataFrame({'group': X_train.columns, 'values': rfc.feature_importances_})
ordered_df = df.sort_values(by='values')

my_range=range(1, len(df.index) + 1)
plt.hlines(y=my_range, xmin=0, xmax=ordered_df['values'], color='skyblue')
plt.plot(ordered_df['values'], my_range, "o", color="skyblue")
plt.yticks(my_range, ordered_df['group'])
plt.title("Importance of features for RandomForest", loc='left')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()

# X_all = songs_grouped[features]
# X_all = X_all.drop(['acousticness', 'duration_ms', 'loudness', 'valence', 'key', 'mode'], axis = 1)
# X_train, X_test, Y_train, Y_test = train_test_split(X_all, Y_all, test_size=0.2, random_state=42)
# rfc = RandomForestClassifier(max_depth=14, random_state=47)
# rfc.fit(X_train, Y_train.values.ravel())
# print(rfc.score(X_test, Y_test))

# prediction = rfc.predict(X_test)
# print(prediction)



# test_accuracy = []
# rg = np.arange(1, 200)
# for i, max_depth in enumerate(rg):
#     rfc = RandomForestClassifier(max_depth=max_depth, random_state=47)
#     rfc.fit(X_train, Y_train.values.ravel())
#     test_accuracy.append(rfc.score(X_test, Y_test))
    


rfc = RandomForestClassifier(max_depth=13, random_state=47)
rfc.fit(X_train, Y_train.values.ravel())
df_predict = pd.read_csv('data_predict/list_top_50_2020_spain_last.csv')
songs_grouped = df_predict.groupby('URL').min()
X_all = songs_grouped[features]


songs_grouped['success'] = songs_grouped['position'] < 15
songs_grouped['success'] = songs_grouped['success'].astype(int)
Y_all = songs_grouped[predict_header]
p = rfc.predict(X_all)
print(classification_report(Y_all, p))
labels = ['1', '0']
cm = confusion_matrix(Y_all, p)
sns.heatmap(cm, annot = True, cmap="Blues")
plt.show()
Y_all['result'] = p
print(Y_all)



# plt.figure(figsize=[13,8])
# plt.plot(rg, test_accuracy, label = 'Precisión de test')
# plt.legend()
# plt.title('max_depth VS Precisión')
# plt.xlabel('max_depth')
# plt.ylabel('Precisión')
# plt.show()
# print("Best precision: {} with max_depth = {}".format(np.max(test_accuracy),1+test_accuracy.index(np.max(test_accuracy))))


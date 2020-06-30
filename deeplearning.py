# Imports
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
# Load Data
#iris = load_iris()

csv_file='data.csv'
data = pd.read_csv('C:/Users/adam/Desktop/data.csv')


# Create a dataframe
df = pd.DataFrame(data, columns = ['blue_agent','area_now','area_#','time_transit','search_effectiveness','area_priority'])
target = df['area_priority']


X = df['time_transit']
X = X.values.reshape(1,-1)
df.sample(4)

# Instantiate Kmeans
km = KMeans(4)
clusts = km.fit_predict(X)

#Plot the clusters obtained using k means
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(km.cluster_centers_[:, 3],
            km.cluster_centers_[:, 0],
            km.cluster_centers_[:, 2],
            s = 250,
            marker='o',
            c='red',
            label='centroids')
scatter = ax.scatter(df['time_transit'],df['search_effectiveness'], df['area_priority'],
                     c=clusts,s=20, cmap='winter')


ax.set_title('time_transit')
ax.set_xlabel('Petal Width')
ax.set_ylabel('search_effectiveness')
ax.set_zlabel('area_priority')
ax.legend()
plt.show()
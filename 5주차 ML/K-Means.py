import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn import cluster
from sklearn import datasets

iris = datasets.load_iris()

X = iris.data
y = iris.target
print(X)
print()
print(y)

estimators = [('k=8', cluster.KMeans(n_clusters=8)),
              ('k=3', cluster.KMeans(n_clusters=3)),
              ('k-3', cluster.KMeans(n_clusters=3, n_init=1, init='random'))]

print(estimators[0])
print(estimators[1])
print(estimators[2])

fignum = 1
titles = ['8 clusters', '3 clusters', '3 clusters, bad initialization']

for name, est in estimators: # estimators : ('k=8', cluster.KMeans(n_clusters=8))
    fig = plt.figure(fignum, figsize=(7, 7)) # fignum 도화지를 여러장 만든다
    ax = Axes3D(fig, elev=48, azim=134) # Set the elevation and azimuth of the axes. (축의 고도와 방위각)
    est.fit(X)
    labels = est.labels_

    # X = iris.data
    ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=labels.astype(np.float), edgecolor='w', s=100)

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Petal width')
    ax.set_ylabel('Sepal length')
    ax.set_zlabel('Petal length')
    ax.set_title(titles[fignum - 1])
    ax.dist = 12 # 값이 커지면 전체 plot 이 작아짐
    
    fignum = fignum + 1

plt.show()
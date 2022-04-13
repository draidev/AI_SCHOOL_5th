import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn import decomposition
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data
y = iris.target

model = decomposition.PCA(n_components=3)
model.fit(X)
X = model.transform(X) # 모델에 맞춰서 원래 데이터를 차원이동


""" 2PCs 시각화 """
plt.scatter(X[:, 0], X[:, 1], c=iris.target)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

""" 3PCs 시각화"""
fig = plt.figure()
ax = Axes3D(fig, elev=48, azim=134) # Set the elevation and azimuth of the axes. (축의 고도와 방위각)

ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=iris.target, edgecolor='w', s=100)
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.dist = 12 # 값이 커지면 전체 plot 이 작아짐

plt.show()


""" 몇 개의 PC면 충분할까? """
# 각각의 새로운 축이 데이터셋의 분산(variance)을 얼마나 표현하는지 확인이 가능
print(model.explained_variance_ratio_)

# np.argmax : 최대값의 인덱스를 리턴
# np.cumsum : 누적된 합계를 계산  (cumulative sum : 누적합)
# 95% 이상의 variance 를 설명하기 위한 축의 갯수를 확인할 수 있음
print(np.argmax(np.cumsum(model.explained_variance_ratio_) >= 0.95) + 1)

# Better option (indicate the ratio of variance you wish to preserve)
model = decomposition.PCA(n_components=0.95)
model.fit(X)
X = model.transform(X)
print(X)
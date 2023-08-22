from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def inertia(sample, closest_cent):
    return sum([(sample[i] - closest_cent[i]) ** 2 for i in range(len(sample))])

iris = datasets.load_iris()
xpoints=[]
ypoints=[]
for i in range(1,11):
    kmeans= KMeans(n_clusters=i,random_state=0)
    kmeans.fit(iris.data)
    xpoints.append(i)
    ypoints.append(kmeans.inertia_)
plt.plot(xpoints,ypoints,'-gD', markevery=[1],label="inertia with elbow point marked")
plt.title('results')
plt.xlabel('clusters number')
plt.ylabel('avg inertia')
plt.savefig('elbow.png')

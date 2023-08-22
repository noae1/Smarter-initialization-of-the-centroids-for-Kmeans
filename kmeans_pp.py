import sys
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import mykmeanssp as km
script_dir = os.path.dirname(__file__)


np.random.seed(0)
#path1 = "C:/Users/Erezd/OneDrive/Desktop/input_2_db_1.txt"
#path2 = "C:/Users/Erezd/OneDrive/Desktop/input_2_db_2.txt"


def calcKmeans():

    if len(sys.argv)!=6 and len(sys.argv)!= 5:
        print("An Error Has Occurred")
        exit()
    if len(sys.argv) == 6:
        k, iter, epsilon, file_name_1, file_name_2 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        #todo: check if int
    else:
        k, epsilon, file_name_1, file_name_2 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        iter='300'
    # k, epsilon, file_name_1, file_name_2 = '7','0',os.path.join(script_dir,"tests/tests/Book1.csv"),os.path.join(script_dir,"tests/tests/input_2_db_2.txt")
    # iter='300'



    def d(dataItem,centroid):
        dataItem = dataItem[1:]
        centroid = centroid[1:]
        res = np.sqrt(np.sum((dataItem-centroid) ** 2))
        return res

    def prepData(data):
        res = []
        for line in data.readlines():
            innerlist = []
            for val in line.split(","):
                innerlist.append(float(val))
            res.append(innerlist)
        return res
    # if file_name_1.endswith('txt'):
    # with open(file_name_1, 'r') as rawData:
    #     data = prepData(rawData)
    #     file1_df = pd.DataFrame(data)
    #     file1_df.columns = [str(i) for i in range(len(file1_df.columns))]
    # # else:
    # #     file1_df=pd.read_csv(file_name_1)
    # # if file_name_2.endswith('txt'):
    # with open(file_name_2, 'r') as rawData:
    #     data = prepData(rawData)
    #     file2_df = pd.DataFrame(data)
    #     file2_df.columns = [str(i) for i in range(len(file2_df.columns))]
    if file_name_1.endswith('txt'):
        data1=np.genfromtxt(file_name_1,dtype=float,delimiter=",")
    else:
        with open(file_name_1, 'r', encoding='utf-8-sig') as f: 
            data1 = np.genfromtxt(f, dtype=float, delimiter=',')
    if file_name_2.endswith('txt'):
        data2=np.genfromtxt(file_name_2,dtype=float,delimiter=",")
    else:
        with open(file_name_2, 'r', encoding='utf-8-sig') as f: 
            data2 = np.genfromtxt(f, dtype=float, delimiter=',')
    file1_df=pd.DataFrame(data1)
    file2_df=pd.DataFrame(data2)
    file1_df.columns = [str(i) for i in range(file1_df.shape[1])]
    file2_df.columns = [str(i) for i in range(file2_df.shape[1])]
# else:
    #     file2_df=pd.read_csv(file_name_2)


    data_points = pd.merge(file1_df, file2_df, on='0')   # inner join
    data_points.columns = [str(i) for i in range(len(file1_df.columns) + len(file2_df.columns) - 1)]
    data_points = data_points.sort_values('0')

    rowCount = data_points.shape[0]
    columnCount = data_points.shape[1]


    if not (iter).isnumeric():
        print("Invalid maximum iteration!")
        sys.exit()
    if not (k).isnumeric():
        print("Invalid number of clusters!")
        sys.exit()
    if not epsilon.replace('.', '', 1).isdigit():
        print("An Error Has Occurred")
        sys.exit()
    k, iter, epsilon = int(k), int(iter), float(epsilon)
    if (k) % 1 != 0 or k <= 1 or k >= rowCount:
        print("Invalid number of clusters!")
        sys.exit()
    if iter % 1 != 0 or iter <= 1 or iter >= 1000:
        print("Invalid maximum iteration!")
        sys.exit()
   

    randomRow = np.random.choice(data_points['0'], 1)[0]
    newCentroid = np.array(data_points[data_points['0']==randomRow])
    centroids_indices = [int(newCentroid[0][0])]
    centroids = np.copy(newCentroid)

    while (len(centroids) < k):

        prob = np.zeros(rowCount)
        for i in range(rowCount):
            x_i = data_points.iloc[i].to_numpy()
            minD = d(x_i , centroids[0])
            for centroid in centroids:
                currD = d(x_i , centroid)
                if currD < minD:
                    minD = currD

            prob[i] = minD

        if np.sum(prob) != 0:
            prob = prob / np.sum(prob)


        randomRow = np.random.choice(data_points['0'], 1 , p = prob)[0]
        newCentroid = np.array(data_points[data_points['0']==randomRow])

        centroids = np.append(centroids,newCentroid, axis=0)
        centroids_indices.append(int(newCentroid[0][0]))

    # print(centroids)
    x=np.array(data_points)
    data_p= [[x[i][j] for j in range(1,columnCount)]  for i in range(rowCount)]
    cent_p= [[centroids[i][j] for j in range(1,columnCount)]  for i in range(k)]

    calcCentroids = km.fit(cent_p,data_p,k,iter,epsilon,rowCount,columnCount-1)
    print(','.join(str(v) for v in centroids_indices))
    for centroid in calcCentroids:
        print(','.join('{:.4f}'.format(v) for v in centroid))
    #print(centroids[0].tolist())



calcKmeans()

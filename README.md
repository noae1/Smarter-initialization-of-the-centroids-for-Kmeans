# K-means++ algorithm

This repository contains the implementation of the K-Means++ algorithm in Python, 
integrated with the K-means algorithm that is ported to a C extension using the C API.

## About
This algorithm ensures a smarter initialization of the centroids and improves the quality of the clustering.
Apart from initialization, the rest of the algorithm is the same as the standard K-means algorithm.

When initializing the centroids, it is important that the initially selected points are fairly apart.
Therefore, K-means++ is a smart way to tackle this problem.

## Algorithm
1. Choose one center uniformly at random among the data points.
2. For each data point x not chosen yet, compute D(x), the distance between x and the nearest
center that has already been chosen (D(x) is minimal Eclidean Distance between point x and centroids).
3. Choose one new data point at random as a new center, using a weighted probability distribution 
where a point x is chosen with probability proportional to P(x_l) = D(x_l)/sumOf(D(x_i) :for all x_i).
4. Repeat Steps 2 and 3 until k centers have been chosen.
5. Now that the initial centers have been chosen, proceed using standard k-means clustering.



## Description
## 1. kmeans_pp.py:
The main interface. It contains all of the command line argument interface, reading the data, the Numpy, K-means++ implementation, the
interface with your C extension and outputting the results.

- Reading user CMD arguments:
• k: Number of required clusters.
• iter: (Optional) argument determines the number of K-means iterations, if not provided the default value is 300.
• eps: the epsilon value for convergence Kmeans.
• file_name_1: The path to the file 1 that will contain N observations.
• file_name_2: The path to the file 2 that will contain N observations.

- Combine both input files by inner join using the first column in each file as a key.
- After join, sort the data points by the ’key’ in ascending order.
- Interfacing with The C extension (C module mykmeanssp): using the fit() method with passing the initial centroids, the datapoints and other
arguments, getting the final centroids that returned by fit() and outputting the results.


## 2. kmeansmodule.c:
A C extension containing the K-means algorithm implementation (appears in another repository called 'Kmeans Clustering').
Step 1 of the algorithm (finding the initial centroids) is replaced by the values obtained from the K-means++ algorithm implemented in kmeans_pp.py.
The final module (as seen in Python) is named mykmeanssp.
The module API provides a function called fit():
(a) The Function receives the initial centroids, datapoints and other necessary arguments.
(b) Skip step 1 from Kmeans algorithm and run Kmeans algorithm.
(c) Return the final centroids.

## 3. setup.py: 
The setup file which allows kmeans_pp.py to import mykmeanssp.

## Output:
• The first line will be the indices of the observations chosen by the K-means++ algorithm as the initial centroids. 
Observation’s index is given by the first column in each input file.
• The second line onwards will be the calculated final centroids from the K-means alogorithm, separated by a comma, such that each centroid is in a line of its own.

## Running:
To build the Python extension: 
```python3 setup.py build_ext --inplace```

For example, run : ```python3 kmeans_pp.py 3 100 0.01 input_1.txt input_2.txt```
*  Don’t compile the C module with gcc.

## Bonus file
This section covers involves working with matplotlib. The goal of this program is to demonstrate the use of the elbow method to determine the optimal number of clusters
for the k-means clustering.
The idea of the elbow method is to run k-means clustering with a range of values of k and for
each value of k calculate the inertia. Then, plot a line chart of the inertia for each corresponding
value of k. If the line chart looks like an arm, then the "elbow" on the arm is the value of k that is
the best.
This program is only produce an output elbow.png in the program folder.



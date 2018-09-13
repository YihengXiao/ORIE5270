import os
import sys

spark_home = os.environ.get('SPARK_HOME', None)
sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.10.7-src.zip'))
sys.path.insert(0, os.path.join(spark_home, 'python'))
exec(open(os.path.join(spark_home, 'python/pyspark/shell.py')).read())

import numpy as np
import pyspark as ps
# import math
import glob
import re
import time


def save_results(centroids):
    """
    param: centriods, a list containing final centroids
    return: a textfile 
    """
    file = open("final_centroids.txt", "w")
    for i in centroids:
        pt = ""
        for val in i:
            pt += str(val) + " "
        file.write(pt + "\n")
    file.close()
    return 1


def k_means(data_file, centroids_file, MAX_ITER = 100, tol = 0.001):
    """
    :param data_file: path of raw data
    :param centroids_file: path of initial guess of centroids
    :param MAX_ITER: maximum iterations
    :param tol: tolerance of convergence
    :return:
    """

    # Load the data
    data = sc.textFile(data_file).map(lambda line: np.array([float(x) for x in line.split(' ')])).cache()
    # load intial centriods and save it as a list
    centroids_0 = sc.textFile(centroids_file).map(lambda line: np.array([float(x) for x in line.split(' ')])).collect()

    for i in range(MAX_ITER):
        
        # cluster each point
        pt_in_group = data.map(lambda m: (np.argmin([np.linalg.norm(m - n) for n in centroids_0]), (m, 1)))
        # compute new centroids
        centroids_1 = pt_in_group.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1])).sortByKey()
        centroids_1 = centroids_1.map(lambda x: x[1][0]/x[1][1]).collect()
        
        # err, compute the difference between consecutive steps (measured by l_2 norm).
        err = np.linalg.norm(np.array(centroids_1) - np.array(centroids_0))
        print(str(i)+","+str(err))
        
        # if err < tol, converge
        if err <= tol:
            print(str(i+1)+" iterations.\n"+"Error: "+str(err)+"Centroids:\n")
            save_results(centroids_1)
            break
        centroids_0 = centroids_1[:]
        if i == MAX_ITER - 1:
            save_results(centroids_1)
    return 1

if __name__ == '__main__':

    # sc = ps.SparkContext(appName="py_kmeans")
    sc = ps.SparkContext.getOrCreate()
    data_file = './data.txt'
    centroids_file = './c1.txt'
    k_means(data_file, centroids_file, MAX_ITER=100, tol=0)
    sc.stop()

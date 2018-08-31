import os
import sys
# spark_home = os.environ.get('SPARK_HOME', None)
# sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.10.7-src.zip'))
# sys.path.insert(0, os.path.join(spark_home, 'python'))
# exec(open(os.path.join(spark_home, 'python/pyspark/shell.py')).read())
import pandas as pd
import numpy as np
import pyspark as ps
import time


def multiply(A, v):
    """
    param: A, path of textfile of matrix A
    param: v, path of textfile of vector v
    return: res, a vector = Av
    """
    
    matrices = sc.textFile(A)
    vectors = sc.textFile(v)
    """
    input 1: matrix.txt
    row idx, entry 0, entry 1, ..., entry n
    0, a00, a00, ..., a0n
    ...
    input 2:vector.txt
    entry 0
    entry 1
    ...
    """
    matrix = matrices.map(lambda l: [float(x) for x in l.split(",")]).cache()  # read matrix A, split each entry by ','
    vector = vectors.map(lambda l: [float(x) for x in l.split(",")]).cache()   # read vector v, split each entry by ','

    matrix = matrix.map(lambda l: (l[0], [(l[i], i-1) for i in range(1, len(l))]))  # add index to each entry of A
    matrix = matrix.flatMap(lambda l: ((l[1][i][1], (l[0], l[1][i][0])) for i in range(len(l[1])))) 
    vector = vector.flatMap(lambda l: [(i, l[i]) for i in range(len(l))])

    res = matrix.join(vector).map(lambda l: (l[1][0][0], l[1][0][1]*l[1][1]))  # multiply entry from matrix and vector
    res = res.reduceByKey(lambda x,y: x+y).sortBy(lambda x: x[0]).map(lambda x: x[1]).collect()  # compute Av

    return res

if __name__ == '__main__':

    n1=10
    n2=10
    a = pd.DataFrame(data = np.array(range(n1*n2)).reshape((n1,n2)),index=range(n1))
    b = pd.DataFrame(data = np.array(range(1,n1+1)).reshape((1,n1)))
    a.to_csv("matrix.txt",sep=',',header=False)
    b.to_csv("vector.txt",index=None,sep=',',header=False)

    sc = ps.SparkContext.getOrCreate()

    start = time.clock()
    A = "./matrix.txt"
    v = "./vector.txt"
    print(multiply(A,v))
    elapsed = (time.clock() - start)
    print(elapsed)
    sc.stop()
    ## Compare with np.dot()
    start = time.clock()
    print(np.dot(np.array(range(n1*n2)).reshape((n1,n2)),np.array(range(1,n1+1)).reshape((n1,1))))
    elapsed = (time.clock() - start)
    print(elapsed)

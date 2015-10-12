"""
Applications for cluster algorithms
@Author: Henry Wan
"""
import alg_cluster
import user40_qqmi7jGqbVyG2vK_0 as cl
import random
import simpleplot
import time
import codeskulptor

codeskulptor.set_timeout(100)

#########################################
def gen_random_clusters(num_clusters):
    """
    Generate random cluster
    """
    ans = []
    for _ in range(num_clusters):
        ans.append(alg_cluster.Cluster(set([]), random.randrange(-1, 1),
                               random.randrange(-1, 1), 0, 0))
    return ans

data1 = []
data2 = []
for i in range(2, 201):
    cluster_set = gen_random_clusters(i)
    time0 = time.time()
    cl.slow_closest_pair(cluster_set)
    time1 = time.time()
    cl.fast_closest_pair(cluster_set)
    time2 = time.time()
    data1.append((i, time1 - time0))
    data2.append((i, time2 - time1))

simpleplot.plot_lines('Running Time Analysis', 400, 300, 'num of clusters', 'time usage', [data1, data2], 
                      False, ['slow_closest_pair', 'fast_closest_pair'])
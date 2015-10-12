"""
Assess the quality of hierarchical clustering and k mean clustering
@author: Henry Wan
"""
import math
import random
import urllib2
import simpleplot
import alg_cluster
import user40_qqmi7jGqbVyG2vK_0 as cl
import codeskulptor

codeskulptor.set_timeout(1000)

###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
                
def compute_distortion(cluster_list, datatable):
    """
    Computer the distortion of a clustering algorithms
    """
    ans = 0
    for cluster in cluster_list:
        ans += cluster.cluster_error(datatable)
    return ans

data_table1 = load_data_table(DATA_896_URL)
data_table2 = load_data_table(DATA_896_URL)
    
singleton_list1 = []
singleton_list2 = []
for line in data_table1:
    singleton_list1.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

for line in data_table2:
    singleton_list2.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

data1 = []
data2 = []
cluster_list1 = cl.hierarchical_clustering(singleton_list1, 21)
    
for i in range(20, 5, -1):
    new_pair = cl.fast_closest_pair(cluster_list1)
    cluster_list1[new_pair[1]].merge_clusters(cluster_list1[new_pair[2]])
    cluster_list1.remove(cluster_list1[new_pair[2]])     
    
    cluster_list2 = cl.kmeans_clustering(singleton_list2, i, 1)
    data1.append((i, compute_distortion(cluster_list1, data_table1)))
    data2.append((i, compute_distortion(cluster_list2, data_table2)))
        
simpleplot.plot_lines('Quality Analysis - 896', 800, 600, 'num of clusters', 'Total Error', [data1, data2], 
                  False, ['hierarchical_clustering', 'kmeans_clustering'])

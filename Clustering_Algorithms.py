"""
Project 3: implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
@Author: Henry Wan
"""

import math
import alg_cluster

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))

def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    ans = (float("inf"), -1, -1)
    for index_i in range(len(cluster_list)):
        for index_j in range(len(cluster_list)):
            if (index_j != index_i):
                new_dis = pair_distance(cluster_list, index_i, index_j)
                if (new_dis[0] < ans[0]):
                    ans = new_dis          
    return ans

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    length = len(cluster_list)
    
    if (length <= 3):
        return slow_closest_pair(cluster_list)
    else:
        ans = (float("inf"), -1, -1)
        mid_cut = int(math.floor(length / 2))
        cluster_left = cluster_list[:mid_cut]
        cluster_right = cluster_list[mid_cut:]
        dis_left = fast_closest_pair(cluster_left)
        dis_right = fast_closest_pair(cluster_right)
        if (dis_left[0] < dis_right[0]):
            ans = dis_left
        else:
            ans = (dis_right[0], dis_right[1] + len(cluster_left), dis_right[2] + len(cluster_left))

        mid = (cluster_list[mid_cut].horiz_center() + cluster_list[mid_cut - 1].horiz_center()) / 2
        mid_ans = closest_pair_strip(cluster_list, mid, ans[0])
        if (mid_ans[0] < ans[0]):
            ans = mid_ans
        return ans

def closest_pair_strip(cluster_list, mid, dis):
    """
    Return a tuple (distance, idx1, ind2) where distance is the smallest pairwise
    distance of points in cluster_list whose horizontal coordinates are within dis
    from mid
    """
    new_list = []
    for idx in range(len(cluster_list)):
        if (abs(cluster_list[idx].horiz_center() - mid) < dis):
            new_list.append(cluster_list[idx])
    new_list.sort(key = lambda cluster: cluster.vert_center())
    
    ans = (float("inf"), -1, -1)
    if (len(new_list) > 0):
        for idx_i in range(len(new_list) - 1):
            for idx_j in range(idx_i + 1, min(idx_i + 4, len(new_list))):
                new_dis = pair_distance(new_list, idx_i, idx_j)
                if (new_dis[0] < ans[0]):
                    ans = new_dis
        final = list(ans)
        idx_1 = search(new_list[final[1]], cluster_list)
        idx_2 = search(new_list[final[2]], cluster_list)
        final[1] = min(idx_1, idx_2)
        final[2] = max(idx_1, idx_2)
    else:
        return ans
    return tuple(final)           

def search(cluster_a, cluster_list):
    """
    Search the position of a cluster in a cluster list
    """
    for idx in range(len(cluster_list)):
        if (cluster_list[idx] == cluster_a):
            return idx

######################################################################
# Code for hierarchical clustering

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while (len(cluster_list) > num_clusters):
        new_pair = fast_closest_pair(cluster_list)
        cluster_list[new_pair[1]].merge_clusters(cluster_list[new_pair[2]])
        cluster_list.remove(cluster_list[new_pair[2]])   
    return cluster_list

######################################################################
# Code for k-means clustering
    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    center_list = sorted(cluster_list,
              key=lambda c: c.total_population())[-num_clusters:]
    center_list = [c.copy() for c in center_list]

    for dummy in range(num_iterations):
        set_list = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for _ in range(num_clusters)]

        for idx_j in range(len(cluster_list)):
            dis = float("inf")
            center_choice = -1
            for idx_i in range(len(center_list)):
                new_dis = cluster_list[idx_j].distance(center_list[idx_i])
                if (new_dis < dis):
                    dis = new_dis
                    center_choice = idx_i
            set_list[center_choice].merge_clusters(cluster_list[idx_j])
            
        for idx_f in range(num_clusters):
            center_list[idx_f] = set_list[idx_f]
            
    return set_list
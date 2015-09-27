"""
Application portion of Module 2
@Author: Henry Wan
"""
# Set system recursion limit
import sys
sys.setrecursionlimit(10000)

# general imports
import urllib2
import random
import time
import math
from collections import deque

# Desktop imports
import matplotlib.pyplot as plt

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree in a faster way
    """
    length = len(list(ugraph.keys()))
    deg_set = [[] for k in range(length)]
    for i in range(length):
        d = len(list(ugraph[i]))
        deg_set[d].append(i)

    L = [[] for k in range(length)]
    i = 0
    for k in range(length - 1, -1, -1):
        while (deg_set[k] != []):
            u = random.choice(deg_set[k])
            deg_set[k].remove(u)
            for item in ugraph[u]:
                d = len(list(ugraph[item]))
                deg_set[d].remove(item)
                deg_set[d - 1].append(item)
            L[i] = u
            i += 1
            delete_node(ugraph, u)
    return L        
    
def random_order(ugraph):
    order = [key for key in ugraph.keys()]
    random.shuffle(order)
    return order

def compute_edge(graph):
    """
    Compute the edge of undirected graph
    """
    count = 0
    for item in graph.keys():
        for dummy in graph[item]:
            count += 1
    return count / 2
    
##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph
 
##########################################################
# Code for undirected ER graph
def make_complete_graph(num_nodes, probability):
    """
    Takes the number of nodes num_nodes and returns a dictionary 
    corresponding to a complete undirected graph with the specified 
    number of nodes. A complete graph contains all possible edges 
    subject to the restriction that self-loops are not allowed.
    """
    if (num_nodes == 1):
        return {0:set([])}
    else:
        next_graph = make_complete_graph(num_nodes - 1, probability)
        node_b_set = set([])
        for node_a in range(num_nodes - 1):
            if (random.random() <= probability):
                node_b_set.add(node_a)
                next_graph[node_a].add(num_nodes - 1)
        dic = {num_nodes - 1: node_b_set}
        next_graph.update(dic)
        return next_graph

##########################################################
# Code for undirected UPA graph
def upa_graph(node_num, m):
    """
    Compute an UPA graph, where 1<= m <= node_num
    """
    graph = make_complete_graph(m, 1)
    pbt_list = [node for node in range(m) for dummy in range(m)]
    for node_a in range(m, node_num):
        # Select m nodes to connect
        new_a = set()
        new_b = []
        for dummy in range(m):
            new_a.add(random.choice(pbt_list))
        for item in new_a:
            graph[item].add(node_a)
            new_b.append(node_a)
            new_b.append(item)
        pbt_list.extend(new_b)
        graph[node_a] = new_a
    return graph

##########################################################
# Other helper codes
def bfs_visited(ugraph, start_node):
    """
    Take undirected graph and source node as input
    output the set of all nodes visited by the algorithm
    """
    queue = deque([])
    visited = [start_node]
    queue.append(start_node)
    while (len(queue) != 0):
        next_node = queue.popleft()
        for item in ugraph[next_node]:
            if item not in visited:
                visited.append(item)
                queue.append(item)
    visited = set(visited)
    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, 
    where each set consists of all the nodes (and nothing else) 
    in a connected component
    """
    remain_nodes = set(ugraph.keys())
    result = []
    while (len(remain_nodes) != 0):
        next_node = remain_nodes.pop()
        node_set = bfs_visited(ugraph, next_node)
        result.append(node_set)
        for item in node_set:
            remain_nodes.discard(item)
    return result

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size 
    (an integer) of the largest connected component in ugraph
    """
    result = cc_visited(ugraph)
    max_num = 0
    for item in result:
        length = len(item)
        if (length > max_num):
            max_num = length
    return max_num

def compute_resilience(ugraph, attack_order):
    """
    The function should return a list whose k+1th entry is the 
    size of the largest connected component in the graph after 
    the removal of the first k nodes in attack_order. The first 
    entry (indexed by zero) is the size of the largest connected 
    component in the original graph.
    """
    result = []
    result.append(largest_cc_size(ugraph))
    keys = ugraph.keys()
    for item in attack_order:
        keys.remove(item)
        for key in keys:
            ugraph[key].discard(item)
        ugraph.pop(item)
        result.append(largest_cc_size(ugraph))
    return result

##########################################################
# Plotting three graphs' resilience
def plot_example():
    """
    Ploting three graphs' resilience
    """
    xvals = [num for num in range(1240)]
    
    plt.plot(xvals, res1, '-b', label='Computer network')
    plt.plot(xvals, res2, '-r', label='ER graphs')
    plt.plot(xvals, res3, '-g', label='UPA graphs')
    
    plt.legend(loc='upper right')
    plt.ylabel('Largeset component in network')
    plt.xlabel('Counts of continuous network attacks')
    plt.title('Network Resilience Analysis')
    plt.show()

graph1 = load_graph(NETWORK_URL)
graph2 = make_complete_graph(1239, 0.004)
graph3 = upa_graph(1239, 2)

res1 = compute_resilience(graph1, targeted_order(graph1))
res2 = compute_resilience(graph2, targeted_order(graph2))
res3 = compute_resilience(graph3, targeted_order(graph3))

plot_example()

##########################################################
# Plotting the running time of two functions - fast_order and targeted_order
def plot_example2():
    """
    Ploting three graphs' resilience
    """
    xvals = [num for num in range(10, 1000, 10)]
    
    plt.plot(xvals, timelist1, '-b', label='fast_order')
    plt.plot(xvals, timelist2, '-r', label='targeted_order')
    
    plt.legend(loc='upper right')
    plt.ylabel('Running time')
    plt.xlabel('Number of nodes')
    plt.title('Running time Analysis')
    plt.show()

#timelist1 = []
#timelist2 = []
#for n in range(10, 1000, 10):
#    start1 = time.time()
#    graph = upa_graph(n, 5)
#    fast_order(graph)
#    end1 = time.time()
#    timelist1.append(end1 - start1)
#    
#    start2 = time.time()
#    graph = upa_graph(n, 5)
#    targeted_order(graph)
#    end2 = time.time()
#    timelist2.append(end2 - start2)
    
#plot_example2()
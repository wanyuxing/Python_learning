"""
DPA graph - Henry Wan.
"""

# general imports
import math
import random
import matplotlib.pyplot as plt

STANDARD = True
LOGLOG = False

def dpa_graph(node_num, m):
    """
    Compute an DPA graph, where 1<= m <= node_num
    """
    graph = make_complete_graph(m)
    pbt_list = [node for node in range(m) for dummy in range(m)]
    for node_a in range(m, node_num):
        # Select m nodes to connect
        new_a = set()
        new_b = []
        for dummy in range(m):
            new_a.add(random.choice(pbt_list))
        for dummy in new_a:
            new_b.append(node_a)
        pbt_list.extend(new_a)
        pbt_list.extend(new_b)
        graph[node_a] = new_a
    return graph

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary 
    corresponding to a complete directed graph with the specified 
    number of nodes. A complete graph contains all possible edges 
    subject to the restriction that self-loops are not allowed.
    """
    graph = {}
    if (num_nodes <= 0):
        return graph
    else:
        for node_a in range(num_nodes):
            node_b_set = set([])
            for node_b in range(num_nodes):
                node_b_set.add(node_b)
            node_b_set.discard(node_a)
            dic = {node_a: node_b_set}
            graph.update(dic)
        return graph
    
def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) 
    and computes the in-degrees for the nodes in the graph.
    """
    graph = {}
    for node in digraph.keys():
        graph[node] = 0
    for node_a in digraph.keys():
        for node_b in digraph.get(node_a):
            graph[node_b] += 1
    return graph

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) 
    and computes the unnormalized distribution of the in-degrees 
    of the graph.
    """
    graph = {}
    graph_in_deg = compute_in_degrees(digraph)
    for node in set(graph_in_deg.values()):
        graph[node] = 0
    for node_a in graph_in_deg.keys():
        graph[graph_in_deg.get(node_a)] += 1
    return graph

graph = in_degree_distribution(dpa_graph(27770, 13))
plt.loglog(graph.keys(), graph.values(), basex = 2, basey = 2)
plt.axis([0 5000, 0, 5000])
plt.ylabel('Count')
plt.xlabel('In-degree number')
plt.title('DPA Graph')
plt.show()


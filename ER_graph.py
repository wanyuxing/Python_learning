"""
ER graph - Henry Wan. This program can only run
on www.codeskulptor.org
"""

# general imports
import simpleplot
import math
import random

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)

STANDARD = True
LOGLOG = False

def er_graph(node_num, p):
    """
    Compute an ER graph
    """
    graph = {}
    for node_a in range(node_num):
        new = set([])
        for node_b in range(node_num):
            if (node_b != node_a):
                if (random.random() < p):
                    new.update(set([node_b]))
        graph[node_a] = new
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

def log_graph(digraph):
    """
    Convert a graph into log-graph
    """
    graph = {}
    for node in digraph.keys():
        if (node != 0):
            graph[math.log(node)] = math.log(digraph[node])
    return graph

graph = in_degree_distribution(er_graph(600, 0.7))
simpleplot.plot_lines("ER Graph", 600, 600, 
                      "input", "counter", [graph])





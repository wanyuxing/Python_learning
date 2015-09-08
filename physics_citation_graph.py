"""
Analyse physics citation graph - Henry Wan. This program can only run
on www.codeskulptor.org
"""

# general imports
import urllib2
import simpleplot
import math

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)

STANDARD = True
LOGLOG = False
CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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
         
citation_graph = load_graph(CITATION_URL)
graph = log_graph(in_degree_distribution(citation_graph))

simpleplot.plot_lines("Physics Citation Graph", 600, 600, 
                      "input", "counter", [graph])





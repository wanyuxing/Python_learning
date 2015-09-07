"""
Degree distributions for graphs, there are 3 contant graphs represented
by dictionary
"""
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 
             4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 
             3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 
             7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

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
    graph = {node: 0 for node in digraph.keys()}
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
    graph_in_deg = compute_in_degrees(digraph)
    graph = {node: 0 for node in set(graph_in_deg.values())}
    for node_a in graph_in_deg.keys():
        graph[graph_in_deg.get(node_a)] += 1
    return graph
        

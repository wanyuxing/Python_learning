"""
Breadth-first search
@author: henrylyc
"""
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 
             4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 
             3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 
             7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}
             
from collections import deque

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
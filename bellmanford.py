import pdb
from collections import OrderedDict

"""
The Bellman-Ford algorithm
Graph API:
    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[u][v] gives weight of edge (u, v)
"""

# Step 1: For each node prepare the destination and predecessor
class BellmanFord(object):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.d = OrderedDict() # Stands for destination
        self.p = OrderedDict() # Stands for predecessor
        for node in self.graph:
            self.d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
            self.p[node] = None
            self.d[source] = 0 # For the source we know how to reach
    def relax(self, node, neighbour):
        # If the distance between the node and the neighbour is lower than the one I have now
        if self.d[neighbour] > self.d[node] + self.graph[node][neighbour]:
            # Record this lower distance
            self.d[neighbour]  = self.d[node] + self.graph[node][neighbour]
            self.p[neighbour] = node
    def run(self):
        for i in range(len(self.graph)-1): #Run this until is converges
            for u in self.graph:
                for v in self.graph[u]: #For each neighbour of u
                    self.relax(u, v) #Lets relax it

        # Step 3: check for negative-weight cycles
        negative_cycles = []
        for u in self.graph:
            for v in self.graph[u]:
                if self.d[v] > self.d[u] + self.graph[u][v]:
                    negative_cycles.append(v)
                    self.p[v] = u
        negative_cycle_lists = []
        for i in negative_cycles:
            j = i
            my_list=[]
            while True:
                if j in my_list:
                    my_list.insert(0, j)
                    break
                my_list.insert(0, j)
                j = self.p[j]
            negative_cycle_lists.append(my_list)
        return self.d, self.p, negative_cycle_lists


def test():
    graph = {
        'a': {'b': -1, 'c':  4},
        'b': {'c':  3, 'd':  2, 'e':  2},
        'c': {},
        'd': {'b':  1, 'c':  5},
        'e': {'d': -3}
        }

    bf = BellmanFord(graph, 'a')
    d, p, negative_cycle_lists = bf.run()

    assert d == {
        'a':  0,
        'b': -1,
        'c':  2,
        'd': -2,
        'e':  1
        }

    assert p == {
        'a': None,
        'b': 'a',
        'c': 'b',
        'd': 'e',
        'e': 'b'
        }

if __name__ == '__main__': test()

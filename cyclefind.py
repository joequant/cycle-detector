#!/usr/bin/python3

import sys

def visited(node, path):
    return node in path

class CycleFind(object):
    def __init__(self, graph, source, **kwargs):
        self.graph = graph
        self.source = source
        self.cycles = []
        self.edges, self.weights = self.getEdges(graph)
        self.cyclelimit = kwargs.get('cyclelimit', None)
        if self.cyclelimit is not None:
            self.cyclelimit = int(self.cyclelimit)
    def run(self):
        paths = []
        for node in self.source:
            self.findNewCycles([node])
        return self.cycles
    def getEdges(self, graph):
        retval = ([], {})
        for ik, iv in graph.items():
            for jk, jv in iv.items():
                retval[0].append((ik, jk))
                retval[1][(ik, jk)] = jv
        return retval
    def findNewCycles(self, path):
        start_node = path[-1]
        next_node= None
        sub = []
        if self.cyclelimit is not None and \
               len(path) > self.cyclelimit:
            return
        #visit each edge and each node of each edge
        for edge in self.edges:
            node1, node2 = edge
            if node1 == start_node:
                next_node = node2
                # check if there is a chord with a shorter path
                weight = self.weights[edge]
                shorter_path = False
                for i1, i2 in zip(path[-2::-1], path[::-1]):
                    weight += self.weights[(i1, i2)]
                    if (i1, next_node) in self.edges and \
                           self.weights[(i1, next_node)] < weight:
                        shorter_path = True
                        break
                if shorter_path:
                    continue
                if not visited(next_node, path):
                    # neighbor node not on path yet
                    sub = list(path)
                    sub.append(next_node)
                    # explore extended path
                    self.findNewCycles(sub);
                elif len(path) > 2  and next_node in path:
                    # cycle found
                    p = self.rotate_to_smallest(path, next_node);
                    if self.isNew(p):
                        self.cycles.append(p)
    def filter_negative(self, cycles):
        negative_cycles = []
        for i in cycles:
            total = 0.0
            path = list(i)
            path.append(i[0])
            for j in zip(path, path[1::]):
                total -= self.graph[j[0]][j[1]]
            if total > 0.0:
                negative_cycles.append(i)
        return negative_cycles
#  rotate cycle path such that it begins with the smallest node
    def rotate_to_smallest(self, path, next_node):
        i = path.index(next_node)
        path = path[i::]
        for i in self.source:
            if i in path:
                n = path.index(i)
                return path[n:]+path[:n]
        n = path.index(min(path))
        return path[n:]+path[:n]
    def isNew(self, path):
        return not path in self.cycles

if __name__ == '__main__':
    from cycledetect import CycleDetect
    cd = CycleDetect()
    for i in sys.argv[1:]:
        with open(i, 'r') as csvfile:
            print("Loading: ", i)
            cd.load([csvfile])
    cf = CycleFind(cd.graph, cd.origins, cyclelimit=cd.cyclelimit)
    cycles = cf.run()
    negative_cycles = cf.filter_negative(cycles)
    for i in cycles:
        print (" -> " .join(i))

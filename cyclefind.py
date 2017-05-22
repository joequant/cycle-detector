#!/usr/bin/python3

cycles = []

from cycledetect import CycleDetect
import sys




def visited(node, path):
    return node in path

class CycleFind(object):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.cycles = []
        self.edges = self.getEdges(graph)
    def run(self):
        paths = []
        for node in self.source:
            self.findNewCycles([node])
            for cy in cycles:
                paths.append([str(node) for node in cy])
        return paths
    def getEdges(self, graph):
        retval = []
        for ik, iv in graph.items():
            for jk, jv in iv.items():
                retval.append([ik, jk])
        return retval
    def findNewCycles(self, path):
        start_node = path[-1]
        next_node= None
        sub = []
        #visit each edge and each node of each edge
        for edge in self.edges:
            node1, node2 = edge
            if node1 == start_node:
                next_node = node2
                if not visited(next_node, path):
                    # neighbor node not on path yet
                    sub = list(path)
                    sub.append(next_node)
                    # explore extended path
                    self.findNewCycles(sub);
                elif len(path) > 2  and next_node == path[0]:
                    # cycle found
                    p = self.rotate_to_smallest(path);
                    if self.isNew(p):
                        cycles.append(p)
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
    def rotate_to_smallest(self, path):
        for i in self.source:
            if i in path:
                n = path.index(i)
                return path[n:]+path[:n]
        n = path.index(min(path))
        return path[n:]+path[:n]
    def invert(self, path):
        return self.rotate_to_smallest(path[::-1])
    def isNew(self, path):
        return not path in self.cycles

if __name__ == '__main__':
    cd = CycleDetect()
    with open(sys.argv[1], 'r') as csvfile:
        cd.load(csvfile)
        cf = CycleFind(cd.graph, cd.origins)
        cycles = cf.run()
        negative_cycles = cf.filter_negative(cycles)
        for i in negative_cycles:
            print (" -> " .join(i))

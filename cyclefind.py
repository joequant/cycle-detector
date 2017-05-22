#!/usr/bin/python3

cycles = []

from cycledetect import CycleDetect
import sys

def main():
    global cycles
    cd = CycleDetect()
    with open(sys.argv[1], 'r') as csvfile:
        cd.load(csvfile)
    edges = getEdges(cd.graph)
    print(edges)
    for node in cd.origins:
        print("node: ", node)
        findNewCycles(edges, [node])
    for cy in cycles:
        path = [str(node) for node in cy]
        s = ",".join(path)
        print(s)

def getEdges(graph):
    retval = []
    for ik, iv in graph.items():
        for jk, jv in iv.items():
            retval.append([ik, jk])
    return retval

def findNewCycles(edges, path):
    start_node = path[0]
    next_node= None
    sub = []
    #visit each edge and each node of each edge
    for edge in edges:
        node1, node2 = edge
        if node1 == start_node:
            next_node = node2
            if not visited(next_node, path):
                # neighbor node not on path yet
                sub = [next_node]
                sub.extend(path)
                # explore extended path
                findNewCycles(edges, sub);
            elif len(path) > 2  and next_node == path[-1]:
                # cycle found
                p = rotate_to_smallest(path);
                inv = invert(p)
                if isNew(p) and isNew(inv):
                    cycles.append(p)

def invert(path):
    return rotate_to_smallest(path[::-1])

#  rotate cycle path such that it begins with the smallest node
def rotate_to_smallest(path):
    n = path.index(min(path))
    return path[n:]+path[:n]

def isNew(path):
    return not path in cycles

def visited(node, path):
    return node in path

main()

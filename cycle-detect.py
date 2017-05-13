#!/bin/python3
import bellmanford
import csv
import sys
import math
graph = {}
origins = []

def add_link(f,t,v):
    if f not in graph:
        graph[f] = {}
    graph[f][t] = v

with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) == 0:
            continue
        format = row[0]
        if row[0][0] == '#':
            continue
        if format == 'origin':
            f = row[1]
            origins.append(f)
        if format == 'link':
            f = row[1]
            t = row[2]
            v = float(row[3])
            add_link(f,t,v)
        elif format == 'node':
            f = row[1]
            if f not in graph:
                graph[f] = {}
        elif format == 'bid-ask':
            f = row[1]
            t = row[2]
            b = math.log(float(row[3]))
            a = math.log(float(row[4]))
            add_link(f,t,-b)
            add_link(t,f,a)
        elif format == 'fee':
            f = row[1]
            t = row[2]
            v = math.log(1.0 - float(row[3]))
            add_link(f,t,-v)
            add_link(t,f,-v)

for node in origins:
    d, p, negative_cycles, negative_cycle_lists = \
       bellmanford.bellman_ford(graph, node)
    print (d, p, negative_cycles, negative_cycle_lists)

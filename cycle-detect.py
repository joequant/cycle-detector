#!/bin/python3
import bellmanford
import csv
import sys
import math
from collections import OrderedDict
graph = OrderedDict()
origins = []
delay = OrderedDict()
limit = OrderedDict()

def add_link(f,t,v,d=None,l=None):
    if f not in graph:
        graph[f] = {}
    if f not in delay:
        delay[f] = {}
    if f not in limit:
        limit[f] = {}
    graph[f][t] = v
    if d is not None:
        delay[f][t] = d
    if l is not None:
        limit[f][t] = l

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
            if len(row) > 5 and row[5] != "":
                d = float(row[5])
            else:
                d = None
            if len(row) > 6 and row[6] != "":
                l = float(row[6])
            else:
                l = None
            add_link(f,t,-b, d, l)
            add_link(t,f,a, d, l)
        elif format == 'fee':
            f = row[1]
            t = row[2]
            v = math.log(1.0 - float(row[3]))
            if len(row) > 4 and row[4] != "":
                d = float(row[4])
            else:
                d = None
            if len(row) > 5 and row[5] != "":
                l = float(row[5])
            else:
                l = None
            add_link(f,t,-v, d, l)
            add_link(t,f,-v, d, l)

for node in origins:
    bf = bellmanford.BellmanFord(graph, node)
    d, p, negative_cycle_lists = bf.run()
    for i in negative_cycle_lists:
        print (" -> ".join(i))
        total = 0.0
        d = 0.0
        l = None
        for j in zip(i, i[1::]):
            total -= graph[j[0]][j[1]]
            d += delay[j[0]].get(j[1], 0.0)
            new_limit = limit[j[0]].get(j[1],None)
            if new_limit is not None:
                if l is None or new_limit < l:
                    l = new_limit
        print ("Expected return:", math.exp(total))
        print ("Delay:", d)
        if l is not None:
            print("Limit: ", l)
        print()

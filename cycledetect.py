#!/bin/python3
import bellmanford
import csv
import sys
import math
from collections import OrderedDict

class CycleDetect(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.graph = OrderedDict()
        self.origins = []
        self.delay = OrderedDict()
        self.limit = OrderedDict()

    def add_link(self, f,t,v,d=None,l=None):
        if f not in self.graph:
            self.graph[f] = {}
        if f not in self.delay:
            self.delay[f] = {}
        if f not in self.limit:
            self.limit[f] = {}
        self.graph[f][t] = v
        if d is not None:
            self.delay[f][t] = d
        if l is not None:
            self.limit[f][t] = l

    def load(self, fp):
        self.reset()
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) == 0:
                continue
            format = row[0]
            if row[0][0] == '#':
                continue
            if format == 'origin':
                f = row[1]
                self.origins.append(f)
            if format == 'link':
                f = row[1]
                t = row[2]
                v = float(row[3])
                self.add_link(f,t,v)
            elif format == 'node':
                f = row[1]
                if f not in self.graph:
                    self.graph[f] = {}
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
                self.add_link(f,t,-b, d, l)
                self.add_link(t,f,a, d, l)
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
                self.add_link(f,t,-v, d, l)
                self.add_link(t,f,-v, d, l)

    def run(self, fp=None):
        if fp is not None:
            self.load(fp)
        retval = []
        for node in self.origins:
            bf = bellmanford.BellmanFord(self.graph, node)
            d, p, negative_cycle_lists = bf.run()
            for i in negative_cycle_lists:
                total = 0.0
                d = 0.0
                l = None
                for j in zip(i, i[1::]):
                    total -= self.graph[j[0]][j[1]]
                    d += self.delay[j[0]].get(j[1], 0.0)
                    new_limit = self.limit[j[0]].get(j[1],None)
                    if new_limit is not None:
                        if l is None or new_limit < l:
                            l = new_limit
                retval.append([i, math.exp(total), d, l])
        return retval

    def format(self, cycles):
        retval = ''
        for i in cycles:
            retval += " -> ".join(i[0]) + "\n"
            retval += "Expected return: " + str(i[1]) + "\n"
            retval += "Delay: " + str(i[2]) + "\n"
            if i[3] is not None:
                retval += "Limit: " + str(i[3]) + "\n"
            retval += "\n"
        return retval

if __name__ == '__main__':
    cd = CycleDetect()
    with open(sys.argv[1], 'r') as csvfile:
        cycles = cd.run(csvfile)
        print(cd.format(cycles))

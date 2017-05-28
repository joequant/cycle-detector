#!/bin/python3
import csv
import sys
import math
from collections import OrderedDict
from graphviz import Digraph
from cyclefind import CycleFind

class CycleDetect(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.graph = OrderedDict()
        self.origins = []
        self.delay = OrderedDict()
        self.limit = OrderedDict()
        self.cyclelimit = None

    def add_link(self, f, t, v, d=None, l=None):
        if f not in self.graph:
            self.graph[f] = {}
        if f not in self.delay:
            self.delay[f] = {}
        if f not in self.limit:
            self.limit[f] = {}
        if t not in self.graph[f]:
            self.graph[f][t] = 0.0
        self.graph[f][t] += v
        if d is not None:
            if t not in self.delay[f]:
                self.delay[f][t] = 0.0
            self.delay[f][t] += d
        if l is not None:
            if t not in self.limit[f]:
                self.limit[f][t] = l
            else:
                self.limit[f][t] = min(self.limit[f][t], l)

    def load(self, fplist):
        tfee = []
        for fp in fplist:
            reader = csv.reader(fp, delimiter=',', quotechar='"')
            for row in reader:
                if len(row) == 0:
                    continue
                lformat = row[0]
                if len(row[0]) == 0 or row[0][0] == '#':
                    continue
                if lformat == 'origin':
                    f = row[1]
                    if f not in self.origins:
                        self.origins.append(f)
                if lformat == 'link':
                    f = row[1]
                    t = row[2]
                    v = float(row[3])
                    self.add_link(f, t, v)
                elif lformat == 'cycle-limit':
                    self.cyclelimit = int(row[1])
                elif lformat == 'node':
                    f = row[1]
                    if f not in self.graph:
                        self.graph[f] = {}
                elif lformat == 'bid-ask':
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
                    self.add_link(f, t, -b, d, l)
                    self.add_link(t, f, a, d, l)
                elif lformat == 'fee':
                    f = row[1]
                    t = row[2]
                    v = math.log(1.0 - float(row[3])/100.0)
                    if len(row) > 4 and row[4] != "":
                        d = float(row[4])
                    else:
                        d = None
                    if len(row) > 5 and row[5] != "":
                        l = float(row[5])
                    else:
                        l = None
                    self.add_link(f, t, -v, d, l)

    def graphviz(self, fp=None):
        if fp is not None:
            self.load(fp);
        nl = self.run()
        show = {}
        dot = Digraph(format='png')
        for ik, iv in self.graph.items():
            ikid = ik.replace(":", "__")
            dot.node(ikid, ik)
        for i in nl:
            i1 = i[0]
            for j in zip(i1, i1[1::]):
                ikid = j[0].replace(":", "__")
                jkid = j[1].replace(":", "__")
                if (ikid, jkid) not in show:
                    show[(ikid, jkid)] = True
                    dot.edge(ikid, jkid, color='red')
        for ik, iv in self.graph.items():
            for jk, jv in iv.items():
                ikid = ik.replace(":", "__")
                jkid = jk.replace(":", "__")
                if (ikid, jkid) not in show:
                    dot.edge(ikid, jkid)
        return dot.pipe()

    def run(self, fp=None):
        if fp is not None:
            self.load(fp)
        retval = []
        cf = CycleFind(self.graph, self.origins, cyclelimit=self.cyclelimit)
        cycles = cf.run()
        negative_cycle_lists = cf.filter_negative(cycles)
        for i in negative_cycle_lists:
            total = 0.0
            d = 0.0
            l = None
            i1 = list(i)
            i1.append(i[0])
            for j in zip(i1, i1[1::]):
                total -= self.graph[j[0]][j[1]]
                d += self.delay[j[0]].get(j[1], 0.0)
                new_limit = self.limit[j[0]].get(j[1], None)
                if new_limit is not None:
                    if l is None or new_limit < l:
                        l = new_limit
            retval.append([i1, math.exp(total), d, l])
        return retval

    def format(self, cycle_list, threshold = 0.0):
        retval = ''
        for i in cycle_list:
            percent = (i[1] - 1.0) * 100
            if percent > threshold:
                retval += " -> ".join(i[0]) + "\n"
                retval += "Expected return: " + str(percent) + "\n"
                retval += "Delay: " + str(i[2]) + "\n"
                if i[3] is not None:
                    retval += "Limit: " + str(i[3]) + "\n"
                retval += "\n"
        return retval

if __name__ == '__main__':
    cd = CycleDetect()
    for i in sys.argv[1:]:
        with open(i, 'r') as csvfile:
            print("Loading: ", i)
            cd.load([csvfile])
    cycles = cd.run()
    print(cd.format(cycles, 2))

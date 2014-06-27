#!/usr/bin/env python

import sys
from starbase import Connection
#from config import hbaseIP
from config import hbasePort

maxPlacesPerRect = 20

hbaseIP = '172.31.11.68'
hbasePort = 8080
c = Connection(hbaseIP, hbasePort)
t = c.table('osm')


def emitPlaces(k, p):
    # stdout
    print '%s\t%s' % (k, p)

    # hbase
    vals = {}
    for placeNum in range(len(p)):
        dk = 'p%d' % placeNum
        dv = p[placeNum]
        vals[dk] = dv
    if (vals != None):
        t.insert(k, {'p':vals})
    

def main():
    key = None
    lastKey = None
    places = []

    for line in sys.stdin:

        line = line.strip()
        key, place = line.split('\t', 1)

        if ((key != lastKey) & (lastKey != None)):
            emitPlaces(lastKey, places)
            places = []
            
        if (len(places) < maxPlacesPerRect):
            places.append(place)
                
        lastKey = key
                
    if key == lastKey:
        emitPlaces(key, places)


if __name__ == "__main__":
    main()

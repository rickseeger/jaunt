#!/usr/bin/env python

import sys

maxPlacesPerRect = 20
lastKey = None
places = []

for line in sys.stdin:

    line = line.strip()
    key, place = line.split('\t', 1)

    if ((key != lastKey) & (lastKey != None)):
        print '%s\t%s' % (lastKey, places)
        places = []

    if (len(places) < maxPlacesPerRect):
        places.append(place)

    lastKey = key
    
if key == lastKey:
    print '%s\t%s' % (key, places)

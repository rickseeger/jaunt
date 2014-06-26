#!/usr/bin/env python
import sys
import cStringIO
import re


# smallest square as (degrees * 10^3); 10 == 0.69 miles 
baseResolution = 10

# each level is twice the width of the previous
numLevels = 6

# OSM tag key/value pattern
kvPattern = re.compile('k="([^"]+)"\sv="([^"]+)"')

# OSM lat/long pattern
llPattern = re.compile('lat="([^"]+)"\slon="([^"]+)"')

# only keep these keys
keyFilter = [ 'name', 'amenity' ]


# return list of k/v pairs found
def process(val):
    dict = {}
    for line in val.splitlines():
        match = kvPattern.search(line)
        if ((match != None) and (match.lastindex == 2)):
            k = match.group(1)
            if any(k in f for f in keyFilter):
                dict[k] = match.group(2)
    return(dict)


def main():
    buff = None
    lat = None
    lon = None
    
    intext = False
    for line in sys.stdin:
        line = line.strip()
        
        if (line.startswith('<node')):
            
            # skip leaf nodes
            if (line.endswith('/>')):
                continue

            # node start
            else:
                match = llPattern.search(line)
                if ((match != None) and (match.lastindex == 2)):
                    lat = match.group(1)
                    lon = match.group(2)
                    intext = True
                    buff = cStringIO.StringIO()

        # node end
        elif line.startswith('</node>'):
            if (buff != None):
                intext = False
                val = buff.getvalue()
                buff.close()
                buff = None
                dict = process(val)
                if (len(dict) > 0):
                    
                    # for each rectangle size emit
                    # key: upper-left corner of rect and rect height in 10^3 degrees as (lat|lon|range)
                    # value: tuple (name, amenity, lat, lon)

        # node middle
        else:
            if intext:
                buff.write(line + '\n') 


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import sys
import cStringIO
import re
import math

# size of smallest rectangle as 1000 x degrees; 10 = 0.69 miles
baseSize = 10

# number of bounding box sizes, each level is double the width of previous 
numLevels = 6

# OSM tag key/value pattern
kvPattern = re.compile('k="([^"]+)"\sv="([^"]+)"')

# OSM lat/lon pattern
llPattern = re.compile('lat="([^"]+)"\slon="([^"]+)"')
keyFilter = [ 'name', 'amenity' ]


# return dict of k/v pairs found in tags
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
                    try:
                        lat = float(match.group(1))
                        lon = float(match.group(2))
                    except ValueError:
                        continue
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

                amenity = dict.get('amenity')
                name = dict.get('name')

                if ((amenity != None) & (name != None)):
                    
                    # emit kv for each rectangle size
                    for level in range(numLevels):

                        # key: lat,lon of upper left bbox + bbox size + amenity type
                        rectSize = math.pow(2,level) * baseSize
                        gridStep = float(1000/rectSize)
                        cornerLat = (math.floor(lat*gridStep)/gridStep) * 100.0
                        cornerLon = ((math.floor(lon*gridStep)/gridStep) + 180.0) * 100.0
                        key = '%.0f:%.0f:%04d:%s' % (cornerLat, cornerLon, rectSize, amenity)

                        # value: tuple (name, lat, lon)
                        value = lat, lon, name
                        print '%s\t%s' % (key, value)

        # node middle
        else:
            if intext:
                buff.write(line + '\n') 


if __name__ == '__main__':
    main()

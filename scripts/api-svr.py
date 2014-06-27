
import math
import json
import config
import pprint
from bottle import route, run, post, request, response, BaseRequest
from starbase import Connection

c = Connection(config.hbaseIP, config.hbasePort)
t = c.table('osm')


def makeJSON(lat,lon,a,t):
    json = '{\n\t"lat" : "%f",\n\t"lon" : "%f",\n\t"amenity" : "%s",\n\t"tilesize" : "%d"\n}' % (lat, lon, a, t)
    return(json)


@route('/')
def hello():

    # defaults
    lat = 37.426301
    lon = -122.141162
    amenity = 'restaurant'
    tilesize = 3
    example = makeJSON(lat, lon, amenity, tilesize)
    
    results = ''
    if (request.query.submit):
        results = request.query.json
        try:
            j = json.loads(request.query.json)
            lat = float(j['lat'])
            lon = float(j['lon'])
            amenity = str(j['amenity'])
            tilesize = int(j['tilesize'])
            example = makeJSON(lat, lon, amenity, tilesize)

        except:
            return('JSON failed to parse')

        # key: lat,lon of upper left bbox + bbox size + amenity type
        rectSize = math.pow(2,tilesize) * config.baseSize
        gridStep = float(1000/rectSize)
        cornerLat = (math.floor(lat*gridStep)/gridStep) * 100.0
        cornerLon = ((math.floor(lon*gridStep)/gridStep) + 180.0) * 100.0
        key = '%.0f:%.0f:%04d:%s' % (cornerLat, cornerLon, rectSize, amenity)
        results = '\nkey:\n' + key + '\n\n'
        
        # value: fetch from hbase
        dict = t.fetch(key)
        results += 'value:\n'
        pp = pprint.PrettyPrinter()
        results += pp.pformat(dict)


    else:
        results = 'None'


    # quick n dirty web page; todo: templates
    h = '<html><body><h1>Jaunt API</h1>'
    h = h + '<table cellspacing=10><tr><td align=left valign=top><form action="" method="get">'
    h = h + '<pre><b>REQUEST</b></pre><p><textarea rows=10 cols=40 name=json>' + example+ '</textarea><br>'
    h = h + '<input type=submit name=submit value=submit></form></td>'
    h = h + '<td valign=top><pre><b>RESPONSE</b><p>' + results + '</pre></td></tr></table></body></html>'

    return(h)

# spawn server
run(host=config.APIHost, port=config.APIPort)

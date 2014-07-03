#!/usr/bin/python
from flask import abort, Flask, json, jsonify, request, make_response
from starbase import Connection
from jsonschema import validate, ValidationError
import jauntlib
import config
import math

schema = {
    "type" : "object",
    "properties" : {
        "lat" : {"type" : "number"},
        "lon" : {"type" : "number"}, 
        "amenity" : {"type" : "string"},
        "tilesize" : {"type" : "number"},
       },
    }


app = Flask(__name__)
c = Connection(config.hbaseIP, config.hbasePort)
t = c.table('osm')

@app.route('/' + config.APIVersion + '/find', methods = ['POST'])
def findPlaces():

    if request.headers['Content-Type'] == 'application/json':

        try:
            j = request.json
            validate(j, schema)

        except ValidationError:
            abort(make_response('{ "error" : "Invalid JSON types" }', 400))

        try:
            lat = float(j['lat'])
            lon = float(j['lon'])
            amenity = str(j['amenity'])
            tilesize = int(j['tilesize'])

        except ValueError:
            abort(make_response('{ "error" : "JSON value conversion error" }', 400))

        tileWidth = math.pow(2,tilesize) * config.baseSize
        (cornerLat, cornerLon) = jauntlib.findTile(lat, lon, tileWidth)
        key = '%.0f:%.0f:%04d:%s' % (cornerLat, cornerLon, tileWidth, amenity)

        try:
            dict = t.fetch(key)
            response = json.dumps(dict)
            return response
        except:
            abort(make_response('{ "error" : "HBase get failed" }', 404))
    
    else:
        abort(make_response('{ "error" : "Unknown Content-Type" }', 400))


if __name__ == '__main__':
    app.run(host=config.APIHost, port=config.APIPort, debug = True)

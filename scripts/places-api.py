
# places-api.py
# implements an API against the Open Street Map dataabase

from bottle import route, run, post, request, response, BaseRequest
import json

# config
APIHost = '50.23.78.115'
APIPort = 5000
debug = True

# places request - return list of places along a route
# [debug: for now just return static JSON object]
@route('/v1/places', method=['GET', 'POST'])
def handleRequest():
    
    tmp = '\
{\
    "status" : "ok", \
    "places" : [{\
"name" : "Bob Dog Pizza",\
        "type" : "restaurant",\
        "lat" : "38.851726",\
        "lon" : "-120.019764"\
    },\
    {\
"name" : "Chevron",\
        "type" : "gas", \
        "lat" : "38.856177",\
        "lon" : "-120.013760"\
    },\
    {\
"name" : "Chevron Pollock Pines",\
        "type" : "gas",\
        "lat" : "38.760141",\
        "lon" : "-120.530486"\
    },\
    {\
"name" : "Sacramento Marriot Rancho Cordova",\
        "type" : "hotel",\
        "lat" : "38.607367",\
        "lon" : "-121.269188"\
    },\
    {\
"name" : "Hilton Garden Inn Folsom",\
        "type" : "hotel",\
        "lat" : "38.642115",\
        "lon" : "-121.189711"\
    }]\
}\
'
    return(tmp)

# spawn server
run(host=APIHost, port=APIPort)

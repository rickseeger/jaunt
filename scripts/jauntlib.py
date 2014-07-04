import requests

import config
import json
import math

# find NW coords of specific tile
def findTile(lat, lon, tileWidthDegrees):
    gridStep = float(1000/tileWidthDegrees)
    cornerLat = (math.floor(lat*gridStep)/gridStep) * 100.0
    cornerLon = ((math.floor(lon*gridStep)/gridStep) + 180.0) * 100.0
    return(cornerLat, cornerLon)


# great circle distance (CAVEAT: assumes a spherical Earth)
def gcDist(lat0, lon0, lat1, lon1):
    earthRadius = 3959
    rlat0 = radians(lat0)
    rlat1 = radians(lat1)
    rlon0 = radians(lon0)
    rlon1 = radians(lon1)
    distRadians = 2*math.asin(math.sqrt(math.pow((math.sin((rlat0-rlat1)/2)),2) + \
                    math.cos(rlat0)*math.cos(rlat1)*math.pow((math.sin((rlon0-rlon1)/2)),2)))
    distMiles = earthRadius * distRadians
    return(distMiles)

# get nearby places using the API
def getPlaces(lat, lon, tilesize, amenity):
    client = requests.session()
    body = {'lat':lat, 'lon':lon, 'tilesize':tilesize, 'amenity':amenity}
    headers = {'content-type':'application/json'}
    response = client.post(config.APIURL, data=json.dumps(body), headers=headers)
    j = json.loads(response.content)
    return(j)
    #return(body)

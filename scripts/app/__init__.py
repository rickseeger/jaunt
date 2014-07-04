# imports
from flask import Flask

# Creates our application.
app = Flask(__name__)

# Development configuration settings
# WARNING - these should not be used in production
app.config.from_pyfile('settings/development.cfg')

# Production configuration settings
# To have these override your development settings,
# you'll need to set your environment variable to
# the file path:
# export PRODUCTION_SETTINGS=/path/to/settings.cfg
app.config.from_envvar('PRODUCTION_SETTINGS', silent=True)

# Application DEBUG - should be True in development
# and False in production
app.debug = app.config["DEBUG"]

# DATABASE SETTINGS
host = app.config["DATABASE_HOST"]
port = app.config["DATABASE_PORT"]
user = app.config["DATABASE_USER"]
passwd = app.config["DATABASE_PASSWORD"]
db = app.config["DATABASE_DB"]


from app import views

import jauntlib
import pprint

def places(args):
    # demo uses static map of Silicon Valley
    mapWidth = float(499)
    mapHeight = float(416)
    top = 37.681984
    left = -122.476479
    bottom = 37.186651
    right = -121.683392

    # convert arguments
    x = float(args.get("x"))
    lon = ((right-left) * (x / mapWidth)) + left
    y = float(args.get("y"))
    lat = top - ((top-bottom) * (y / mapHeight))
    tilesize = int(args.get("range"))
    amenity = str(args.get("amenity"))
    pp = pprint.PrettyPrinter()
    return pp.pformat(jauntlib.getPlaces(lat, lon, tilesize, amenity))


app.jinja_env.globals.update(places=places)

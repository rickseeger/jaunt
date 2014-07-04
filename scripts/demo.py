import config
from app import app

app.run(host=config.DemoHost, port=config.DemoPort, debug=True)

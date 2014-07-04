from flask import render_template
from app import app, host, port, user, passwd, db
import jauntlib

# ROUTING/VIEW FUNCTIONS
@app.route('/')
def index():
    # Renders index.html.
    return render_template('index.html')


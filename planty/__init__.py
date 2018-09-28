# Import flask and template operators
from flask import Flask
from flask_assets import Environment

from jinja2 import StrictUndefined

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

assets = Environment(app)

app.jinja_env.undefined = StrictUndefined
assets.url = app.static_url_path

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
import planty.views
import planty.reminder_sender

import os

# Statement for enabling the development environment
DEBUG = os.environ.get("DEBUG")
DEVELOPMENT = os.environ.get("DEVELOPMENT")

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI        = os.environ.get("DATABASE_URL")
SQALCHEMY_ECHO                 = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

PORT = os.environ.get("PORT")

# FlickrAPI
FLICKR_API_KEY    = os.environ.get("FLICKR_API_KEY")
FLICKR_API_SECRET = os.environ.get("FLICKR_API_SECRET")

# TwilioAPI
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN  = os.environ.get("TWILIO_TOKEN")

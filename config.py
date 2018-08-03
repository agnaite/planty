import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "secret"

PORT = os.environ.get("PORT")

# FlickrAPI
FLICKR_API_KEY = os.environ.get("FLICKR_API_KEY")
FLICKR_API_SECRET = os.environ.get("FLICKR_API_SECRET")

# TwilioAPI
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_TOKEN")

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
# THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
# CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
# CSRF_SESSION_KEY = "secret"

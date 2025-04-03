# config file
from datetime import timedelta
import logging

# static secret key for consistency
SECRET_KEY = 'FILL_ME_IN'

# not expiring sessions
PERMANENT_SESSION_LIFETIME = timedelta(days=365*100)

# SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
LOGGING_LEVEL = logging.DEBUG

# Browserstack testing
BROWSERSTACK_ACCESS_KEY = 'FILL_ME_IN'
BROWSERSTACK_USERNAME = 'FILL_ME_IN'
#!/usr/bin/python
from Flask import app as application
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/")

application.secret_key = 'AddYourSecretKey'

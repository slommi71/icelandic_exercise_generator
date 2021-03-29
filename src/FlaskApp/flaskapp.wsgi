#!/usr/bin/python
from FlaskApp import app as application
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/")

application.secret_key = 'AddYourSecretKey'

import sys
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.jinja_env.add_extension('jinja2.ext.do')
CORS(app)

from app.config import config

app.config.from_object(config)


from app.routes import *


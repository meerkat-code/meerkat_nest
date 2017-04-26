"""
Root Flask app for the Meerkat Nest.
"""
from flask import Flask, make_response, abort
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from datetime import datetime
from raven.contrib.flask import Sentry
import os
import resource

# Create the Flask app
app = Flask(__name__)


@app.route('/')
def nest_root_url():
    return "Meerkat Nest"
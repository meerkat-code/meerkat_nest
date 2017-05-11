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

from meerkat_nest import setup_database
from meerkat_nest import model

# Create the Flask app
app = Flask(__name__)
api = Api(app)
app.config.from_object('meerkat_nest.config.Config')

db_url = os.environ['MEERKAT_NEST_DB_URL']
setup_database.create_db(db_url, model.Base, drop=True)

@app.route('/')
def nest_root_url():
    return "Meerkat Nest"

from meerkat_nest.resources.upload_data import uploadData
from meerkat_nest.resources.download_data import downloadData

api.add_resource(uploadData, "/upload")
api.add_resource(downloadData, "/download")
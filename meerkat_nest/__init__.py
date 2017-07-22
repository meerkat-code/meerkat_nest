"""
Root Flask app for the Meerkat Nest.
"""
from flask import Flask
from flask_restful import Api
import os

from meerkat_nest import setup_database
from meerkat_nest import model

from meerkat_nest.resources.upload_data import UploadData
from meerkat_nest.resources.amend_data import amendData

# Create the Flask app
app = Flask(__name__)
api = Api(app)
app.config.from_object('meerkat_nest.config.Config')

db_url = os.environ['MEERKAT_NEST_DB_URL']
setup_database.create_db(db_url, model.Base, drop=False)


@app.route('/')
def nest_root_url():
    return "Meerkat Nest"

api.add_resource(UploadData, "/upload")
api.add_resource(amendData,"/amend")
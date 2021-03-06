import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from targetexplorer.core import read_project_config

targetexplorer_flaskapp_dir = os.path.dirname(__file__)

app = Flask(__name__)
db = SQLAlchemy(app)
project_config = read_project_config()
app.config.update(
    SQLALCHEMY_DATABASE_URI=project_config.get('sqlalchemy_database_uri')
)
import models

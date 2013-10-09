
"""cteward/st-sqlite RESTful API

provides simple sqlite storage API access
"""

import flask.ext.restless
import database

def init(app, config):
  """populate Flask app object with Api & resources"""

  manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=database.Database.database)

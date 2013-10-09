
"""cteward/st-sqlite database access

uses Flask-SQLAlchemy to provide database access
"""

import flask.ext.sqlalchemy

class Database:
  database = None
  """database connection object"""

  @staticmethod
  def init(app, config):
    """connect to database

    app    -- the flask application object
    config -- a dict containing parameters passed through.
    """
    Database.database = flask.ext.alchemy.SQLAlchemy(app)

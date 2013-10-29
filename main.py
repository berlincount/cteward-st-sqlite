#!/usr/bin/env python

"""cteward/st-sqlite storage API

provides simple sqlite storage

ENV: CTEWARD_ST_sqlite_CONFIG can override config file name
"""

import json
import os
import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from OpenSSL import SSL

config = {}
sslcontext = None
app = None
db = None
manager = None

def load_config():
  global config
  configfile = os.getenv('CTEWARD_ST_SQLITE_CONFIG', '/etc/cteward/st-sqlite.json')
  config = json.load(open(configfile))

def check_config():
  global config
  # runner not configured? -> default to 127.0.0.1:14339
  if not 'runner' in config:
    config['runner'] = {
      'port': 14339
    }

  # no flask configuration? no worries.
  if not 'flask' in config:
    config['flask'] = {}

  # no API configuration?
  if not 'api' in config:
    config['api'] = {
    }

def setup_ssl():
  global sslcontext
  # SSL configured? set up context for server
  if 'ssl' in config:
    sslcontext = SSL.Context(SSL.SSLv23_METHOD)
    sslcontext.use_certificate_file(config['ssl']['cert'])
    sslcontext.use_privatekey_file(config['ssl']['key'])

def setup_flask():
  global app
  # set up Flask object, configure it, add API, and go!
  app = flask.Flask('st-sqlite')
  app.config.update(**config['flask'])

def setup_database():
  global db
  global Tariff
  global Item
  global Price
  db = flask.ext.sqlalchemy.SQLAlchemy(app)

  class Tariff(db.Model):
    __tablename__ = 'tariffs'
    id          = db.Column('tariff_id',    db.Integer, primary_key=True)
    displayName = db.Column('dn',           db.String(80))
    meta_unit   = db.Column('meta',         db.Text)
    items       = db.relationship('Item')

  class Item(db.Model):
    __tablename__ = 'items'
    id          = db.Column('item_id',      db.Integer, primary_key=True)
    displayName = db.Column('dn',           db.String(80))
    tariff_id   = db.Column(db.Integer,     db.ForeignKey('tariffs.tariff_id'))
    price_id    = db.Column(db.Integer,     db.ForeignKey('prices.price_id'))
    meta        = db.Column('meta',         db.Text)

  class Price(db.Model):
    __tablename__ = 'prices'
    id          = db.Column('price_id',     db.Integer, primary_key=True)
    displayName = db.Column('dn',           db.String(80))
    amount      = db.Column('amount',       db.Float)
    amount_unit = db.Column('amount_unit',  db.String(12))
    price       = db.Column('price',        db.Float)
    price_unit  = db.Column('price_unit',   db.String(12))
    meta        = db.Column('meta',         db.Text)

  db.create_all()

def setup_manager():
  global manager
  manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

  manager.create_api(Tariff, methods=['GET', 'POST', 'PUT', 'DELETE'])
  manager.create_api(Item,   methods=['GET', 'POST', 'PUT', 'DELETE'])
  manager.create_api(Price,  methods=['GET', 'POST', 'PUT', 'DELETE'])

def run_app():
  global app
  app.run(ssl_context=sslcontext, **config['runner'])

if __name__ == '__main__':
  load_config()
  check_config()
  setup_ssl()
  setup_flask()
  setup_database()
  setup_manager()
  run_app()

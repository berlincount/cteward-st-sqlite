#!/usr/bin/env python

"""cteward/st-sqlite storage API

provides simple sqlite storage

ENV: CTEWARD_ST_sqlite_CONFIG can override config file name
"""

import json
import os
from flask import Flask
from OpenSSL import SSL

import api

import sys

config = {}
sslcontext = None
app = None

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

def setup_database():
  # database configured? initialize it!
  #if 'database' in config:
  #  Database.init(config['database'])
  pass

def setup_flask():
  global app
  # set up Flask object, configure it, add API, and go!
  app = Flask('st-sqlite')
  app.config.update(**config['flask'])

def setup_api():
  api.init(app, config=config['api'])

def run_app():
  global app
  app.run(ssl_context=sslcontext, **config['runner'])

if __name__ == '__main__':
  load_config()
  check_config()
  setup_ssl()
  setup_database()
  setup_flask()
  setup_api()
  run_app()

#!/usr/bin/env python

from flask import Flask
from db_subapi import db_subapi
from auth_subapi import auth_subapi
from entry_subapi import entry_subapi

import argparse

app = Flask(__name__)

app.register_blueprint(db_subapi)
app.register_blueprint(auth_subapi)
app.register_blueprint(entry_subapi)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the Flask cteward-st-sqlite app')

    args = parser.parse_args()
    print(app.url_map)
    app.run(host='0.0.0.0', debug=True)

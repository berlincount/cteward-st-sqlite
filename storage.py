#!/usr/bin/env python

# Simple storage backend using Flask & SQLite3
import argparse
import sqlite3
import json
import os

from flask import Flask, render_template, request, abort

app = Flask(__name__)
app.config.from_object(__name__)


def open_database(dbname):
    # if no dbname was given in the request itself,
    # use start of hostname requested
    if not dbname:
        dbname = request.host.split('.', 2)[0]

    # if we're not testing stay away from special DB names
    if not app.config['TESTING']:
        if dbname.startswith('_'):
            abort(400)

    # does the database exist and is writable for us?
    if not os.path.isfile('%s.sqlite3' % dbname):
        abort(404)
    if not os.access('%s.sqlite3' % dbname, os.W_OK):
        abort(520)

    return sqlite3.connect('%s.sqlite3' % dbname)


# list existing entries (TODO: no subtables yet)
@app.route("/entries",
           methods=['GET'],
           defaults={'dbname': None})
@app.route("/<dbname>/entries",
           methods=['GET'])
def get_entries(dbname):
    # db = open_database(dbname)
    print("get_entries %s" % dbname)
    selection = []  # list(r.table('entries').run(g.rdb_conn))
    return json.dumps(selection)


# create an entry
@app.route("/entries",
           methods=['POST'],
           defaults={'dbname': None})
@app.route("/<dbname>/entries",
           methods=['POST'])
def new_entry(dbname):
    print("new_entry %s" % dbname)
    # inserted = r.table('entries').insert(request.json).run(g.rdb_conn)
    # return jsonify(id=inserted['generated_keys'][0])


# get a single entry
@app.route("/entries/<string:entry_id>",
           methods=['GET'],
           defaults={'dbname': None})
@app.route("/<dbname>/entries/<string:entry_id>",
           methods=['GET'])
def get_entry(dbname, entry_id):
    print("get_entry %s" % dbname)
    # entry = r.table('entries').get(entry_id).run(g.rdb_conn)
    # return json.dumps(entry)


# replacing an entry (TODO: no updating / transaction log yet)
@app.route("/entries/<string:entry_id>",
           methods=['PUT'],
           defaults={'dbname': None})
@app.route("/<dbname>/entries/<string:entry_id>",
           methods=['PUT'])
def update_entry(dbname, entry_id):
    print("update_entry %s" % dbname)
    # return jsonify(r.table('entries').get(entry_id).replace(request.json)
    #                 .run(g.rdb_conn))


# updating an entry (TODO: no updating / transaction log yet)
@app.route("/entries/<string:entry_id>",
           methods=['PATCH'],
           defaults={'dbname': None})
@app.route("/<dbname>/entries/<string:entry_id>",
           methods=['PATCH'])
def patch_entry(dbname, entry_id):
    print("patch_entry %s" % dbname)
    # return jsonify(r.table('entries').get(entry_id).update(request.json)
    #                 .run(g.rdb_conn))


# deleting an entry (TODO: no updating / transaction log yet)
@app.route("/entries/<string:entry_id>",
           methods=['DELETE'],
           defaults={'dbname': None})
@app.route("/<dbname>/entries/<string:entry_id>",
           methods=['DELETE'])
def delete_entry(dbname, entry_id):
    print("delete_entry %s" % dbname)
    # return jsonify(r.table('entires').get(entry_id).delete().run(g.rdb_conn))


@app.route("/",
           methods=['GET'],
           defaults={'dbname': None})
@app.route("/<dbname>/",
           methods=['GET'])
def show_entries(dbname):
    # db = open_database(dbname)
    print("show_entries %s" % dbname)
    return render_template('entries.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the Flask cteward-st-sqlite app')

    args = parser.parse_args()
    print app.url_map
    app.run(host='0.0.0.0', debug=True)

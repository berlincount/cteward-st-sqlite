# Simple storage backend using Flask & SQLite3
import sqlite3
import glob
import os

from flask import Blueprint, request, abort, jsonify
from database import open_database

entry_subapi = Blueprint('entry_subapi', __name__)


@entry_subapi.route("/_databases",
                    methods=['GET'])
def databases_get():
    databases = [
        database.replace('.sqlite3', '')
        for database in glob.glob('*.sqlite3')
    ]
    return jsonify(data={'databases': databases})


@entry_subapi.route("/_databases",
                    methods=['POST'])
def databases_new():
    if not request.json:
        abort(400)
    if 'database' not in request.json:
        abort(400)

    # FIXME: sanitized database name
    # FIXME: limit _ database names
    if os.path.exists('%s.sqlite3' % request.json['database']):
        abort(409)
    else:
        db = sqlite3.connect('%s.sqlite3' % request.json['database'])
        if not db:
            abort(500)
        cursor = db.cursor()
        cursor.execute(
            'CREATE TABLE metadata (\
               version text,\
               created datetime,\
               updated datetime\
             )')
        cursor.execute(
            'CREATE TABLE entries (\
               id text,\
               data text\
             )')
    return jsonify(data={'database': request.json['database']})


@entry_subapi.route("/_databases/<string:dbname>",
                    methods=['DELETE'])
def databases_delete(dbname):
    if not os.path.exists('%s.sqlite3' % dbname):
        abort(404)
    os.remove('%s.sqlite3' % dbname)

    return jsonify(data={'message': 'ok'})


# list existing entries (TODO: no subtables yet)
@entry_subapi.route("/",
                    methods=['GET'],
                    defaults={'dbname': None})
@entry_subapi.route("/<string:dbname>/",
                    methods=['GET'])
def get_entries(dbname):
    db = open_database(dbname, request)
    # FIXME: db would be unused
    print("get_entries %s" % dbname, db)
    cursor = db.cursor()
    result = cursor.execute('SELECT id FROM entries')
    dataset = []
    for entry in result.fetchall():
        dataset.append(entry[0])
    db.close()

    return jsonify(data=dataset)


# create an entry
@entry_subapi.route("/",
                    methods=['POST'],
                    defaults={'dbname': None})
@entry_subapi.route("/<string:dbname>/",
                    methods=['POST'])
def new_entry(dbname):
    print("new_entry %s" % dbname)
    if not request.json:
        abort(400)
    if 'data' not in request.json:
        abort(400)

    db = open_database(dbname, request)
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO entries\
         (id, data)\
         VALUES\
         (?, ?)',
        (request.json['id'],
         request.json['data']))
    db.commit()
    db.close()

    return jsonify(data=request.json)

    # inserted = r.table('entries').insert(request.json).run(g.rdb_conn)
    # return jsonify(id=inserted['generated_keys'][0])


# get a single entry
@entry_subapi.route("/<string:entry_id>",
                    methods=['GET'],
                    defaults={'dbname': None})
@entry_subapi.route("/<string:dbname>/<string:entry_id>",
                    methods=['GET'])
def get_entry(dbname, entry_id):
    db = open_database(dbname, request)
    print("get_entry %s, %s" % (dbname, entry_id))
    cursor = db.cursor()
    result = cursor.execute(
        'SELECT\
         *\
         FROM\
         entries\
         WHERE\
         id = (?)', (entry_id,))
    # FIXME: check rowcount
    data = result.fetchone()
    desc = []
    for columndesc in result.description:
        desc.append(columndesc[0])
    db.close()
    return jsonify(data=dict(zip(desc, data)))
    # entry = r.table('entries').get(entry_id).run(g.rdb_conn)
    # return json.dumps(entry)


# replacing an entry (TODO: no updating / transaction log yet)
@entry_subapi.route("/<string:entry_id>",
                    methods=['PUT'],
                    defaults={'dbname': None})
@entry_subapi.route("/<string:dbname>/<string:entry_id>",
                    methods=['PUT'])
def update_entry(dbname, entry_id):
    print("update_entry %s" % dbname)
    # return jsonify(r.table('entries').get(entry_id).replace(request.json)
    #                 .run(g.rdb_conn))


# updating an entry (TODO: no updating / transaction log yet)
@entry_subapi.route("/<string:entry_id>",
                    methods=['PATCH'],
                    defaults={'dbname': None})
@entry_subapi.route("/<string:dbname>/<string:entry_id>",
                    methods=['PATCH'])
def patch_entry(dbname, entry_id):
    print("patch_entry %s" % dbname)
    # return jsonify(r.table('entries').get(entry_id).update(request.json)
    #                 .run(g.rdb_conn))


# deleting an entry (TODO: no updating / transaction log yet)
@entry_subapi.route("/<string:entry_id>",
                    methods=['DELETE'],
                    defaults={'dbname': None})
@entry_subapi.route("/<string:dbname>/<string:entry_id>",
                    methods=['DELETE'])
def delete_entry(dbname, entry_id):
    print("delete_entry %s" % dbname)
    # return jsonify(r.table('entires').get(entry_id).delete().run(g.rdb_conn))


# @app.route("/",
#            methods=['GET'],
#            defaults={'dbname': None})
# @app.route("/<string:dbname>/",
#            methods=['GET'])
# def show_entries(dbname):
#     # db = open_database(dbname)
#     print("show_entries %s" % dbname)
#     return render_template('entries.html')

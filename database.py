import sqlite3
import os
from flask import abort


def open_database(dbname, request):
    # if no dbname was given in the request itself,
    # use start of hostname requested
    if not dbname:
        dbname = request.host.split('.', 2)[0]

    # FIXME
    # if we're not testing stay away from special DB names
    # if not app.config['TESTING']:
    #    if dbname.startswith('_'):
    #         abort(400)

    # does the database exist and is writable for us?
    if not os.path.isfile('%s.sqlite3' % dbname):
        abort(404)
    if not os.access('%s.sqlite3' % dbname, os.W_OK):
        abort(520)

    return sqlite3.connect('%s.sqlite3' % dbname)

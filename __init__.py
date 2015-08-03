#!/usr/local/bin/python3.6
# coding: utf-8


# noinspection PyUnresolvedReferences
from common import *
# noinspection PyUnresolvedReferences
from andrew.dashboard import *
# noinspection PyUnresolvedReferences
from first.super_admin import *
# noinspection PyUnresolvedReferences
from first.stage1 import *
# noinspection PyUnresolvedReferences
from andrew.stage2 import *
# noinspection PyUnresolvedReferences
from first.stage3 import *
# noinspection PyUnresolvedReferences
from andrew.stage4 import *
# noinspection PyUnresolvedReferences
from first.stage5 import *
# noinspection PyUnresolvedReferences
from chat.chat import *


@app.error()
@app.error(400)
@app.error(401)
@app.error(402)
@app.error(403)
@app.error(404)
@app.error(405)
@app.error(500)
@app.error(501)
@app.error(502)
@app.error(503)
@view('errors')
def our_err(err):
    return dict(e=err, ver=PROJECT_VERSION, date=str(datetime.now())[:-7])


@app.route('/static/<name:path>')
def static_handler(name):
    return static_file(name, root='.')

@app.route ('/full_stats')
def stats():
	projects = [i for i in Project.select().order_by(Project.create_time.desc())]
	tickets = [i for i in Ticket.select().order_by(Ticket.add_time.desc())]
	return template('stats.tpl', projects=projects, tickets=tickets, ver=PROJECT_VERSION, date=str(datetime.now())[:-7]);

from gevent import monkey

monkey.patch_os()
monkey.patch_time()
monkey.patch_thread(threading=False, _threading_local=False, Event=True, logging=True,
                    existing_locks=True)
monkey.patch_all(os=False, time=False, thread=False)

app.run(host='0.0.0.0', port=8080, debug=True, reloader=False)

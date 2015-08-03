#!/usr/bin/python3
# coding: utf-8

"""
chat
author : andrew b
26.07.2015
"""

# TODO:
#

# OK:
#
from common import *


@app.post('/chat_broadcaster')
@app.post('/chat_broadcaster/')
def broadcaster_empty():
    pr_id = int(request.forms.getunicode('pr_id'))

    m = [i for i in ChatMessage
        .select()
        .where(ChatMessage.pid == pr_id)
        .order_by(ChatMessage.add_time.asc())]

    return str(m).replace('\'', '\"')


@app.post('/chat_broadcaster/<last_time>')
@app.post('/chat_broadcaster/<last_time>/')
def broadcaster(last_time):
    pr_id = int(request.forms.getunicode('pr_id'))

    m = [i for i in ChatMessage
        .select()
        .where(ChatMessage.add_time > last_time,
               ChatMessage.pid == pr_id)
        .order_by(ChatMessage.add_time.asc())]

    return str(m).replace('\'', '\"')


@app.post('/chat_history/<last_time>')
@app.post('/chat_history/<last_time>/')
def history(last_time):
    pr_id = int(request.forms.getunicode('pr_id'))

    m = [i for i in ChatMessage
        .select()
        .where(ChatMessage.add_time < last_time,
               ChatMessage.pid == pr_id)
        .order_by(ChatMessage.add_time.desc())
        .limit(90)]

    return str(m).replace('\'', '\"')


@app.post('/chat_user_data')
@app.post('/chat_user_data/')
def get_user_data():
    pr_id = int(request.forms.getunicode('pr_id'))

    admins = []
    writers = []

    user_roles_in_project = [i for i in Role.select().where(Role.pid == pr_id)]
    for i in user_roles_in_project:
        cat = UserCategory.get(UserCategory.id == i.cid)
        if 'a' in cat.priv:
            admins.append(User.get(User.id == i.uid).nickname)
        elif 'w' in cat.priv:
            writers.append(User.get(User.id == i.uid).nickname)

    return str(dict(admins=admins, writers=writers)).replace('\'', '\"')


@app.post('/chat_receiver')
@app.post('/chat_receiver/')
def receiver():
    pr_id = int(request.forms.getunicode('pr_id'))
    author = request.forms.getunicode('author')
    msg = request.forms.getunicode('msg')
    ChatMessage.create(author=author, msg=msg,
                       add_time=str(datetime.now())[:-7], pid=pr_id)
    return 'OK'

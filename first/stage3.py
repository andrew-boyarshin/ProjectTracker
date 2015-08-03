#!/usr/bin/python3
# coding: utf-8

"""
stage 3 v0.1
author : nev
27.07.2015
"""

# TODO:
# 

# OK:
# 

from common import *


@app.get('/projects/<pr_id:int>/ack')
@app.get('/projects/<pr_id:int>/ack/')
def ack_main(pr_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 3)
    sows = [i for i in Sow.select().where(Sow.pid == pr_id).order_by(Sow.edit_time.desc()).limit(1)]
    vector = []
    all_count = [0, 0]
    if len(sows) > 0:
        hds = [i for i in Header.select().where(Header.sowid == sows[0].id).order_by(SQL('nlevel'))]
        h1 = dict()
        for i in hds:
            if i.nlevel == 1:
                h1[i.id] = (i, [])
            else:
                h1[i.parent][1].append(i)
        h1 = sorted(h1.values(), key=lambda x: x[0].num)
        for i in h1:
            count = [0, 0]
            x = sorted(i[1], key=lambda x: x.num)
            x2 = []
            for j in x:
                y = ack_get_data(pr_id, j.id)
                if y[0] == y[1]:
                    count[0] += 1
                count[1] += 1
                my_app = (Approve.select().where(Approve.pid==pr_id, 
                    Approve.uid==u.id, Approve.hid==j.id)).count() > 0
                x2.append((j, y, my_app))
            all_count[0] += count[0]
            all_count[1] += count[1]
            vector.append((i[0], x2, count))
    if all_count[0] == all_count[1]:
        Project.update(stage=4).where(Project.id == pr_id).execute()
        redirect('/projects/' + str(pr_id) + '/maintain')
    print (vector)
    return template('first/stage3.tpl', vector=vector, sow_id=sows[0].id,
                    pid=sows[0].pid, all_count=all_count,
                    ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                    cur_author=u.nickname, readonly=not check_user_rights (u.id, pr_id, 'w'))


@app.get('/projects/<pr_id:int>/ack/change')
def ack_update(pr_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 3)
    if not check_user_rights (u.id, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    sid = request.query.sow
    h2 = request.query.h2
    st = request.query.st
    if st == 'true':
        Approve.create(uid=u.id, sowid=sid, hid=h2, pid=pr_id)
    else:
        Approve.delete().where(Approve.uid == u.id, Approve.hid == h2, Approve.pid == pr_id).execute()
    count = ack_get_data(pr_id, h2)
    res = (st == 'true' and count[0] == count[1]) or (st == 'false' and count[0] == count[1] - 1)
    return {'uc': count[1], 'ac': count[0], 'inc': int(res), 'st': int(st == 'true')}

#!/usr/bin/python3  
# coding: utf-8

"""
stage 1 v0.1
author : nev
26.07.2015
"""

# TODO:
# 

# OK:
# 

from common import *


# *******REDIRECT PAGES************************************************************************************

@app.post('/projects/<pr_id>/edit_sow_apply')
def edit_sow_apply(pr_id):
    def fix_string (s):
        return s.replace('<', '&lt;').replace('>', '&gt;')
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 1)
    uid = u.id
    if not check_user_rights (uid, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    vector = md2html(fix_string(request.forms.getunicode('sow')).strip())
    sid = Sow.create(editor=uid, edit_time=str(datetime.now())[:-7], pid=pr_id)
    h1i = 0
    for i in vector:
        if i != [None, [[None, None, None, False]], False] and i[0] != None:
            h1i += 1
            name = ''
            mdstr = ''
            if i[0] is not None:
                name = i[0].strip()
                if i[2]:
                    mdstr += name + '\n' + ''.join(['=' for i in range(len(name))]) + '\n'
                else:
                    mdstr = '# ' + name + '\n'
            h1id = Header.create(
                name=name, parent=sid, num=h1i,
                nlevel=1, sowid=sid, md=mdstr, html='', pid=pr_id)
            h2i = 0
            for j in i[1]:
                if (j != [None, None, None, False]) and (j != [None, '<p></p>', None, False]):
                    if j[1] is None:
                        j[1] = ''
                    html = j[1].replace('<p></p>', '')
                    h2i += 1
                    mdstr2 = ''
                    if j[0] is not None:
                        name2 = j[0].strip()
                        if j[3]:
                            mdstr2 += name2 + '\n' + ''.join(['-' for i in range(len(name2))]) + '\n'
                        else:
                            mdstr2 = '## ' + name2 + '\n'
                        if j[2] is not None:
                            mdstr2 += j[2]
                        Header.create(
                            name=name2, parent=h1id, num=h2i,
                            nlevel=2, sowid=sid,
                            md=mdstr2,
                            html=html, pid=pr_id)
                    else:
                        Header.update(md=mdstr + j[2], html=html).where(Header.id == h1id).execute()
    if h1i == 0:
        Sow.delete().where(Sow.id == sid).execute()
        redirect('/projects/' + str(pr_id) + '/sow?null_sow=true')
    else:
        sows = [i for i in Sow.select().where(Sow.pid == pr_id).order_by(Sow.edit_time.desc()).limit(1)]
        if len(sows) > 1:
            Approve.delete().where(Approve.sowid == sows[1].id, Approve.hid==0).execute()
        redirect('/projects/' + str(pr_id) + '/sow')


@app.post('/projects/<pr_id>/sow_approve')
def edit_sow_approve(pr_id):
    check_project_stage (pr_id, 1)
    u = user_check_project_access(pr_id)
    uid = u.id
    if not check_user_rights (uid, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    mode = request.forms.getunicode('type').strip()
    if mode == 'app':
        sows = [i for i in Sow.select().where(Sow.pid == pr_id).order_by(Sow.edit_time.desc()).limit(1)]
        if len(sows):
            app = Approve.select().where(Approve.uid == uid, Approve.pid==pr_id, Approve.hid==0).count()
            if app == 0:
                Approve.create(hid=0, sowid=sows[0].id, uid=uid, pid=pr_id)
    else:
        Approve.delete().where(Approve.uid == uid, Approve.pid==pr_id, Approve.hid==0).execute()
    redirect('/projects/' + str(pr_id) + '/sow')


# *******VISIBLE PAGES***********************************************************************************


@app.get('/projects/<pr_id:int>/sow')
@app.get('/projects/<pr_id:int>/sow/')
def sow_edit(pr_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 1)
    sows = [i for i in Sow.select().where(Sow.pid == pr_id).order_by(Sow.edit_time.desc())]
    # Get html and markdown from databaseP
    md_html = ['','']
    if len(sows) > 0:
        md_html = header2md(sows[0].id)
    # Make list of users and they rules
    # Check rules of current user
    users2 = [i for i in Role.select().where(Role.pid == pr_id)]
    users = []
    my_rules = False
    my_approve = False
    for i in users2:
        uc = UserCategory.get(UserCategory.id == i.cid)
        if 'w' in uc.priv:
            users.append(i)
            if i.uid == u.id:
                my_rules = True
    if len(sows):
        # Checking : if all writers give approvements, then redirect to next stage
        oks = [i for i in Approve.select().where(Approve.sowid == sows[0].id, Approve.hid==0)]
        if len(users) == len(oks):
            Project.update(stage=2).where(Project.id == pr_id).execute()
            redirect('/projects/' + str(pr_id))
            # Make list of users and they opinions
        for i in range(len(users)):
            appr = Approve.select().where(
                Approve.uid == users[i].uid, Approve.sowid == sows[0].id, Approve.hid==0).count()
            users[i] = (User.get(User.id == users[i].uid), appr > 0)
            my_approve |= (users[i][0].id == u.id) and users[i][1]
        #
    sows = [(i, User.get(User.id==i.editor)) for i in sows]
    return template2('first/sow_edit', ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                     md=md_html[0], pr_id=pr_id, html=md_html[1], users=users, 
                     my_app=my_approve, show=my_rules, esow=(len(sows) > 0),
                     null_sow=request.query.null_sow != '',
                     cur_author=u.nickname, sows=sows)

@app.get ('/projects/<pr_id:int>/sow/get_backup')
def get_backup (pr_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 1)
    sid = request.query.sowid
    sows = [i for i in Sow.select().where(Sow.id == sid)]
    if len (sows):
        md = header2md(sows[0].id)[0]
        return {'md': str(md)}
    return {'md': ''}
# noescape

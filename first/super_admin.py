#!/usr/bin/python3
# coding: utf-8

"""
super administrator's dashboard v0.1
author : nev & andrew b.
24.07.2015
"""

# TODO:
# 
# All
# Refill db

# OK:
# 

from common import *


@app.get('/sadm/init_db')
def sadm_init_db():
    db.database.set_autocommit(True)
    db.database.create_table(User, safe=True)
    db.database.create_table(Role, safe=True)
    db.database.create_table(UserCategory, safe=True)
    db.database.create_table(Project, safe=True)
    db.database.create_table(Header, safe=True)
    db.database.create_table(Sow, safe=True)
    db.database.create_table(Ticket, safe=True)
    db.database.create_table(ChatMessage, safe=True)
    db.database.create_table(Approve, safe=True)
    db.database.create_table(KV, safe=True)
    db.database.create_table(Request, safe=True)
    db.database.create_table(Comment, safe=True)
    db.database.create_table(Archive, safe=True)

    KV.create(k='superadmin_nick', v='nick')
    KV.create(k='superadmin_pass', v=sha('123'))
    UserCategory.create(name='Administrator', priv='ra')
    UserCategory.create(name='Developer', priv='rw')
    UserCategory.create(name='Coffee maker', priv='r')

    # Tests
    # User.create(name='nev', nickname='nev', password=sha('123'))
    # User.create(name='myke', nickname='myke', password=sha('456'))
    # User.create(name='andrewb', nickname='stalker_2010', password=sha('789'))
    # end tests
    # kv['lol'] = str(True)
    # db.database.commit()
    return 'DB initialized. <a href="/sadm">Return to super admin dashboard</a>'


# *****Superadmin block****************************************************************

# Redirect pages


def sadm_check_access(name=None, passw=None, to_redirect=True):
    name = name or request.get_cookie('susername')
    passw = passw or request.get_cookie('spassword')
    try:
        nick_kv = KV.get(KV.k == 'superadmin_nick', KV.v == name)
        pass_kv = KV.get(KV.k == 'superadmin_pass', KV.v == passw)
        if nick_kv is None or pass_kv is None:
            raise Exception()
        return nick_kv, pass_kv
    except Exception as e:
        if to_redirect:
            redirect('/sadm')
        return None


@app.post('/sadm')
def sadm_check_auth():
    name = request.forms.getunicode('name')
    passw = sha(request.forms.getunicode('pass'))
    if sadm_check_access(name, passw, to_redirect=False) is not None:
        response.set_cookie('susername', name)
        response.set_cookie('spassword', passw)
        redirect('/sadm/all')
    else:
        redirect('/sadm?wrong=True')


@app.post('/sadm/create_project')
def sadm_create_project():
    sadm_check_access()
    pr_name = request.forms.getunicode('name').strip()
    if len (pr_name) == 0:
        redirect('/sadm/all')
    p = [i for i in Project.select().where(Project.name == pr_name).limit(1)]
    if len(p):
        redirect('/sadm/all?exists=true')
    else:
        Project.create(name=pr_name, stage=1, create_time=str(datetime.now())[:-7])
        redirect('/sadm/all')


@app.post('/sadm/delete_project')
def sadm_delete_project():
    sadm_check_access()
    pr_id = request.forms.getunicode('pr_id')
    Project.delete().where(Project.id == pr_id).execute()
    Role.delete().where(Role.pid == pr_id).execute()
    Header.delete().where(Header.pid == pr_id).execute()
    Ticket.delete().where(Ticket.pid == pr_id).execute()
    Sow.delete().where(Sow.pid == pr_id).execute()
    Approve.delete().where(Approve.pid == pr_id).execute()
    ChatMessage.delete().where(ChatMessage.pid == pr_id).execute()
    Request.delete().where(Request.pid == pr_id).execute()
    Comment.delete().where(Comment.pid == pr_id).execute()
    redirect('/sadm/all')


@app.post('/sadm/edit_apply')
def sadm_edit_apply():
    sadm_check_access()
    uc = request.forms.getunicode('users_count')
    for i in range(1, int(uc) + 1):
        isadm = request.forms.getunicode('isadm' + str(i)) == 'on'
        uid = int(request.forms.getunicode('uid' + str(i)))
        cid = int(request.forms.getunicode('cid' + str(i)))
        if (cid == 1 and not isadm) or (cid != 1 and isadm):
            Role.update(cid=(1 if isadm else 3)).where(Role.uid == uid).execute()
    redirect('/sadm/all')


@app.post('/sadm/del_cat')
def sadm_del_cat():
    sadm_check_access()
    cid = int(request.forms.getunicode('cid'))
    if cid > 3:
        Role.update(cid=3).where(Role.cid == cid).execute()
        UserCategory.delete().where(UserCategory.id == cid).execute()
    redirect('/sadm/all')


@app.post('/sadm/change_cat')
def sadm_change_cat():
    sadm_check_access()
    cid = int(request.forms.getunicode('cid'))
    name=request.forms.getunicode('cat_name').strip()
    uc = [i for i in UserCategory.select().where(UserCategory.name==name)]
    if (len (name) == 0) or len(uc):
        redirect('/sadm/all')
    if cid > 3 and len(name) > 0:
        UserCategory.update(name=name,
                            priv=request.forms.getunicode('cat_rights')).where(UserCategory.id == cid).execute()
    redirect('/sadm/all')


@app.post('/sadm/<pr_id:int>/new_user')
def sadm_new_user(pr_id):
    sadm_check_access()
    uid = int(request.forms.getunicode('user_id'))
    rid = int(request.forms.getunicode('req_id'))
    Role.create(pid=pr_id, cid=1, uid=uid)
    Request.delete().where(Request.id == rid).execute()
    redirect('/sadm/all')


# Visible pages

@app.get('/sadm')
@app.get('/sadm/')
@view('first/sadm_login')
def sadm_main_page():
    name = request.get_cookie('susername')
    passw = request.get_cookie('spassword')
    if sadm_check_access(name, passw, to_redirect=False) is not None:
        redirect('/sadm/all')
    else:
        return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                    msg_viz=('block' if request.query.wrong != '' else 'none'))


@app.get('/sadm/all')
@app.get('/sadm/all/')
@view('first/sadm_all')
def sadm_all():
    sadm_check_access(to_redirect=True)
    cats = UserCategory.select()
    projects = [i for i in Project.select()]
    return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                projects=projects, cats=cats, exists=request.query.exists != '')


@app.get('/sadm/<pr_id:int>')
@app.get('/sadm/<pr_id:int>/')
@view('first/sadm_edit')
def sadm_edit_project(pr_id):
    sadm_check_access(to_redirect=True)
    pr = Project.get(Project.id == pr_id)
    users = [(User.get(User.id == i.uid),
              UserCategory.get(UserCategory.id == i.cid))
             for i in Role.select().where(Role.pid == pr.id)]
    req = []
    if len(users) == 0:
        req = [(i, User.get(User.id == i.uid)) for i in Request.select().where(Request.pid == pr.id)]
    return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                pr=pr, users=users, req=req)


# *****Admin block*************************************************************************

def admin_check_access(pr_id):
    us = user_check_project_access(pr_id)
    if not us:
        redirect('/')
    else:
        pid = Project.select().where(Project.id == pr_id)
        role = Role.get(Role.pid == pid, Role.uid == us.id)
        if not ('a' in UserCategory.get(UserCategory.id == role.cid).priv):
            redirect('/')
    return us


# Redirect pages

@app.post('/admin/<pr_id:int>/new_user')
def admin_new_user(pr_id):
    admin_check_access(pr_id)
    uid = int(request.forms.getunicode('user_id'))
    rid = int(request.forms.getunicode('req_id'))
    Role.create(pid=pr_id, cid=3, uid=uid)
    Request.delete().where(Request.id == rid).execute()
    redirect('/admin/' + str(pr_id))


@app.post('/admin/<pr_id:int>/del_req')
def admin_del_req(pr_id):
    admin_check_access(pr_id)
    rid = int(request.forms.getunicode('req_id'))
    Request.delete().where(Request.id == rid).execute()
    redirect('/admin/' + str(pr_id))


@app.post('/admin/<pr_id:int>/del_user')
def admin_del_user(pr_id):
    us = admin_check_access(pr_id)
    uid = int(request.forms.getunicode('uid'))
    uid_my = us.id
    if uid_my != uid:
        Role.delete().where(Role.uid == uid, Role.pid == pr_id).execute()
    redirect('/admin/' + str(pr_id))


@app.post('/admin/<pr_id:int>/change_user_role')
def admin_change_role(pr_id):
    us = admin_check_access(pr_id)
    uid = int(request.forms.getunicode('uid'))
    cid = int(request.forms.getunicode('new_role'))
    uid_my = us.id
    if uid != uid_my:
        Role.update(cid=cid).where(Role.uid == uid).execute()
    else:
        uc = UserCategory.get(UserCategory.id == cid)
        if 'a' in uc.priv:
            Role.update(cid=cid).where(Role.uid == uid).execute()
    redirect('/admin/' + str(pr_id))


@app.post('/admin/<pr_id:int>/create_usercat')
def admin_create_category(pr_id):
    admin_check_access(pr_id)
    name = request.forms.getunicode('cat_name').strip()
    if len(name): 
        a = ('a' if request.forms.get ("a_right") == 'on' else '') 
        w = ('w' if request.forms.get ("w_right") == 'on' else '') 
        # r = ('r' if request.forms.get ("r_right") == 'on' else '') 
        r = 'r'
        rights = a + w + r
        uc = [i for i in UserCategory.select().where(UserCategory.name==name)]
        if len(rights) and len(name) and (len(uc) == 0):
            UserCategory.create(name=name, priv=rights)
            redirect('/admin/' + str(pr_id))
        else:
            redirect('/admin/'+str(pr_id)+'?no_category=true')
    else:
        redirect('/admin/'+str(pr_id)+'?no_category=true')


@app.post('/admin/<pr_id:int>/change_stage')
def admin_change_stage(pr_id):
    admin_check_access(pr_id)
    sows = [i for i in Sow.select().where(Sow.pid == pr_id).order_by(Sow.edit_time.desc()).limit(1)]
    if len (sows) == 0:
        redirect('/admin/'+str(pr_id)+'?no_sow=true')
    stage = int(request.forms.getunicode('stage'))
    if stage == 5:
        pr = Project.get(Project.id == pr_id)
        sows = sows[0]
        md = ''
        hds = [i for i in Header.select().where(Header.sowid == sows.id).order_by(SQL('nlevel'))]
        h1 = dict()
        for i in hds:
            if i.nlevel == 1:
                h1[i.id] = (i, [])
            else:
                h1[i.parent][1].append(i)
        h1 = sorted(h1.values(), key=lambda x: x[0].num)
        for i in h1:
            # md += '# ' + i[0].name + '\n' + i[0].md
            if i[0].md != '':
                md += i[0].md
            x = sorted(i[1], key=lambda x: x.num)
            for j in x:
                md += j.md + '\n'
        tickets1 = Ticket.select().where(Ticket.pid == pr_id, Ticket.category > 2,
                                         Ticket.category < 5, Ticket.closed == True).count()
        tickets2 = Ticket.select().where(Ticket.pid == pr_id, Ticket.category > 2, Ticket.category < 5).count()
        tickets3 = Ticket.select().where(Ticket.pid == pr_id, Ticket.closed == True).count()
        tickets4 = Ticket.select().where(Ticket.pid == pr_id).count()
        tickets = str(tickets1) + '/' + str(tickets2) + '/' + str(tickets3) + '/' + str(tickets4)
        Archive.create(name=pr.name, close_time=str(datetime.now())[:-7], create_time=pr.create_time,
                       md=md, tickets=tickets)
        Project.delete().where(Project.id == pr_id).execute()
        Role.delete().where(Role.pid == pr_id).execute()
        Header.delete().where(Header.pid == pr_id).execute()
        Ticket.delete().where(Ticket.pid == pr_id).execute()
        Sow.delete().where(Sow.pid == pr_id).execute()
        Approve.delete().where(Approve.pid == pr_id).execute()
        ChatMessage.delete().where(ChatMessage.pid == pr_id).execute()
        Request.delete().where(Request.pid == pr_id).execute()
        Comment.delete().where(Comment.pid == pr_id).execute()
        redirect('/projects')
    else:
        Project.update(stage=stage).where(Project.id == pr_id).execute()
        redirect('/admin/' + str(pr_id))


# Visible pages

@app.get('/admin/<pr_id:int>')
@view('first/admin_main')
def admin_main(pr_id):
    admin_check_access(pr_id)
    pr = Project.get(Project.id == pr_id)
    req = [(i, User.get(User.id == i.uid)) for i in Request.select().where(Request.pid == pr.id)]
    rs = [i for i in Role.select().where(Role.pid == pr.id)]
    users = [(User.get(User.id == i.uid), UserCategory.get(UserCategory.id == i.cid))
             for i in Role.select().where(Role.pid == pr.id)]
    cats = UserCategory.select()
    return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                pr=pr, users=users, req=req, roles=rs, cats=cats,
                no_sow=request.query.no_sow != '', no_category=request.query.no_category != '')

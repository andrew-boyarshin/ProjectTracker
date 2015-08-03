#!/usr/bin/python3
# coding: utf-8

"""
dashboard v0.1
author : andrew b. & nev
24.07.2015
"""

# TODO:
# 

# OK:
# 

from common import *


#######################################################################################################################


@app.get('/')
@view('andrew/dash_auth')
def user_auth():
    if user_check_access(to_redirect=False) is not None:
        redirect('/projects')
    else:
        return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                    wrong=request.query.wrong != '',
                    already_reg=request.query.already_registered != '',
                    too_long=request.query.too_long != '')


def user_check_access_by_uname(uname, passw=None, to_redirect=True):
    passw = passw or request.get_cookie('password')
    try:
        user = User.get(User.nickname == uname, User.password == passw)
        if user is None:
            raise Exception()
        return user
    except Exception as e:
        if to_redirect:
            redirect('/')
        return None


@app.post('/login')
def user_check_auth():
    name = request.forms.getunicode('nick')
    if len(name):
        passw = sha(request.forms.getunicode('pass'))
        u = user_check_access_by_uname(name, passw, to_redirect=False)
        if u is not None:
            response.set_cookie('uid', str(u.id))
            response.set_cookie('password', str(passw))
            redirect('/projects')
    redirect('/?wrong=True')


@app.post('/register')
def user_register():
    name = fix_string(request.forms.getunicode('nick'))
    if len(name):
        passw = request.forms.getunicode('pass')
        if len(passw):
            passw = sha(passw)
            us = [i for i in User.select().where(User.nickname == name).limit(1)]
            if len(us):
                u = user_check_access_by_uname(name, passw, to_redirect=False)
                if u is not None:
                    response.set_cookie('uid', str(u.id))
                    response.set_cookie('password', str(passw))
                    redirect('/projects')
                else:
                    redirect('/?already_registered=true')
            else:
                if len(name) < 20:
                    u = User.create(name=name, nickname=name, password=passw)
                    response.set_cookie('uid', str(u.id))
                    response.set_cookie('password', str(passw))
                    redirect('/projects?first_time=true')
                else:
                    redirect('/?too_long=true')
    redirect('/')

@app.get("/request/cancel/<id:int>")
def request_access_cancel(id):
    user_check_auth_data()
    r = Request.get(Request.id == id)
    if r:
        r.delete_instance()
    redirect('/request_access')


@app.get("/request/apply/<id:int>/<comment:path>")
def request_access_apply(id, comment):
    u = user_check_auth_data()
    if u:
        Request.create(uid=u.id, pid=id, comment=comment)
    redirect('/request_access')


@app.get("/request/apply/<id:int>/")
def request_access_apply(id):
    u = user_check_auth_data()
    if u:
        Request.create(uid=u.id, pid=id, comment='(no comment)')
    redirect('/request_access')

@app.post("/settings/save/password")
def settings_save_password():
    u = user_check_auth_data()
    old_pass = request.forms.getunicode('old')
    new_pass = request.forms.getunicode('new')
    new_confirm_pass = request.forms.getunicode('new_confirm')
    if len(old_pass) and len(new_pass) and len(new_confirm_pass):
        old_pass = sha(old_pass)
        new_pass = sha(new_pass)
        new_confirm_pass = sha(new_confirm_pass)
        if old_pass == u.password:
            if new_pass == new_confirm_pass:
                if u.password != new_pass:
                    User.update(password=new_pass).where(User.id == u.id).execute()
                    response.set_cookie('password', new_pass, path='/')
                redirect('/settings?changed_pass=true')
            else:
                redirect('/settings?diff_new=true')
        else:
            redirect('/settings?wrong_pass=true')
    else:
        redirect('/settings?null_pass=true')     


@app.get('/logout')
def logout():
    response.delete_cookie('username')
    response.delete_cookie('password')
    redirect('/')


@app.post("/settings/save/username")
def settings_save_username():
    u = user_check_auth_data()
    new_username = request.forms.getunicode('username')
    if len(new_username):
        User.update(name=new_username).where(User.id == u.id).execute()
        redirect('/settings?changed_name=true')
    else:
        redirect('/settings?null_name=true')

#######################################################################################################################

# *****Users block*****

# Visible pages

@app.get('/projects')
@app.get('/projects/')
@view('first/select_project')
def select_project():
    u = user_check_auth_data()
    pr = []
    for i in Role.select().where(Role.uid == u.id):
        pr.append(Project.get(Project.id == i.pid))
    return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                projects=pr)


@app.get('/projects/<pr_id:int>')
@app.get('/projects/<pr_id:int>/')
@view('first/user_view_project')
def select_project(pr_id):
    u = user_check_project_access(pr_id)
    pr = Project.get(Project.id == pr_id)
    uid = u.id
    role = Role.get(Role.pid == pr_id, Role.uid == uid)
    isadm = ('a' in UserCategory.get(UserCategory.id == role.cid).priv)
    stage = pr.stage
    redirect_link = '/projects/' + str(pr_id) + '/' + ('sow', 'dev', 'ack', 'maintain', 'done')[stage - 1]
    if isadm:
        return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                    isadm=isadm, pr=pr, redirect_href=redirect_link)
    else:
        redirect(redirect_link)


@app.get("/settings")
@app.get("/settings/")
@view('andrew/dash_settings')
def settings():
    u = user_check_auth_data()
    return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                username=u.name, 
                ch_name=request.query.changed_name != '', 
                null_name=request.query.null_name != '',
                ch_pass=request.query.changed_pass != '',
                diff_new=request.query.diff_new != '',
                wrong_pass=request.query.wrong_pass != '',
                null_pass=request.query.null_pass != '')

@app.get("/help")
@app.get("/help/")
def help_red ():
    redirect ('/help/0')

@app.get("/help/<help_name>")
@app.get("/help/<help_name>/")
def help_show (help_name):
    html = ''
    try:
        with open('help/'+str(help_name)+'.md', 'r') as f:
            vector = md2html(f.read())
            for i in vector:
                if i != [None, [[None, None, None, False]], False] and i[0] != None:
                    if i[0] is None: i[0] = ''
                    html += '<h1>'+i[0]+'</h1>'
                    for j in i[1]:
                        if (j != [None, None, None, False]) and (j != [None, '<p></p>', None, False]):
                            if j[1] is None: j[1] = ''
                            if j[0] is None: j[0] = ''
                            html += '<h2>'+j[0]+'</h2>' + j[1].replace('<p></p>', '')
    except Exception as e:
        abort (404, "Sorry, file not found")
    return template2('first/show_help.tpl', ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
        md=html)

@app.get("/request_access")
@view('andrew/request_access')
def request_access():
    u = user_check_auth_data()
    rqs = [i for i in Request.select().where(Request.uid == u.id)]
    res_already = []
    res_avail = []
    projects = [i for i in Project.select()]
    for i in projects:
        try:
            if Role.get(Role.uid == u.id, Role.pid == i.id) is not None:
                continue
        except:
            rq = None
            for j in rqs:
                if j.pid == i.id:
                    rq = j

            if rq is not None:
                res_already.append((i, rq))
            else:
                res_avail.append(i)

    res_avail = [(i, Role.select().where(Role.pid==i.id).count()) for i in res_avail]

    return dict(ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                res_already=res_already, res_avail=res_avail)



from common import *


# noinspection PyPep8Naming
@app.get('/projects/<pr_id:int>/dev')
@app.get('/projects/<pr_id:int>/dev/')
def sow_dev(pr_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    latest = [i for i in Sow.select().where(Sow.pid == pr_id).order_by(Sow.edit_time.desc()).limit(1)]
    if not len(latest):
        redirect('/projects/'+str(pr_id))
    latest = latest[0]
    headers = [i for i in Header.select().where(Header.sowid == latest.id).order_by(Header.nlevel.asc())]
    data = {}
    num_by_id = {}
    for i in headers:
        if i.nlevel == 1:
            data[i.num] = {}
            data[i.num]['h1'] = i
            num_by_id[i.id] = i.num
        else:
            data[num_by_id[i.parent]][i.num] = i
    for k, i in data.items():
        data[k] = sorted(i.values(), key=lambda x: (x.nlevel, x.num))
    return template2('andrew/stage2', data=data, pr_id=pr_id, 
        ver=PROJECT_VERSION, date=str(datetime.now())[:-7],
                     cur_author=u.nickname)


@app.get('/projects/<pr_id:int>/dev/load/<header_id:int>')
def sow_dev_load(pr_id, header_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    header = Header.get(Header.id == header_id)
    res = []
    for i in Ticket.select().where(Ticket.hid == header_id).order_by(Ticket.add_time.asc()):
        comments = []
        for j in Comment.select().where(Comment.tid == i.id).order_by(Comment.add_time.asc()):
            cur = dict(
                id=j.id,
                nick=str(j.nick),
                tid=j.tid,
                msg=md2html_line(fix_string(str(j.msg))),
                add_time=str(j.add_time),
                edit_time=str(j.edit_time),
                pid=str(j.pid)
            )
            comments.append(cur)
        cur = dict(
            id=i.id,
            name=md2html_line(fix_string(str(i.name))),
            content=md2html_line(fix_string(str(i.content))),
            add_time=i.add_time,
            hid=i.hid,
            category=i.category,
            closed=str(i.closed).lower(),
            close_time=i.close_time,
            nickname=i.nickname,
            pid=i.pid,
            comments=comments
        )
        res.append(cur)
    my_priv = check_user_rights (u.id, pr_id, 'w')
    data = {'ro': str (not my_priv), 'html': header.html, 'tickets': res}
    return str(data).replace('\'', '\"')


@app.get('/projects/<pr_id:int>/dev/<ticket_id:int>/mark')
def sow_dev_mark(pr_id, ticket_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    if not check_user_rights (u.id, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    Ticket.update(closed=True, close_time=str(datetime.now())[:-7]).where(Ticket.id == ticket_id).execute()
    return 'OK'


@app.get('/projects/<pr_id:int>/dev/<ticket_id:int>/unmark')
def sow_dev_unmark(pr_id, ticket_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    if not check_user_rights (u.id, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    Ticket.update(closed=False, close_time='').where(Ticket.id == ticket_id).execute()
    return 'OK'


@app.post('/projects/<pr_id:int>/dev/<hid:int>/ticket_create')
def sow_dev_create_ticket(pr_id, hid):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    if not check_user_rights (u.id, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    data = request.forms.getunicode('data').strip()
    if len(data):
        splitted = data.split('\n', maxsplit=1)
        title = splitted[0]
        content = splitted[1] if len(splitted) > 1 else splitted[0]
        Ticket.create(name=title, content=content,
                      add_time=str(datetime.now())[:-7],
                      hid=hid, 
                      category=4 if ('error' in title.lower()) or ('fatal' in title.lower()) else 1,
                      crit=False, closed=False, close_time='', nickname=u.nickname, pid=pr_id)
        return 'OK'
    return 'FAIL'


@app.post('/projects/<pr_id:int>/dev/ticket/<ticket_id:int>/set_category')
def sow_dev_set_category(pr_id, ticket_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    if not check_user_rights (u.id, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    new_cat = int(request.forms.getunicode('val').strip())
    Ticket.update(category=new_cat).where(Ticket.id == ticket_id).execute()
    return 'OK'


@app.post('/projects/<pr_id:int>/dev/ticket/<ticket_id:int>/comment_create')
def sow_dev_create_comment(pr_id, ticket_id):
    u = user_check_project_access(pr_id)
    check_project_stage (pr_id, 2)
    if not check_user_rights (u.id, pr_id, 'w'):
        abort(403, "Sorry, access denied.")
    data = request.forms.getunicode('msg').strip()
    if len(data):
        Comment.create(nick=u.nickname, tid=ticket_id, msg=data, 
            add_time=str(datetime.now())[:-7], edit_time='', pid=pr_id)
        return 'OK'
    return 'FAIL'

import hashlib

from bottle_peewee import PeeweePlugin
from peewee import *
from bottle import *
from md2html import *

app = Bottle()

db = PeeweePlugin(connection='sqlite:///one.db')
app.install(db)

PROJECT_VERSION = '0.2'

chat_receiver_app = Bottle()
chat_broadcaster_app = Bottle()


class BaseModel(Model):
    class Meta(object):
        database = db.proxy


class User(BaseModel):
    name = TextField()
    nickname = TextField()
    password = TextField()

    def __repr__(self):
        return 'User[{}, {}, {}, {}]'.format(
            str(self.id),
            str(self.name), str(self.nickname), str(self.password))


class Role(BaseModel):
    pid = IntegerField()
    uid = IntegerField()
    cid = IntegerField()

    def __repr__(self):
        return 'Role[{}, {}, {}]'.format(
            str(self.pid), str(self.uid), str(self.cid))


class UserCategory(BaseModel):
    name = TextField()
    priv = TextField()

    def __repr__(self):
        return 'UserCategory[{}, {}]'.format(
            str(self.name), str(self.priv))


class Project(BaseModel):
    name = TextField()
    stage = IntegerField()
    create_time = TextField()

    def __repr__(self):
        return 'User[{}, {}]'.format(
            str(self.name), str(self.stage))


class Header(BaseModel):
    name = TextField()
    parent = IntegerField()
    num = IntegerField()
    nlevel = IntegerField()
    sowid = IntegerField()
    md = TextField()
    html = TextField()
    pid = IntegerField()

    def __repr__(self):
        return 'Header[{}, {}, {}, {}, {}, {}, {}]'.format(
            str(self.name), str(self.parent), str(self.num), str(self.nlevel),
            str(self.sowid), str(self.md), str(self.html))


class Sow(BaseModel):
    editor = TextField()
    edit_time = TextField()
    pid = IntegerField()

    def __repr__(self):
        return 'Sow[{}, {}, {}]'.format(
            str(self.editor), str(self.edit_time), str(self.pid))


class Ticket(BaseModel):
    name = TextField()
    content = TextField()
    add_time = TextField()
    hid = IntegerField()
    category = IntegerField()  # IWEFR - 12345
    closed = BooleanField()
    close_time = TextField()
    nickname = TextField()
    pid = IntegerField()

    def __repr__(self):
        mesg = "'id': {}, 'name': '{}', 'content': '{}', 'add_time': '{}', 'hid': {}, 'category': {}, 'closed': {}, 'close_time': '{}', 'nickname': '{}', 'pid': {}"
        mesg = mesg.format(self.id,
                           md2html_line(str(self.name)), md2html_line(str(self.content).replace('\n', '<br />')),
                           self.add_time, self.hid, self.category,
                           str(self.closed).lower(),
                           self.close_time, self.nickname, self.pid)
        mesg = '{' + mesg + '}'
        return mesg


class ChatMessage(BaseModel):
    author = TextField()
    msg = TextField()
    add_time = TextField()
    pid = IntegerField()

    def __repr__(self):
        mesg = "'id': {}, 'author': '{}', 'msg': '{}', 'add_time': '{}', 'pid': {}"
        mesg = mesg.format(self.id, self.author, md2html_line(fix_string(self.msg)), self.add_time, self.pid)
        mesg = '{' + mesg + '}'
        return mesg


class Approve(BaseModel):
    hid = IntegerField()
    sowid = IntegerField()
    uid = IntegerField()
    pid = IntegerField()

    def __repr__(self):
        return 'Approve[{}, {}, {}, {}]'.format(
            str(self.hid), str(self.sowid),
            str(self.uid), str(self.pid))


class Comment(BaseModel):
    nick = TextField()
    tid = IntegerField()
    msg = TextField()
    add_time = TextField()
    edit_time = TextField()
    pid = IntegerField()

    def __repr__(self):
        mesg = "'id': {}, 'nick': '{}', 'tid': {}, 'msg': '{}', 'add_time': '{}', 'edit_time': '{}', 'pid': {}"
        mesg = mesg.format(str(self.id), str(self.nick), str(self.tid), md2html_line(str(self.msg)), str(self.add_time),
                           str(self.edit_time), str(self.pid))
        mesg = '{' + mesg + '}'
        return mesg


class Archive(BaseModel):
    name = TextField()
    create_time = TextField()
    close_time = TextField()
    md = TextField()
    tickets = TextField()


class KV(BaseModel):
    k = TextField()
    v = TextField()

    def __repr__(self):
        return 'KV[{}, {}]'.format(
            str(self.k), str(self.v))


class Request(BaseModel):
    uid = IntegerField()
    pid = IntegerField()
    comment = TextField()

    def __repr__(self):
        return 'KV[{}, {}, {}]'.format(
            str(self.uid), str(self.pid), str(self.comment))


def sha(s):
    return hashlib.sha1(s.encode()).hexdigest()


def user_check_access(uid=None, passw=None, to_redirect=True):
    uid = uid or request.get_cookie('uid')
    passw = passw or request.get_cookie('password')
    try:
        user = User.get(User.id == uid, User.password == passw)
        if user is None:
            raise Exception()
        return user
    except Exception as e:
        if to_redirect:
            redirect('/')
        return None


def user_check_auth_data(main_page=False):
    c = user_check_access(to_redirect=(not main_page))
    if c:
        if main_page:
            redirect('/projects')
    # if c and main_page: ... ? -- myke
    return c


def user_check_project_access(pr_id):
    u = user_check_auth_data()
    uid = u.id
    if len([i for i in Role.select().where(Role.pid == pr_id, Role.uid == uid)]) == 0:
        redirect('/projects')
    return u

def check_project_stage(pr_id, stage):
    pr = Project.get (Project.id==pr_id)
    if pr.stage != stage:
        redirect('/projects/'+str(pr_id))
    return True

def check_user_rights (uid, pid, need):
    role = Role.get (Role.uid == uid, Role.pid == pid)
    cat = UserCategory.get (UserCategory.id == role.cid)
    return need in cat.priv

def get_users_priv_count(s, pid):
    users2 = [i for i in Role.select().where(Role.pid == pid)]
    users = 0
    for i in users2:
        uc = UserCategory.get(UserCategory.id == i.cid)
        if s in uc.priv:
            users += 1
    return users

def rus_declension (x, y):
    """ declension for russian nouns """
    x = x % 100
    if (x < 21 and x > 4) or x == 0:
        return y[2]
    elif x % 10 == 1:
       return y[0]
    return y[1]


def ack_get_data(pid, h2id):
    count_h2 = Approve.select().where(Approve.hid == h2id, Approve.pid == pid).count()
    count_users = get_users_priv_count('w', pid)
    return (count_h2, count_users)


# noinspection PyShadowingNames
def template2(*args, **kwargs):
    """
    Get a rendered template as a string iterator.
    You can use a name, a filename or a template string as first parameter.
    Template rendering arguments can be passed as dictionaries
    or directly (as keyword arguments).
    """
    tpl = args[0] if args else None
    adapter = kwargs.pop('template_adapter', MyTemplate)
    lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    tplid = (id(lookup), tpl)
    if tplid not in TEMPLATES or DEBUG:
        settings = kwargs.pop('template_settings', {})
        if isinstance(tpl, adapter):
            TEMPLATES[tplid] = tpl
            print(123)
            if settings: 
                TEMPLATES[tplid].prepare(**settings)
        elif "\n" in tpl or "{" in tpl or "%" in tpl or '$' in tpl:
            TEMPLATES[tplid] = adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tplid] = adapter(name=tpl, lookup=lookup, **settings)
    if not TEMPLATES[tplid]:
        abort(500, 'Template (%s) not found' % tpl)
    for dictarg in args[1:]: 
        kwargs.update(dictarg)
    return TEMPLATES[tplid].render(kwargs)


# noinspection PyAttributeOutsideInit
class MyTemplate(SimpleTemplate):
    def prepare(self, escape_func=html_escape, noescape=True, syntax=None, **ka):
        self.cache = {}
        enc = self.encoding
        self._str = lambda x: touni(x, enc)
        self._escape = lambda x: escape_func(touni(x, enc))
        self.syntax = syntax
        if noescape:
            self._str, self._escape = self._escape, self._str


def fix_string(s):
    return s \
        .replace('\"', '&quot;') \
        .replace('\'', '&apos;') \
        .replace('<', '&lt;') \
        .replace('>', '&gt;') \
        .replace('\n', '<br />')

def header2md (sowid):
    md = ''
    html = ''
    hds = [i for i in Header.select().where(Header.sowid == sowid).order_by(SQL('nlevel'))]
    h1 = dict()
    for i in hds:
        if i.nlevel == 1:
            h1[i.id] = (i, [])
        else:
            h1[i.parent][1].append(i)
    h1 = sorted(h1.values(), key=lambda x: x[0].num)
    for i in h1:
        html += '<h1>' + i[0].name + '</h1>'
        # md += '#' + i[0].name + '\n'
        if i[0].md != '':
            html += i[0].html
            md += i[0].md
        i[1].sort(key=lambda x: x.num)
        for j in i[1]:
            md += j.md + '\n'
            j.name = '<h2>' + j.name + '</h2>'
            html += j.name + j.html
    return (md, html)


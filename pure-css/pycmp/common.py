#!/usr/bin.env python3
# -*- coding: utf-8 -*-
import db


def search(request):
    """Performs search in db.
    request - str
    return rows - list of cortages
    """
    req_id = None
    try:
        req_id = int(request)
    except ValueError:
        req_id = None

    sql_str = "title='{req}' OR description='{req}'"
    if req_id:
        sql_str = "id={req} OR title='{req}' OR description='{req}'"
    sql_str = sql_str.format(req=request)
    res = db.select("CMPS", sql_str)

    return res


def user_answers_for_cmp(cmp_id, user_id):
    """get users answers for competition
    return list of rows
    """
    user_answers = []
    cond_f = 'cmp_id={}'
    cond = cond_f.format(cmp_id)
    questions = db.select('questions', cond)
    cond_f = 'user_id={} AND task_id={}'.format(user_id, '{}')
    for task in questions:
        cond = cond_f.format(task[0])
        user_answers += db.select('user_answers', cond)
    return user_answers


def is_user_solve_cmp(cmp_id, user_id):
    """
    return True or False
    """
    cond_f = 'cmp_id={}'
    cond = cond_f.format(cmp_id)
    questions = db.select('questions', cond)
    cond_f = 'user_id={} AND task_id={}'
    if questions and len(questions) and len(questions[0]):
        cond = cond_f.format(user_id, questions[0][0])
        return bool(db.select('user_answers', cond))
    else:
        return False


def escape(string):
    res = string.replace("`", '"')
    res = res.replace("\\", '')
    res = res.replace(";", "\\;")
    res = res.replace("'", '"')
    res = res.replace('"', '\\"')
    res = res.replace("<", "\\<")
    res = res.replace(">", "\\>")
    return res


def dbg_log(msg):
    with open('logs/my_log.log', 'a', encoding="utf-8") as oufile:
        oufile.writelines(msg + '\n')

# Taken from Python source code
_MONTHNAMES = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_DAYNAMES = [None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def utctime(date):
    weekday = date.toordinal() % 7 or 7
    return "%s, %2d %s %04d %02d:%02d:%02d GMT" % (
        _DAYNAMES[weekday],
        date.day,
        _MONTHNAMES[date.month],
        date.year,
        date.hour, date.minute, date.second)

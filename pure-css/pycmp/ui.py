#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UI module. Forms HTML page with CSS and JS mixins.
"""
import db
import string

HTML_FOLDER = "templates/"


def main_page(data):
    return login_page(data)


def login_page(data):
    """data
    error_msg - str - Error message to show(if no error - can be None or empty)
    """
    html = get_html(HTML_FOLDER + "auth.html")
    html = prepare(html)

    emsg = data["error_msg"] if "error_msg" in data else ""
    estate = "block" if emsg else "none"

    html = html.format(error_msg=emsg, error_viz=estate)
    return html


def error_page(data):
    """data
    error_msg - str - Error message to show, can be None
    """
    html = get_html(HTML_FOLDER + "error.html")
    html = prepare(html)

    emsg = "Error Message: " + data["error_msg"] if "error_msg" in data else ""

    html = html.format(error_msg=emsg)
    return html


def dashboard_page(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    search_page - str - None or string with search results
    users_cmps - list of cortages - User created cmps rows from db
    solved_cmps - list of cortages - Competitions, solved by user
    is_op - bool - has user OP features or not
    """
    username = get_username(data)
    user_id = data['user_id'] or db.id_by_username(username)
    html = get_html(HTML_FOLDER + "dashboard.html")
    html = prepare(html)

    has_search_data = False
    is_op = False
    if 'is_op' in data:
        if data['is_op']:
            is_op = data['is_op']

    search_list = ""
    if 'search_page' in data:
        if data['search_page']:
            search_list = data['search_page']
            has_search_data = True

    user_created_list = ""
    if 'users_cmps' in data:
        if data['users_cmps']:
            user_created_list = _cmp_info(data['users_cmps'], user_id)

    user_solved_list = ""
    if 'solved_cmps' in data:
        if data['solved_cmps']:
            user_solved_list = _cmp_info(data['solved_cmps'], None)

    html = html.format(
        username=username,
        search_list=search_list,
        user_created_list=user_created_list,
        user_solved_list=user_solved_list,
        search_comment_start="" if has_search_data is True else "<!--",
        search_comment_end="" if has_search_data is True else "-->",
        create_cmp_comment_start="" if is_op is True else "<!--",
        create_cmp_comment_end="" if is_op is True else "-->"
    )
    return html


def create_cmp_page(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    """
    username = get_username(data)
    html = get_html(HTML_FOLDER + "cmp_create.html")
    html = prepare(html)

    html = html.format(username=username)
    return html


def create_questions_page(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    title - str - Title of newly created competition
    description - str - Description of this competition
    qnumber - int - Number of questions to create
    """
    username = get_username(data)
    html = get_html(HTML_FOLDER + "cmp_questions.html")
    htpl = get_html(HTML_FOLDER + "cmp_questions_tpl.html")
    html = prepare(html)

    hquestions = "\n".join(
        htpl.format(id=i, id_ui=i+1) for i in range(data["qnumber"])
    )

    html = html.format(
        username=username,
        question_list=hquestions,
        title=data["title"],
        description=data["description"],
        qnumber=data["qnumber"]
    )
    return html


def solve_page(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    cmp_id - int - ID of this competition
    title - str - Title of competition
    description - str - Description of competition
    questions - list of cortages:
        [(task_id, "question text"), ...]
        EXAMPLE:
            [(45, "Test Question 1"), (87, "Test Question 2")]
    """
    username = get_username(data)
    html = get_html(HTML_FOLDER + "solve_quiz.html")
    htpl = get_html(HTML_FOLDER + "solve_tpl.html")
    html = prepare(html)

    hanswers = "\n".join(
        htpl.format(
            index=i+1,
            question=j[1],
            task_id=j[0]
        ) for i, j in enumerate(data["questions"]))

    html = html.format(
        username=username,
        answer_list=hanswers,
        cmp_id=str(data["cmp_id"]),
        title=data["title"],
        description=data["description"]
    )
    return html


def results_page(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    cmp_id - int - ID of this competition
    title - str - Title of competition
    description - str - Description of competition
    is_cmp_author - bool - Who sees this page - user, who created or solved
    results - list of cortages:
        [(task_id, "question text", user_ans_id, "user_answer", result), ...]
        EXAMPLE:
            [(45, "Test Question 1", 135, "Test User Answer 1", True),
                (87, "Test Question 2", 136, "Test User Answer 2", False)]
    """
    username = get_username(data)
    html = get_html(HTML_FOLDER + "results.html")
    htpl = get_html(HTML_FOLDER + "results_tpl.html")
    html = prepare(html)

    htable = "\n".join(
        htpl.format(
            question_index=i+1,
            question_text=j[1],
            answer=j[3],
            result="Right" if j[4] else "Wrong",
            class_name="" if j[4] else "pure-table-odd"
        ) for i, j in enumerate(data["results"])
    )

    all_count = htable.count("class")
    right_count = all_count - htable.count("pure-table-odd")

    right_percent = (right_count / all_count) * 100
    wrong_percent = 100 - right_percent

    html = html.format(
        username=username,
        table_list=htable,
        title=data["title"],
        right_percent=round(right_percent, 1),
        wrong_percent=round(wrong_percent, 1),
        user_viz="none" if data['is_cmp_author'] else "block",
        author_viz="block" if data['is_cmp_author'] else "none"
    )
    return html


def search_page(data):
    """data
    results - list of cortages, from db
    """
    snf_path = HTML_FOLDER + "search_not_found.html"
    return _cmp_info(data['results'], None) or get_html(snf_path)


def _cmp_info(cmps, user_id):
    """cmps - list of cortages - from db
    user_id - int - can be None, used to check, can user edit or not
    """
    if len(cmps):
        html = get_html(HTML_FOLDER + "search_tpl.html")

        a = "<!--"
        b = ""
        c = "-->"
        d = True if (user_id) else False

        hr = "\n".join(
            html.format(
                id=j[0],
                title=j[1],
                description=j[2],
                author_options_start=b if d and (j[3] == user_id) else a,
                author_options_end=b if d and (j[3] == user_id) else c
            ) for i, j in enumerate(cmps)
        )
        return hr
    else:
        return ""


def cmp_edit(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    cmp_id - int - ID of this competition
    title - str - Title of created competition
    description - str - Description of this competition
    questions - list of cortages:
        [(task_id, "question text", "right answer"), ...]
        EXAMPLE:
            [(45, "Test Question 1", "Test Answer 1"),
                (87, "Test Question 2", "Test Answer 2")]
    """
    username = get_username(data)
    html = get_html(HTML_FOLDER + "cmp_edit.html")
    htpl = get_html(HTML_FOLDER + "cmp_edit_tpl.html")
    html = prepare(html)

    hquestions = "\n".join(
        htpl.format(
            id=i,
            id_ui=i+1,
            question=j[1],
            answer=j[2]
        ) for i, j in enumerate(data['questions'])
    )

    html = html.format(
        username=username,
        question_list=hquestions,
        title=data["title"],
        description=data["description"],
        id=str(data["cmp_id"])
    )
    return html


def cmp_participants_page(data):
    """data
    user_id - int - Currently logined user id
    user_name - str - Currently logined user name(only if user_id is not given)
    cmp_id - int - ID of this competition
    title - str - Title of created competition
    description - str - Description of this competition
    users - list of cortages:
        [user_id_1, user_id_2, ...]
        EXAMPLE:
            [2, 45, 67]
    """
    username = get_username(data)
    html = get_html(HTML_FOLDER + "participants.html")
    htpl = get_html(HTML_FOLDER + "participants_tpl.html")
    html = prepare(html)

    hparts = "\n".join(
        htpl.format(
            uid=j,
            uname=db.username_by_id(j),
            cmp_id=data['cmp_id']
        ) for i, j in enumerate(data['users'])
    )

    html = html.format(
        username=username,
        part_list=hparts,
        title=data["title"],
        description=data["description"]
    )
    return html


def get_html(path):
    with open(path) as ifile:
        return ifile.read()


class BlankFormatter(string.Formatter):
    def get_value(self, key, args, kwds):
# TODO: make solution right
        if key not in kwds:
            return "{"+key+"}"
        else:
            return kwds.get(key)


def prepare(base):
    base = header(base)
    base = toolbar_default(base)
    base = toolbar_tpl(base)
    base = toolbar_user_tpl(base)
    return base


def header(base):
    html = get_html(HTML_FOLDER + "header_tpl.html")
    fmt = BlankFormatter()
    replaces = {
        'header_tpl': html
    }
    base = fmt.format(
        base,
        **replaces
    )
    return base


def toolbar_default(base):
    html = get_html(HTML_FOLDER + "toolbar_default.html")
    fmt = BlankFormatter()
    replaces = {
        'toolbar_default': html
    }
    base = fmt.format(
        base,
        **replaces
    )
    return base


def toolbar_tpl(base):
    html = get_html(HTML_FOLDER + "toolbar_tpl.html")
    fmt = BlankFormatter()
    replaces = {
        'toolbar_tpl': html
    }
    base = fmt.format(
        base,
        **replaces
    )
    return base


def toolbar_user_tpl(base):
    html = get_html(HTML_FOLDER + "toolbar_user_tpl.html")
    fmt = BlankFormatter()
    replaces = {
        'toolbar_user_tpl': html
    }
    base = fmt.format(
        base,
        **replaces
    )
    return base


def get_username(data):
    username = ""
    if "user_name" in data:
        username = data["user_name"]
    elif "user_id" in data:
        username = db.username_by_id(data["user_id"])
    else:
        username = "Failed to fetch user name"
    return username

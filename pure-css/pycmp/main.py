#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Kononov Arseniy and Boyarshin Andrew
# version: 0.1

import cgi
import urllib
import traceback
import auth
import ui
import db
import creator
import solver
import common


def main_page(env, headers):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        headers.append(('Location', '/dashboard'))
    else:
        query_data = _get_query_data(env)
        if 'error_msg' in query_data:
            return ui.main_page({'error_msg': query_data['error_msg'][0]})
        else:
            return ui.main_page({})
    return ''


def login(env, headers):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        headers.append(('Location', '/dashboard'))
    else:
        post_data = _get_post_data(env)
        if ('password' in post_data) and ('username' in post_data):
            password = post_data['password'][0]
            username = post_data['username'][0]
            user_id = auth.login(username, password, headers)
            if user_id is None:
                error_msg = urllib.parse.quote('Wrong username or password')
                location = '/?error_msg={}'.format(error_msg)
                headers.append(('Location', location))
            else:
                headers.append(('Location', '/dashboard'))
        else:
            error_msg = urllib.parse.quote('Username or password is not given')
            location = '/?error_msg={}'.format(error_msg)
            headers.append(('Location', location))
    return ''


def logout(env, headers):
    cookies = _get_cookies(env)
    auth.logout(headers, cookies)
    headers.append(('Location', '/'))
    return ''


def register(env, headers):
    post_data = _get_post_data(env)
    if ('password' in post_data) and ('username' in post_data):
        password = post_data['password'][0]
        username = post_data['username'][0]
        if auth.register(username, password) is None:
            error_msg = urllib.parse.quote('Registration failed')

            err_msg = "Guest tried to register '{}' and failed"
            err_msg = err_msg.format(str(username))
            common.dbg_log(err_msg)

            location = '/?error_msg={}'.format(error_msg)
            headers.append(('Location', location))
        else:
            auth.login(username, password, headers)
            headers.append(('Location', '/dashboard'))
    else:
        error_msg = urllib.parse.quote('Username or password is not given')
        location = '/?error_msg={}'.format(error_msg)
        headers.append(('Location', location))
    return ''


def dashboard(env, headers):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        headers.append(('Location', '/dashboard'))
        post_data = _get_post_data(env)
        search_list = None
        if 'search' in post_data:
            request = post_data['search'][0]
            search_list = ui.search_page({'results': common.search(request)})
        cond_f = 'user_id={}'
        cond = cond_f.format(user_id)
        users_cmps = db.select('cmps', cond)
        user_answers = db.select('user_answers', cond)
        cond_f = 'id={}'
        solved_cmps = []
        used_tasks = {None}
        for user_answer in user_answers:
            cond = cond_f.format(user_answer[2])
            task_id = db.select('questions', cond)[0][2]
            if not (task_id in used_tasks):
                used_tasks.add(task_id)
                cond = cond_f.format(db.select('questions', cond)[0][2])
                solved_cmps += db.select('cmps', cond)
        return ui.dashboard_page({
            'user_id': user_id,
            'search_page': search_list,
            'users_cmps': users_cmps,
            'solved_cmps': solved_cmps,
            'is_op': auth.is_op(user_id)
        })
    else:
        headers.append(('Location', '/'))
    return ''


def new_cmp(env, headers):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        if auth.is_op(user_id):
            return ui.create_cmp_page({'user_id': user_id})
        else:
            err_msg = "User ID {} tried to create cmp without op"
            err_msg = err_msg.format(str(user_id))
            common.dbg_log(err_msg)
            em = '403: You don\'t have permissions to create competition'
            return (ui.error_page({'error_msg': em}), '403 Forbidden')
    else:
        headers.append(('Location', '/'))
    return ''


def new_questions(env, headers):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        if auth.is_op(user_id):
            post_data = _get_post_data(env)
            title = post_data['title'][0]
            description = post_data['description'][0]
            qnumber = int(post_data['qnumber'][0])
            return ui.create_questions_page({
                'user_id': user_id,
                'qnumber': qnumber,
                'title': title,
                'description': description})
        else:
            err_msg = "User ID {} tried to create cmp without op"
            err_msg = err_msg.format(str(user_id))
            common.dbg_log(err_msg)
            em = '403: You don\'t have permissions to create competition'
            return (ui.error_page({'error_msg': em}), '403 Forbidden')
    else:
        headers.append(('Location', '/'))
    return ''


def create_cmp(env, headers):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        if auth.is_op(user_id):
            post_data = _get_post_data(env)
            checks = ('title' in post_data) and ('description' in post_data)
            if checks and ('qnumber' in post_data):
                title = common.escape(post_data['title'][0])
                description = common.escape(post_data['description'][0])
                qnumber = int(common.escape(post_data['qnumber'][0]))
                format_q = 'question-{}'
                format_a = 'answer-{}'
                tasks = []
                for i in range(qnumber):
                    question_tpl = format_q.format(i)
                    answer_tpl = format_a.format(i)
                    if (answer_tpl in post_data) and (question_tpl in post_data):
                        q = post_data[question_tpl][0]
                        a = post_data[answer_tpl][0]
                        answers = common.escape(a).split('##')
                        answers = [j for j in answers if j]
                        tasks.append(
                            tuple(
                                [common.escape(q)] + answers
                            ))
                username = db.username_by_id(user_id)
                creator.create(title, description, username, tuple(tasks))
                headers.append(('Location', '/dashboard'))
        else:
            err_msg = "User ID {} tried to create cmp without op"
            err_msg = err_msg.format(str(user_id))
            common.dbg_log(err_msg)
            em = '403: You don\'t have permissions to create competition'
            return (ui.error_page({'error_msg': em}), '403 Forbidden')
    else:
        headers.append(('Location', '/'))
    return ''


def cmp_page(env, headers, cmp_id):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        sql_str = 'id={}'
        sql_str = sql_str.format(cmp_id)
        rows = db.select('CMPS', sql_str)
        if rows and len(rows):
            row = rows[0]
            if common.is_user_solve_cmp(cmp_id, user_id):
                headers.append(('Location', '/quiz/{}/results'.format(cmp_id)))
            else:
                username = db.username_by_id(user_id)
                sql_str = 'cmp_id={}'
                sql_str = sql_str.format(cmp_id)
                questions = [(r[0], r[1]) for r in db.select('QUESTIONS', sql_str)]
                return ui.solve_page({
                    'cmp_id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'user_name': username,
                    'questions': questions})
        else:
            err_msg = "User ID {} tried to solve non-existing cmp {}"
            err_msg = err_msg.format(str(user_id), str(cmp_id))
            common.dbg_log(err_msg)
            return (ui.error_page({'error_msg': '404: Competition not found'}), '404 Not Found')
    else:
        headers.append(('Location', '/'))
    return ''


def cmp_solve(env, headers, cmp_id):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        sql_str = 'id={}'
        sql_str = sql_str.format(cmp_id)
        rows = db.select('CMPS', sql_str)
        if rows:
            post_data = _get_post_data(env)
            format_a = 'answer-{}'
            sql_str = 'cmp_id={}'
            sql_str = sql_str.format(cmp_id)
            answers = (
                (r[0], common.escape(post_data[format_a.format(r[0])][0]))
                for r in db.select('QUESTIONS', sql_str))
            username = db.username_by_id(user_id)
            solver.save_answers(username, answers, cmp_id)
            headers.append(('Location', '/quiz/{}/results'.format(cmp_id)))
        else:
            err_msg = "User ID {} tried to solve non-existing cmp {}"
            err_msg = err_msg.format(str(user_id), str(cmp_id))
            common.dbg_log(err_msg)
            return (ui.error_page({'error_msg': '404: Competition not found'}), '404 Not Found')
    else:
        headers.append(('Location', '/'))
    return ''


def cmp_results(env, headers, cmp_id):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    logineduid = user_id
    if user_id is not None:
        cond_f = 'id={}'
        cond = cond_f.format(cmp_id)
        rows = db.select('CMPS', cond)
        if rows:
            row = rows[0]
            qs = _get_query_data(env)
            is_cmp_author = False
            if 'uid' in qs:
                uid = int(qs['uid'][0])
                if (uid != user_id) and (row[3] == user_id):
                    user_id = uid
                    is_cmp_author = True
            if common.is_user_solve_cmp(cmp_id, user_id):
                username = db.username_by_id(logineduid)
                cond_f = 'cmp_id={}'
                cond = cond_f.format(cmp_id)
                tasks = db.select('questions', cond)
                answers = common.user_answers_for_cmp(cmp_id, user_id)
                restuple = solver.is_cmp_right(cmp_id, answers)
                results = [
                    (task[0], task[1], ans[0], ans[3], res)
                    for task, ans, res in zip(tasks, answers, restuple)]
                return ui.results_page({
                    'cmp_id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'user_name': username,
                    'results': results,
                    'is_cmp_author': is_cmp_author})
            else:
                headers.append(('Location', '/quiz/{}'.format(cmp_id)))
                err_msg = "User ID {} tried to see result for non-solved cmp {}"
                err_msg = err_msg.format(str(user_id), str(cmp_id))
                common.dbg_log(err_msg)
        else:
            err_msg = "User ID {} tried to view result for non-existing cmp {}"
            err_msg = err_msg.format(str(user_id), str(cmp_id))
            common.dbg_log(err_msg)
            return (ui.error_page({'error_msg': '404: Competition not found'}), '404 Not Found')
    else:
        headers.append(('Location', '/'))
    return ''


def cmp_edit(env, headers, cmp_id):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        cond = 'id={}'.format(cmp_id)
        cmp_rows = db.select('CMPS', cond)
        if cmp_rows:
            cmp_row = cmp_rows[0]
            if cmp_row[3] == user_id:
                title = cmp_row[1]
                description = cmp_row[2]
                cond = 'cmp_id={}'.format(cmp_id)
                tasks = db.select('QUESTIONS', cond)
                tcond = 'task_id={}'
                questions = [
                    (
                        task[0], task[1],
                        '##'.join(
                            answer[1]
                            for answer in
                            db.select('answers', tcond.format(task[0]))
                        )
                    )
                    for task in tasks
                ]
                headers.append(('Location', '/quiz/{}/edit'.format(cmp_id)))
                return ui.cmp_edit({
                    'cmp_id': cmp_id,
                    'title': title,
                    'description': description,
                    'user_id': user_id,
                    'questions': questions
                })
            else:
                err_msg = "User ID {} tried to edit cmp {} without access"
                err_msg = err_msg.format(str(user_id), str(cmp_id))
                common.dbg_log(err_msg)
                em = '403: You don\'t have permissions to edit this competition'
                return (ui.error_page({'error_msg': em}), '403 Forbidden')
        else:
            err_msg = "User ID {} tried to edit non-existing cmp {}"
            err_msg = err_msg.format(str(user_id), str(cmp_id))
            common.dbg_log(err_msg)
            return (ui.error_page({'error_msg': '404: Competition not found'}), '404 Not Found')
    else:
        headers.append(('Location', '/'))
    return ''


def cmp_edit_save(env, headers, cmp_id):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        post_data = _get_post_data(env)
        cmp_rows = db.select('CMPS', 'id={}'.format(cmp_id))
        if cmp_rows:
            cmp_row = cmp_rows[0]
            if cmp_row[3] == user_id:
                title = cmp_row[1]
                description = post_data['description'][0]
                format_q = 'question-{}'
                format_a = 'answer-{}'
                qnumber = len(db.select('QUESTIONS', 'cmp_id={}'.format(cmp_id)))
                tasks = []
                for i in range(qnumber):
                    answers = post_data[format_a.format(i)][0].split('##')
                    answers = [common.escape(j) for j in answers if j]
                    tasks.append(
                        tuple(
                            [common.escape(post_data[format_q.format(i)][0])] +
                            answers
                        ))
                creator.edit(cmp_id, title, description, tasks)
                headers.append(('Location', '/dashboard'))
            else:
                err_msg = "User ID {} tried to edit cmp {} without access"
                err_msg = err_msg.format(str(user_id), str(cmp_id))
                common.dbg_log(err_msg)
                em = '403: You don\'t have permissions to edit this competition'
                return (ui.error_page({'error_msg': em}), '403 Forbidden')
        else:
            err_msg = "User ID {} tried to edit non-existing cmp {}"
            err_msg = err_msg.format(str(user_id), str(cmp_id))
            common.dbg_log(err_msg)
            return (ui.error_page({'error_msg': '404: Competition not found'}), '404 Not Found')
    else:
        headers.append(('Location', '/'))
    return ''


def participants(env, headers, cmp_id):
    cookies = _get_cookies(env)
    user_id = auth.is_logined(cookies)
    if user_id is not None:
        sql_str = 'id={}'
        sql_str = sql_str.format(cmp_id)
        rows = db.select('CMPS', sql_str)
        if rows:
            row = rows[0]
            if row[3] == user_id:
                cond_f = 'cmp_id={}'
                cond = cond_f.format(cmp_id)
                task = db.select('questions', cond)[0]
                cond_f = 'task_id={}'
                cond = cond_f.format(task[0])
                users = [i[1] for i in db.select('user_answers', cond)]
                return ui.cmp_participants_page({
                    'cmp_id': cmp_id,
                    'title': row[1],
                    'description': row[2],
                    'user_id': user_id,
                    'users': users
                })
            else:
                err_msg = "UID {} tried to admin cmp {} without access"
                err_msg = err_msg.format(str(user_id), str(cmp_id))
                common.dbg_log(err_msg)
                em = '403: You don\'t have permission to admin this competition'
                return (ui.error_page({'error_msg': em}), '403 Forbidden')
        else:
            err_msg = "UID {} tried to view participants of non-existing cmp {}"
            err_msg = err_msg.format(str(user_id), str(cmp_id))
            common.dbg_log(err_msg)
            return (ui.error_page({'error_msg': '404: Competition not found'}), '404 Not Found')
    else:
        headers.append(('Location', '/'))
    return ''


def choose_action(env, headers):
    """Works with paths. Selects, which page to show.
    return html - string
    """
    paths = [([''], main_page),
             (['user', 'login'], login),
             (['user', 'logout'], logout),
             (['user', 'register'], register),
             (['dashboard'], dashboard),
             (['cmp', 'create'], new_cmp),
             (['quiz', 'create', 'questions'], new_questions),
             (['contest', 'create', 'tasks'], new_questions),
             (['quiz', 'create', 'save'], create_cmp),
             (['contest', 'create', 'save'], create_cmp),
             (['quiz', (int, 'cmp_id')], cmp_page),
             (['quiz', (int, 'cmp_id'), 'solve'], cmp_solve),
             (['quiz', (int, 'cmp_id'), 'results'], cmp_results),
             (['quiz', (int, 'cmp_id'), 'edit'], cmp_edit),
             (['quiz', (int, 'cmp_id'), 'edit', 'save'], cmp_edit_save),
             (['quiz', (int, 'cmp_id'), 'participants'], participants)]

    path = env['PATH_INFO'].split('/')
    path.remove('')
    for path_f in paths:
        if len(path) != len(path_f[0]):
            continue
        vardict = {}
        for i, j in enumerate(path_f[0]):
            if type(j) == tuple:
                try:
                    vardict[j[1]] = j[0](path[i])
                except ValueError:
                    break
            elif j != path[i]:
                break
        else:
            try:
                return path_f[1](env, headers, **vardict)
            except Exception:
                common.dbg_log(traceback.format_exc())
                return (ui.error_page({'error_msg': '500: Internal Server Error'}), '500 Internal Server Error')
    common.dbg_log("Page not found: "+str(env['PATH_INFO']))
    return (ui.error_page({'error_msg': '404: Not found'}), '404 Not found')


def _get_cookies(env):
    if 'HTTP_COOKIE' in env:
        cookie = env['HTTP_COOKIE']
        return {i[0]: i[1] for i in (j.split('=') for j in cookie.split('; '))}
    return {}


def _get_post_data(env):
    if 'CONTENT_LENGTH' in env:
        Content_Length = env['CONTENT_LENGTH']
        Content_Length = 0 if Content_Length == '' else int(Content_Length)
        qsr = env['wsgi.input'].read(Content_Length)
        qs = urllib.parse.unquote(str(qsr))[2:][:-1]
        return cgi.parse_qs(qs)
    return {}


def _get_query_data(env):
    if 'QUERY_STRING' in env:
        qs = urllib.parse.unquote(env['QUERY_STRING'])
        return cgi.parse_qs(qs)


def application(env, start_response):
    headers = []
    headers.append(('Content-Type', 'text/html'))
    response_code = '200 OK'
    # common.dbg_log(str(env))
    res = choose_action(env, headers)
    if type(res) == tuple:
        res_content = res[0].encode()
        if len(res) > 1:
            response_code = res[1]
    else:
        res_content = res.encode()
    for i, j in enumerate(headers):
        if j[0] == "Location":
            if j[1] != env["PATH_INFO"]:
                response_code = "302 Moved Temporarily"
    headers.append(('Content-Length', str(len(res_content))))
    start_response(response_code, headers)
    yield res_content


if __name__ == '__main__':
    db.init_db()
    print("DB reinitialized")

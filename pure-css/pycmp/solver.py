#!/usr/bin.env python3
# -*- coding: utf-8 -*-
"""Module, that allows user to solve competitions.
Also provides ability to check answers.
"""
import db


def save_answers(username, answers, cmp_id):
    """answers - cortage of cortages (id of task, answer)
        (
            (1,'ans1'),
            (2,'ans2')
        )
    cmp_id - int - id of competition
    return True or False
    """
    user_id = db.id_by_username(username)
    is_ok = True
    for answer in answers:
        check = db.insert('USER_ANSWERS', (
            user_id, answer[0], answer[1], cmp_id))
        if check is None:
            is_ok = False
    return is_ok


def is_right(task_id, answer):
    """Is answer right.
    TODO: not fully right answers
    return True or False
    """
    cond_f = "task_id={} AND answer='{}'"
    cond = cond_f.format(task_id, answer)
    return bool(db.select('answers', cond))


def is_cmp_right(cmp_id, answers):
    """Check, which answers are right, and which aren't.
    answers - user's answers
    return check result - cortage of boolean
    answers - list of rows
    """
    check_results = []
    cmp_id_full = 'cmp_id={}'
    tasks = db.select('QUESTIONS', cmp_id_full.format(cmp_id))
    for task, answer in zip(tasks, answers):
        check_results.append(is_right(task[0], answer[3]))
    return check_results

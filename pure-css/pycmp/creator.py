#!/usr/bin.env python3
# -*- coding: utf-8 -*-
"""Module to create new competitions and work with existing ones.
"""
import db
import common


def create(title, description, username, questions):
    """Create new competition
    questions - cortage of cortages
    EXAMPLE:    (
                    ('Question1','Answer1'),
                    ('Question2','Answer2', 'Answer22')
                )
    return id or None
    """
    check = cmp_exists(title)
    common.dbg_log(str(questions))
    if check is None:
        user_id = db.id_by_username(username)
        cmp_id = db.insert('CMPS', (title, description, user_id, 0, 0))
        for task in questions:
            task_id = db.insert('QUESTIONS', (task[0], cmp_id))
            common.dbg_log(str(task_id))
            for i in range(1, len(task)):
                db.insert('ANSWERS', (task[i], task_id, cmp_id))
        return cmp_id
    else:
        return None


def cmp_exists(title):
    """Exists competition with given title or not.
    Returns id of found competition or None.
    return id or None
    """
    title_full = "title='{}'"
    res = db.select('CMPS', title_full.format(common.escape(title)))
    return res[0][0] if res else None


def edit(cmp_id, title, description, questions):
    """Edit campetition
    questions - cortage of cortages
    EXAMPLE:    (
                    ('Question1','Answer1'),
                    ('Question2','Answer2', 'Answer22')
                )
    return id or None
    """
    cmp_row = db.select('CMPS', "id={}".format(cmp_id))[0]
    vals = (title, description, cmp_row[3], cmp_row[4], cmp_row[5])
    if db.update('CMPS', cmp_id, vals):
        cmp_id_sql = "cmp_id={}".format(cmp_id)
        for task in questions:
            task_row = db.select('QUESTIONS', cmp_id_sql)[0]
            if task_row and len(task_row) and task_row[0]:
                db.update_rows('QUESTIONS', [task_row], (task[0], cmp_id))
                task_id_sql = 'task_id={}'.format(task_row[0])
                db.remove_conditions('ANSWERS', task_id_sql)
                for i in range(1, len(task)):
                    db.insert('ANSWERS', (task[i], task_row[0], cmp_id))
        return cmp_id
    else:
        return None

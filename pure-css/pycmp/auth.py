#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: kononov_arseniy
"""Authorization module.
Called from main module. Requires headers and cookies to fully function.
Password must be already encrypted on client side.
"""
import db
import random
import string
import datetime
import scrypt
import base64
import common


def register(username, password):
    """Yay! New user to our site! Let's create his account.
    Must check user existance.
    return id or None
    """
    username = common.escape(username)
    sql_str = "username='{}'"
    sql_str = sql_str.format(username)
    if db.select('USERS', sql_str):
        return None
    salt = _generate_string(32)
    pass_hash = _generate_hash(password, salt)
    return db.insert('USERS', (username, pass_hash, salt, False))


def login(username, password, headers):
    """Log in user into his account(if it is his account)
    headers - dictionary
    return id or None
    """
    username = common.escape(username)
    sql_str = "username='{}'"
    sql_str = sql_str.format(username)
    user = db.select('USERS', sql_str)
    if user:
        user = user[0]
        pass_hash = _generate_hash(password, user[3])
        if user[2] == pass_hash:
            session_id = None
            while (session_id is None) or db.select('SESSIONS', sql_str):
                session_id = _generate_string(256)
                sql_str = "session_id='{}'"
                sql_str = sql_str.format(session_id)

            td = datetime.timedelta(14)
            dt = datetime.datetime.today()
            dt = dt + td
            expires = common.utctime(dt)
            cookie = "session_id={}; expires={}; path=/"
            cookie = cookie.format(session_id, expires)
            headers.append(('Set-Cookie', cookie))

            user_id = user[0]
            db.insert('SESSIONS', (session_id, user_id))
            return user_id
    return None


def logout(headers, cookies):
    """Log out user from his account
    headers - dictionary
    cookies - dictionary
    return True or False
    """
    if 'session_id' in cookies:
        #try without session_id value
        expires_in = 'Thu, 31 Aug 1995 00:00:00 GMT'
        cookie = 'session_id={}; expires={}; path=/'
        cookie = cookie.format(cookies['session_id'], expires_in)
        headers.append(('Set-Cookie', cookie))
        sql_str = "session_id='{}'"
        sql_str = sql_str.format(cookies['session_id'])
        return db.remove_conditions('SESSIONS', sql_str)
    return False


def is_logined(cookies):
    """Check, is user now logined or not
    cookies - dictionary
    return id or None
    """
    if 'session_id' in cookies:
        sql_str = "session_id='{}'"
        sql_str = sql_str.format(cookies['session_id'])
        rows = db.select('SESSIONS', sql_str)
        return rows[0][2] if rows else None
    return None


def is_op(user_id):
    """Check, has user with given id OP rights or not
    user_id - int - user id
    return True or False
    """
    row = db.select("USERS", "id=" + str(user_id) + "")
    if len(row) and len(row[0]):
        return row[0][4]
    common.dbg_log("User with id "+str(user_id)+" not found")
    return False


def _generate_string(length):
    syms = (random.choice(string.ascii_lowercase) for i in range(length))
    return ''.join(syms)


def _generate_hash(message, salt):
    return base64.b64encode(scrypt.hash(message, salt)).decode()

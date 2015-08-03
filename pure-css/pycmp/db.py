#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Andrew Boyarshin
"""SQL data types:
 * text
 * int

For all methods, which have argument "conditions":
Conditions - sql compatible string
SAMPLES:
    username="Nick" AND password="1234"
    goats=120 OR field="value"
    work=5

For those, who want to run PyCMP on your own server - change DB_NAME, DB_USER
    and DB_PWRD constants in this(db) module.
"""
import psycopg2
import common


DB_NAME = "pycmp"
DB_USER = "postgres"
DB_PWRD = "master"
DB_HOST = "localhost"


def init_db():
    cort = _quick_cursor()
    conn = cort[0]
    cur = cort[1]
    t1 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS USERS(
        id serial PRIMARY KEY,
        username text NOT NULL,
        password text NOT NULL,
        salt text NOT NULL,
        op boolean DEFAULT FALSE
    );''')
    t2 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS CMPS(
        id serial PRIMARY KEY,
        title text NOT NULL,
        description text NOT NULL,
        user_id int NOT NULL REFERENCES USERS(id),
        start_time int NOT NULL,
        end_time int NOT NULL
    );''')
    t3 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS QUESTIONS(
        id serial PRIMARY KEY,
        question text NOT NULL,
        cmp_id int NOT NULL REFERENCES CMPS(id)
    );''')
    t4 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS ANSWERS(
        id serial PRIMARY KEY,
        answer text NOT NULL,
        task_id int NOT NULL REFERENCES QUESTIONS(id),
        cmp_id int NOT NULL REFERENCES CMPS(id)
    );''')
    t5 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS USER_ANSWERS(
        id serial PRIMARY KEY,
        user_id int NOT NULL REFERENCES USERS(id),
        task_id int NOT NULL REFERENCES QUESTIONS(id),
        answer text NOT NULL,
        cmp_id int NOT NULL REFERENCES CMPS(id)
    );''')
    t6 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS SESSIONS(
        id serial PRIMARY KEY,
        session_id text NOT NULL,
        user_id int NOT NULL REFERENCES USERS(id)
    );''')
    t7 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS CONTESTS(
        id serial PRIMARY KEY,
        title text NOT NULL,
        description text NOT NULL,
        user_id int NOT NULL REFERENCES USERS(id),
        start_time int NOT NULL,
        end_time int NOT NULL
    );''')
    t8 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS TASKS(
        id serial PRIMARY KEY,
        title text NOT NULL,
        description text NOT NULL,
        cmp_id int NOT NULL REFERENCES CONTESTS(id)
    );''')
    t9 = cur.mogrify('''
    CREATE TABLE IF NOT EXISTS SOLUTIONS(
        id serial PRIMARY KEY,
        user_id int NOT NULL REFERENCES USERS(id),
        task_id int NOT NULL REFERENCES TASKS(id),
        result text NOT NULL,
        cmp_id int NOT NULL REFERENCES CONTESTS(id),
        log text NOT NULL
    );''')
    cur.execute(t1)
    cur.execute(t2)
    cur.execute(t3)
    cur.execute(t4)
    cur.execute(t5)
    cur.execute(t6)
    cur.execute(t7)
    cur.execute(t8)
    cur.execute(t9)
    conn.commit()
    cur.close()
    conn.close()
    return True


def create(table_name, fields):
    """Create table in our database
    table_name - str
    fields - sql compat string with column names and theirs types
                 WITHOUT ID COLUMN (SERIAL TYPE):
        AS:      field_name field_type, field_2_name field_2_type
        EXAMPLE: field2 text, field3 int
    return True or False
    """
    if fields and len(fields):
        cort = _quick_cursor()
        conn = cort[0]
        cur = cort[1]
        sql_str = "CREATE TABLE {} (id serial PRIMARY KEY, {});"
        sql_str = sql_str.format(table_name, fields)
        req = cur.mogrify(sql_str)
        cur.execute(req)
        conn.commit()
        cur.close()
        conn.close()
        return True
    common.dbg_log("db.create got None or Empty fields")
    return False


def insert(table_name, values):
    """Insert row in table
    table_name - str
    values - cortage, contains values to insert
    return id or None
    """
    if values and len(values):
        cort = _quick_cursor()
        conn = cort[0]
        cur = cort[1]
        sql_str = "INSERT INTO {} VALUES (DEFAULT{});"
        sql_str = sql_str.format(table_name, _pack_str_args(values))
        req = cur.mogrify(sql_str, values)
        cur.execute(req)
        conn.commit()
        d = _cortage_to_dictionary(table_name, values)
        vals = ""
        for i, j in d.items():
            vals += str(i) + " = "
            vals += "'"+str(j)+"'"
            vals += " AND "
        vals = vals[:-5]
        rows = select(table_name, vals)
        res = int(rows[0][0])
        cur.close()
        conn.close()
        return res
    common.dbg_log("db.insert got None or Empty values")
    return None


def remove(table_name, id):
    """Remove row by id
    table_name - str
    id - int
    return True or False
    """
    rows = select(table_name, "id="+str(id))
    return remove_rows(table_name, rows)


def update(table_name, id, values):
    """Update row by id with given values
    table_name - str
    id - int
    values - cortage !in the order of table columns!
    return True or False
    """
    rows = select(table_name, "id="+str(id))
    return update_rows(table_name, rows, values)


def remove_conditions(table_name, conditions):
    """Remove row by given conditions (uses select function)
    table_name - str
    conditions - str, read module description
    return True or False
    """
    rows = select(table_name, conditions)
    return remove_rows(table_name, rows)


def update_conditions(table_name, conditions, values):
    """Update row by given conditions
    table_name - str
    conditions - str, read module description
    values - cortage !in the order of table columns!
    return True or False
    """
    rows = select(table_name, conditions)
    return update_rows(table_name, rows, values)


def remove_rows(table_name, rows):
    """Update and remove by given rows
    table_name - str
    return True or False
    """
    if len(rows):
        cort = _quick_cursor()
        conn = cort[0]
        cur = cort[1]
        ids = ""
        for c in rows:
            ids += "id = " + str(c[0]) + " OR "
        ids = ids[:-4]
        if len(ids):
            sql_str = "DELETE FROM {} WHERE {};"
            sql_str = sql_str.format(table_name, ids)
            req = cur.mogrify(sql_str)
            cur.execute(req)
            res = int(cur.statusmessage.replace("DELETE ", ""))
            conn.commit()
            cur.close()
            conn.close()
            return res > 0
        else:
            common.dbg_log("db.remove_rows ids were empty")
            return False
    common.dbg_log("db.remove_rows got None or Empty rows")
    return False


def update_rows(table_name, rows, values):
    """table_name - str
    rows - list of cortages(e.g. from select function)
    values - cortage !in the order of table columns!
    return True or False
    """
    if len(rows):
        cort = _quick_cursor()
        conn = cort[0]
        cur = cort[1]
        d = _cortage_to_dictionary(table_name, values)
        vals = ""
        for i, j in d.items():
            vals += str(i) + " = '" + str(j) + "', "
        vals = vals[:-2]
        ids = ""
        for c in rows:
            ids += "id = " + str(c[0]) + ", "
        ids = ids[:-2]
        if len(ids):
            sql_str = "UPDATE {} SET {} WHERE {};"
            sql_str = sql_str.format(table_name, vals, ids)
            req = cur.mogrify(sql_str)
            cur.execute(req)
            res = int(cur.statusmessage.replace("UPDATE ", ""))
            conn.commit()
            cur.close()
            conn.close()
            return res > 0
        else:
            common.dbg_log("db.update_rows ids were empty")
            return False
    common.dbg_log("db.update_rows got None or Empty rows")
    return False


def select(table_name, conditions):
    """Finds row, that conforms given condition. To be used by all modules.
    table_name - str
    conditions - str, read module description
    return  list of cortages - rows
    """
    if conditions and len(conditions):
        cort = _quick_cursor()
        conn = cort[0]
        cur = cort[1]
        sql_str = "SELECT * FROM {} WHERE {};"
        sql_str = sql_str.format(table_name, conditions)
        req = cur.mogrify(sql_str)
        cur.execute(req)
        row = cur.fetchall()
        cur.close()
        conn.close()
        return row
    else:
        common.dbg_log("db.select got None or Empty conditions")
        return []


def id_by_username(username):
    """Get id of user by given name
    return id or None
    """
    row = select("USERS", "username='" + str(username) + "'")
    if len(row) and len(row[0]):
        return row[0][0]
    return None


def username_by_id(id):
    """Get name of user by given id
    return username
    """
    row = select("USERS", "id=" + str(id))
    if len(row) and len(row[0]):
        return row[0][1]
    return None

#####################################################
#
# FOR INTERNAL USE ONLY, DO NOT USE IN OTHER MODULES!
#
#####################################################


def _quick_cursor():
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PWRD, host=DB_HOST)
    cur = conn.cursor()
    return (conn, cur)


def _cortage_to_dictionary(table_name, cortage):
    d = {}
    cl = len(cortage)
    sc = -1
    if (table_name == "USERS"):
        if (cl == 5):
            d['id'] = cortage[0]
            sc = 0
        d['username'] = cortage[sc + 1]
        d['password'] = cortage[sc + 2]
        d['salt'] = cortage[sc + 3]
        d['op'] = cortage[sc + 4]
    elif (table_name == "CMPS"):
        if (cl == 6):
            d['id'] = cortage[0]
            sc = 0
        d['title'] = cortage[sc + 1]
        d['description'] = cortage[sc + 2]
        d['user_id'] = cortage[sc + 3]
        d['start_time'] = cortage[sc + 4]
        d['end_time'] = cortage[sc + 5]
    elif (table_name == "QUESTIONS"):
        if (cl == 3):
            d['id'] = cortage[0]
            sc = 0
        d['question'] = cortage[sc + 1]
        d['cmp_id'] = cortage[sc + 2]
    elif (table_name == "ANSWERS"):
        if (cl == 4):
            d['id'] = cortage[0]
            sc = 0
        d['answer'] = cortage[sc + 1]
        d['task_id'] = cortage[sc + 2]
        d['cmp_id'] = cortage[sc + 3]
    elif (table_name == "USER_ANSWERS"):
        if (cl == 5):
            d['id'] = cortage[0]
            sc = 0
        d['user_id'] = cortage[sc + 1]
        d['task_id'] = cortage[sc + 2]
        d['answer'] = cortage[sc + 3]
        d['cmp_id'] = cortage[sc + 4]
    elif (table_name == "SESSIONS"):
        if (cl == 3):
            d['id'] = cortage[0]
            sc = 0
        d['session_id'] = cortage[sc + 1]
        d['user_id'] = cortage[sc + 2]
    elif (table_name == "CONTESTS"):
        if (cl == 6):
            d['id'] = cortage[0]
            sc = 0
        d['title'] = cortage[sc + 1]
        d['description'] = cortage[sc + 2]
        d['user_id'] = cortage[sc + 3]
        d['start_time'] = cortage[sc + 4]
        d['end_time'] = cortage[sc + 5]
    elif (table_name == "TASKS"):
        if (cl == 4):
            d['id'] = cortage[0]
            sc = 0
        d['title'] = cortage[sc + 1]
        d['description'] = cortage[sc + 2]
        d['cmp_id'] = cortage[sc + 3]
    elif (table_name == "SOLUTIONS"):
        if (cl == 6):
            d['id'] = cortage[0]
            sc = 0
        d['user_id'] = cortage[sc + 1]
        d['task_id'] = cortage[sc + 2]
        d['result'] = cortage[sc + 3]
        d['cmp_id'] = cortage[sc + 4]
        d['log'] = cortage[sc + 5]
    return d


def _dictionary_to_cortage(table_name, d):
    cortage = ()
    if (table_name == "USERS"):
        cortage = (d['id'], d['username'], d['password'], d['salt'], d['op'])
    elif (table_name == "CMPS"):
        cortage = (
            d['id'], d['title'], d['description'], d['user_id'],
            d['start_time'], d['end_time'])
    elif (table_name == "QUESTIONS"):
        cortage = (d['id'], d['question'], d['cmp_id'])
    elif (table_name == "ANSWERS"):
        cortage = (d['id'], d['answer'], d['task_id'], d['cmp_id'])
    elif (table_name == "USER_ANSWERS"):
        cortage = (
            d['id'], d['user_id'], d['task_id'], d['answer'], d['cmp_id'])
    elif (table_name == "SESSIONS"):
        cortage = (d['id'], d['session_id'], d['user_id'])
    elif (table_name == "CONTESTS"):
        cortage = (
            d['id'], d['title'], d['description'], d['user_id'],
            d['start_time'], d['end_time'])
    elif (table_name == "TASKS"):
        cortage = (d['id'], d['title'], d['description'], d['cmp_id'])
    elif (table_name == "SOLUTIONS"):
        cortage = (
            d['id'], d['user_id'], d['task_id'], d['result'], d['cmp_id'],
            d['log'])
    return cortage


def _pack_str_args(values):
    return ''.join((', %s' for i in values))


def _dbg():
    init_db()
    res = insert("USERS", ("Test User", "12345", "ab", "DEFAULT"))
    if res:
        print("Inserted " + str(res))
        if (update("USERS", res, ("Test User Modified", "123", "bl", "DEFAULT"))):
            print("Updated user successfully")
            un = username_by_id(res)
            row = select("USERS", "username='"+un+"'")
            if (remove_rows("USERS", row)):
                print("Row removed")
            else:
                print("Row not removed")
        else:
            print("Update user failed")
    else:
        print("Failed")


if __name__ == '__main__':
    _dbg()

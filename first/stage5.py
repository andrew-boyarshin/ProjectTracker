#!/usr/bin/python3
# coding: utf-8

"""
stage 5 v0.1
author : nev
27.07.2015
"""

# TODO:
#

# OK:
# 

from common import *


# *******VISIBLE PAGES***********************************************************************************


@app.get('/archive/')
@app.get('/archive')
def archive_main():
    arh = [i for i in Archive.select()]
    return template ('first/archive_main.tpl', arh=arh,
        ver=PROJECT_VERSION, date=str(datetime.now())[:-7])

@app.get('/archive/<pr_id:int>/')
@app.get('/archive/<pr_id:int>')
def finish_page(pr_id):
    pr = [i for i in Archive.select().where(Archive.id == pr_id)]
    if len(pr) == 0:
        redirect('/projects/')
    return template('first/finish_page.tpl', pr=pr[0],
                    ver=PROJECT_VERSION, date=str(datetime.now())[:-7])


@app.get('/archive/<pr_id:int>/stat')
@app.get('/archive/<pr_id:int>/stat/')
def finish_page(pr_id):
    pr = [i for i in Archive.select().where(Archive.id == pr_id)]
    if len(pr) == 0:
        redirect('/projects/')
    return template('first/finish_stat.tpl', pr=pr[0],
                    ver=PROJECT_VERSION, date=str(datetime.now())[:-7])

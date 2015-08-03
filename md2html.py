#!/usr/bin/python3
#coding: utf-8

"""
converter of markdown to html v0.1
author : nev
22.07.2015
"""

# TODO:
# 
# Nothing.

# OK:
# 
# headers
# tables
# comments
# lists
# links []()
# <p>
# bold + italic
# lists with -
# headers with #
# check spaces before end tags

import re


def md2html_line (md): 
    md = re.sub(r'[\[]([^\)\]]*)[\]][\(]([^\)\]]*)[\)]', r'<a href="\2">\1</a>', md)
    md += ' '
    pred = ''
    mode = ['6']
    stack = ['']
    for ch in md:
        if ch in ('_', '*'):
            pred += ch
        else:
            if pred != '': 
                if len(mode) == 1 and ch != ' ':
                     while (pred):
                        while pred.startswith (('**', '__')):
                            mode.append (pred[:2])
                            stack.append ('')
                            pred = pred[2:]
                        while pred.startswith (('*', '_')):
                            mode.append (pred[0])
                            stack.append ('')
                            pred = pred[1:]
                elif len (mode) > 1 and not stack[-1].endswith (' '):
                    while (pred.startswith (mode[-1]) or pred.startswith (mode[-1].replace ('*', '_'))):
                        if mode[-1] == '**' or mode[-1] == '__':
                            stack[-2] += '<b>' + stack[-1] + '</b>'
                            del stack[-1]
                            del mode[-1]
                            pred = pred[2:]
                        elif mode[-1] == '*' or mode[-1] == '_':
                            stack[-2] += '<i>' + stack[-1] + '</i>'
                            del stack[-1]
                            del mode[-1]
                            pred = pred[1:]
                    while (pred):
                        while pred.startswith (('**', '__')):
                            mode.append (pred[:2])
                            stack.append ('')
                            pred = pred[2:]
                        while pred.startswith (('*', '_')):
                            mode.append ('*')
                            stack.append ('')
                            pred = pred[1:]
                else:
                    stack[-1] += pred
                    pred = ''
            stack[-1] += ch
    for i in range (len (mode) - 1, 0, -1):
        stack[i - 1] += mode[i] + stack[i]
    return stack[0].strip()



def md2html (md):
    lines = md.split ('\n')
    # good !
    lines.append ('')
    lines.append ('')

    res_list = [[None, None, False]]
    sub_res_list = [[None, None, None, False]]

    pred = lines[0]
    stack = ['']
    md_stack = ''
    mode = ['7']
    spaces = [-2]
    req_new_str = True
    is_table = False
    table_str = ''
    for i in lines[1:]:
        # print (res_list, sub_res_list)
        if (pred.startswith('.')):
            md_stack += pred + '\n'
            stack[-1] += '<br>' + pred[1:] + '</br>'
            pred = i
            continue
        if is_table:
            if pred.strip() == '':
                is_table = False
                stack[-1] += '<table>' + table_str + '</table>'
                table_str = ''
            else:
                table_str += '<tr>'
                for x in pred.split (' | '):
                    table_str += '<td>' + md2html_line (x) + '</td>'
                table_str += '</tr>'
            md_stack += pred + '\n'
            pred = i
        elif pred.startswith ('T--'):
            md_stack += pred + '\n'
            is_table = True
            pred = i
        elif i.count ('=') >= len (pred) and i.count ('=') > 1 and i.startswith ('='):
            # stack[-1] += '<h1>' + pred + '</h1>'
            req_new_str = False
            if (stack[-1] != ''):
                sub_res_list[-1][1] = stack[-1]
                sub_res_list[-1][2] = md_stack
            res_list[-1][1] = sub_res_list
            res_list.append ([pred, None, True])
            sub_res_list = [[None, None, None, False]]
            stack[-1] = ''
            md_stack = ''
            pred = ''
        elif i.count ('-') >= len (pred) and i.count ('-') > 1 and i.startswith ('-'):
            # stack[-1] += '<h2>' + pred + '</h2>'
            req_new_str = False
            sub_res_list[-1][1] = stack[-1]
            sub_res_list[-1][2] = md_stack
            sub_res_list.append ([pred, None, None, True])
            stack[-1] = ''
            md_stack = ''
            pred = ''
        elif pred.startswith ('#'):
            for j in range (len (stack) - 1, 0, -1):
                    if mode[-1] == 'ol>':
                        stack[-2] += '<' + mode[-1] + stack[-1] + '</' + mode[-1]
                        del stack[-1]
                        del mode[-1]
                        del spaces[-1] 
                    elif mode[-1] == 'ul>':
                        stack[-2] += '<' + mode[-1] + stack[-1] + '</' + mode[-1]
                        del stack[-1]
                        del mode[-1]
                        del spaces[-1] 
            x = pred.lstrip ('#')
            level = len (pred) - len (x)
            x = x.rstrip ('#')
            if (level) == 1:
                if (stack[-1] != ''):
                    sub_res_list[-1][1] = stack[-1]
                    sub_res_list[-1][2] = md_stack
                    sub_res_list.append ([None, None, None, False])
                res_list[-1][1] = sub_res_list
                res_list.append ([x, None, False])
                sub_res_list = [[None, None, None, False]] 
                stack[-1] = ''
                md_stack = ''
            elif level == 2:
                sub_res_list[-1][1] = stack[-1]
                sub_res_list[-1][2] = md_stack
                sub_res_list.append ([x, None, None, False])
                stack[-1] = ''
                md_stack = ''
            else:
                md_stack += pred
                stack[-1] += '<h' + str (level) + '>' + x + '</h' + str (level) + '>'
            pred = i
            req_new_str = False
        else:
            md_stack += pred + '\n'
            cur_spaces = len(re.search(r'(\s*).*', pred).group(1))
            if re.match(r'\s*[\*-]\s', pred) is not None:
                if spaces[-1] < cur_spaces:
                    mode.append ('ul>')
                    spaces.append (cur_spaces)
                    stack.append ('')
                while spaces[-1] > cur_spaces or mode[-1] == 'ol>':
                    stack[-2] += '<' + mode[-1] + stack[-1] + '</' + mode[-1]
                    del stack[-1]
                    del mode[-1]
                    sp = spaces[-1]
                    del spaces[-1]  
                    if (sp == cur_spaces):
                        mode.append ('ul>')
                        spaces.append (cur_spaces)
                        stack.append ('')   
                stack[-1] += '<li>' + md2html_line (re.search(r'\s*[\*-]\s(.*)', pred).group(1)) + '</li>'
                pred = i
            elif re.match(r'\s*\d+\.\s', pred) is not None:
                if spaces[-1] < cur_spaces:
                    mode.append ('ol>')
                    spaces.append (cur_spaces)
                    stack.append ('')
                while spaces[-1] > cur_spaces or mode[-1] == 'ul>':
                    stack[-2] += '<' + mode[-1] + stack[-1] + '</' + mode[-1]
                    del stack[-1]
                    del mode[-1]
                    sp = spaces[-1]
                    del spaces[-1]  
                    if (sp == cur_spaces):
                        mode.append ('ol>')
                        spaces.append (cur_spaces)
                        stack.append ('')
                stack[-1] += '<li>' + md2html_line (re.search(r'\s*\d+\.\s(.*)', pred).group(1)) + '</li>'
                pred = i
            else:
                for j in range (len (stack) - 1, 0, -1):
                    if mode[-1] == 'ol>':
                        stack[-2] += '<' + mode[-1] + stack[-1] + '</' + mode[-1]
                        del stack[-1]
                        del mode[-1]
                        del spaces[-1] 
                    elif mode[-1] == 'ul>':
                        stack[-2] += '<' + mode[-1] + stack[-1] + '</' + mode[-1]
                        del stack[-1]
                        del mode[-1]
                        del spaces[-1] 
                stack[-1] += ('<p>' if req_new_str else '') + md2html_line (pred) + ('</p>' if req_new_str else '')
                if not req_new_str:
                    req_new_str = True
                pred = i
    if (stack[-1] != ''):
        sub_res_list[-1][1] = stack[-1]
        sub_res_list[-1][2] = md_stack
    res_list[-1][1] = sub_res_list
    return res_list


if __name__ == '__main__':
    with open('test.md', 'r') as f, open ('test.html', 'w') as f2:
        f2.write (md2html (f.read()))
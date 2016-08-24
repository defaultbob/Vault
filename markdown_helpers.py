import json
import sys

def append_line(str_list, line):
    str_list.append(line)
    str_list.append('\n')

def append_line_html(str_list, line):
    str_list.append(line)
    str_list.append('<br/>')

def add_column(row, value):
    # if first column
    if row == '':
        row = '|'

    row = row + str(value) + '|'
    return row

def header_seperator(columns):
    return ('|:---' * columns) + '|'

def get_common_strings():
    with open('User_Strings/common.json') as data_file:  
        obj = json.load(data_file)

    return obj

def get_comment(comment:str):
    return '[//]: # ({0})'.format(comment)

def block_quote(comment:str):
    return '> ' + comment
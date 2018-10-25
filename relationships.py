import VaultService
import datetime
import subprocess
import os
import mdl
import Helpers
import json
import ast
import component_schema as cs
import sys
import collections
import copy
import markdown_helpers as mdh


def to_string(str_list):
    return ''.join(str_list)

def get_attribute(dictionary, key):
    if dictionary:
        d = dict(dictionary)
    if key in d:
        return d[key]

    return ''

def get_user_string_row(type:str, sub:str,attr_name:str, attr_type:str, attr_component:str):
    
    return '{0},{1},{2},{3},{4}'.format(type,sub,attr_name,attr_type,attr_component)

def append_attribute_user_string_row(user_strings:list, attributes:list, component:str, sub:str):
    for attr in attributes:
        Helpers.append_line(user_strings,get_user_string_row(component,sub, attr.name,attr.type, attr.component or ''))
     

def create_files(components: list):
    path = "output/rel/" 
    print('dumping files to {0}'.format(path))
    if not os.path.exists(path):
        os.makedirs(path)
        
    user_strings = []
    
    Helpers.append_line(user_strings, '{0},{1},{2},{3},{4}'.format('Component Type','Sub Component Type','Attribute','Type','Component'))
    for type,json_definition in components:
        if json_definition:
            response = cs.Response(json_definition)
            if response.component:
                component = response.component
                append_attribute_user_string_row(user_strings, component.attributes, component.name, '')
                
                for sub in component.sub_components:
                    append_attribute_user_string_row(user_strings, sub.attributes, component.name, sub.name)
                
        

    Helpers.save_as_file('relationships', to_string(user_strings), path, 'csv')



def main():
    print("""
 ______    _______  ___      _______  _______  ___   _______  __    _  _______  __   __  ___   _______  _______ 
|    _ |  |       ||   |    |   _   ||       ||   | |       ||  |  | ||       ||  | |  ||   | |       ||       |
|   | ||  |    ___||   |    |  |_|  ||_     _||   | |   _   ||   |_| ||  _____||  |_|  ||   | |    _  ||  _____|
|   |_||_ |   |___ |   |    |       |  |   |  |   | |  | |  ||       || |_____ |       ||   | |   |_| || |_____ 
|    __  ||    ___||   |___ |       |  |   |  |   | |  |_|  ||  _    ||_____  ||       ||   | |    ___||_____  |
|   |  | ||   |___ |       ||   _   |  |   |  |   | |       || | |   | _____| ||   _   ||   | |   |     _____| |
|___|  |_||_______||_______||__| |__|  |___|  |___| |_______||_|  |__||_______||__| |__||___| |___|    |_______|
    """)
    
    client = VaultService.get_client()

    components = mdl.get_component_definitions(client)

    create_files(components)

if __name__ == '__main__':
    main()
    
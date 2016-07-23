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

def append_line(str_list, line):
    str_list.append(line)
    str_list.append('\n')

def append_line_html(str_list, line):
    str_list.append(line)
    str_list.append('<br/>')

def to_string(str_list):
    return ''.join(str_list)

def get_common_strings():
    with open('User_Strings/common.json') as data_file:  
        obj = json.load(data_file)
    
    return obj

def get_attribute(dictionary, key):
    if dictionary:
        d = dict(dictionary)
    if key in d:
        return d[key]

    return ''

def convert_json_to_markdown(json_definition):

    markdown = []
    words = dict(get_common_strings())

    if json_definition:
        response = cs.Response(json_definition)
        if response.component:
            component = response.component
            append_line(markdown, "# " + component.name)
            
            append_line(markdown, get_string_replacement_tag(component.name, 'overview'))
            append_line(markdown, '')
            append_line(markdown, get_string_replacement_tag(component.name, 'overview_description'))

            append_line(markdown, '')
            append_line(markdown, words["abbreviation"] + words["separator"] + component.abbreviation)
            
            append_line(markdown, '## ' + words['component'])

            component_attribute_markdown = build_attribute_markdown(component, words)
            append_line(markdown, component_attribute_markdown)

            for sub in component.sub_components:            
                append_line(markdown, '### ' + words['sub_component'] + words["separator"] + sub.name)
                sub_component_attribute_markdown = build_attribute_markdown(sub, words)
                append_line(markdown, sub_component_attribute_markdown)

            return to_string(markdown)
        else:   
            append_line(markdown, "# " + response.name)

    append_line(markdown, "*" + words["no_docs"] + "*")
    return to_string(markdown)


def link_to_component(component:str):
    return '[`{0}`](../{0}/)'.format(component)

def get_attribute_allows(words, attribute:cs.Component_Attribute):
    cell = []
    # Type
    if attribute.component:
        type = link_to_component(attribute.component)
    else:
        type = attribute.type

    append_line_html(cell, words["type"] + words["separator"] + type)
    
    if attribute.required:
        append_line_html(cell, words["required"])
    
    if attribute.multi_value:
        append_line_html(cell, words["multi_value"])
    
    if attribute.max_length > -1:
        append_line_html(cell, words["max_length"] + words["separator"] + str(attribute.max_length))
    if attribute.max_value > -1:
        append_line_html(cell, words["max_value"] + words["separator"] + str(attribute.max_value))
    if attribute.min_value > -1:
        append_line_html(cell, words["min_value"] + words["separator"] + str(attribute.min_value))
        
    if attribute.ordered:
        append_line_html(cell, words["ordered"] + words["separator"] + str(True))

    if attribute.type == 'Enum' and attribute.enums:
        # no need to append_line_html because of <ul>
        cell.append(words["enums"] + words["separator"])
        enums_str = '<ul>'
        for enum in attribute.enums:
            enums_str += '<li>{0}</li>'.format(str(enum))
        enums_str += '</ul>'
        cell.append(enums_str)

    cell_str = ''.join(cell)    
    if cell_str.endswith('<br/>'):
        cell_str = cell_str[:-5]
    return cell_str

def add_column(row, value):
    # if first column
    if row == '':
        row = '|'

    row = row + str(value) + '|'
    return row

def header_seperator(columns):
    return ('|:---' * columns) + '|'

def build_attribute_markdown(component, common_words):
    md = []
    append_line(md,'')

    # | Attribute | Allows | Description | 
    header_row = '' 
    header_row = add_column(header_row, common_words['attribute_header'])
    header_row = add_column(header_row, common_words['allows_header'])
    header_row = add_column(header_row, common_words['description_header'])
    append_line(md, header_row)
    
    append_line(md, header_seperator(3))
    
    for attr in component.attributes:       
        attribute_row = ''
        attribute_row = add_column(attribute_row, '`' + attr.name +'`')
        attribute_row = add_column(attribute_row, get_attribute_allows(common_words, attr))
        attribute_row = add_column(attribute_row, get_string_replacement_tag(component.name, attr.name))
        append_line(md, attribute_row)

    return ''.join(md)

def dump_files(components):
    
    path = "../output/vault_developer_portal/_posts/mdl/"
    print('dumping post files to {0}'.format(path))

    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        markdown = convert_json_to_markdown(json_definition)
        Helpers.save_as_file('{0}-attributes'.format(type), markdown, path, "markdown")
        

def default_component_user_strings():
    d = collections.OrderedDict()
    d['overview'] = ''
    d['description'] = ''
    return d

def get_string_replacement_key(type:str, attribute:str):
    return '{0}-{1}'.format(type, attribute)

def get_user_string_row(type:str, attribute:str):
    return '{0}: {1} description'.format(get_string_replacement_key(type, attribute), attribute)

def get_string_filename(type:str):  
    return '{0}_attr_description'.format(type)

def get_string_replacement_tag(type:str, attribute:str):
    # {{ site.data.mdl.Docrelationshiptype_attr_description.Docrelationshiptype-label }} {% assign attr = 'Docrelationshiptype-label' %}
    key = get_string_replacement_key(type, attribute)
    filename = get_string_filename(type)
    part1 = "site.data.mdl.{0}.{1}".format(filename, key)
    part2 = "assign attr = '{0}'".format(key)
    return "{{ " + part1 + " }} {% " + part2 + " %}"

def append_attribute_user_string_row(user_strings:list, attributes:list, component:str):
    append_line(user_strings, get_user_string_row(component, "overview")) 
    append_line(user_strings, get_user_string_row(component, "overview_description")) 
    
    for attr in attributes:
	    append_line(user_strings, get_user_string_row(component, attr.name)) 

def create_user_strings(type:str, path:str ,json_definition):
        
    user_strings = []
    
    if json_definition:
        response = cs.Response(json_definition)
        if response.component:
            component = response.component

            append_attribute_user_string_row(user_strings, component.attributes, component.name)
            
            for sub in component.sub_components:
                append_attribute_user_string_row(user_strings, sub.attributes, sub.name)
               
    file_name = get_string_filename(type)           
    Helpers.save_as_file(file_name, to_string(user_strings), path, 'yml')

def create_user_strings_json(type:str, path:str ,json_definition):
        
    user_strings = default_component_user_strings()
    
    if json_definition:
        response = cs.Response(json_definition)
        if response.component:
            component = response.component
            
            for attr in component.attributes:
                user_strings[attr.name] = '' 
            
            for sub in component.sub_components:
                sub_comp_strings = default_component_user_strings()
                for sub_attr in sub.attributes:
                    sub_comp_strings[sub_attr.name] = ''
                user_strings[sub.name] = sub_comp_strings

    Helpers.dump_json_file(type, user_strings, path)

def generate_component_string_files(components: list):
    path = "../output/vault_developer_portal/_data/mdl/" 
    print('dumping string files to {0}'.format(path))
    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        user_strings = create_user_strings(type, path, json_definition)

def main():
    print("""
 _______ _______ _______ _______ _______ _______ _______ _______ 
|\     /|\     /|\     /|\     /|\     /|\     /|\     /|\     /|
| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
| |   | | |   | | |   | | |   | | |   | | |   | | |   | | |   | |
| |M  | | |A  | | |R  | | |K  | | |D  | | |O  | | |W  | | |N  | |
| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
    """)
    
    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    components = mdl.get_component_definitions(client)
    components2 = copy.deepcopy(components)

    dump_files(components)
    generate_component_string_files(components2)
    


if __name__ == '__main__':
    main()
    
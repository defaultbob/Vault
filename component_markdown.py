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

def get_component_strings(type:cs.Component_Schema):
    with open('User_Strings/{0}.json'.format(type.name)) as data_file:  
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

            # get component specific words
            component_words = dict(get_component_strings(component))
            
            append_line(markdown, component_words['overview'])
            append_line(markdown, '')
            append_line(markdown, component_words['description'])

            append_line(markdown, '')
            append_line(markdown, words["abbreviation"] + words["separator"] + component.abbreviation)
            
            append_line(markdown, '## ' + words['component'])

            component_attribute_markdown = build_attribute_markdown(component, words, component_words)
            append_line(markdown, component_attribute_markdown)

            for sub in component.sub_components:
                # get sub component specific words
                sub_component_words = dict(component_words[sub.name])
            
                append_line(markdown, '### ' + words['sub_component'] + words["separator"] + sub.name)
                sub_component_attribute_markdown = build_attribute_markdown(sub, words, sub_component_words)
                append_line(markdown, sub_component_attribute_markdown)

            return to_string(markdown)
        else:   
            append_line(markdown, "# " + response.name)

    append_line(markdown, "*" + words["no_docs"] + "*")
    return to_string(markdown)


def link_to_component(component:str):
    return '[`{0}`](http://developer.veevavault.com/docs/mdl/{0}/)'.format(component)

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
    return ('|-' * columns) + '|'

def build_attribute_markdown(component, common_words, words):
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
        attribute_row = add_column(attribute_row, get_attribute(words, attr.name))
        append_line(md, attribute_row)

    return ''.join(md)

def dump_files(client, instance_name, components):
    
    path = "../output/Markdown/%s/%s/" % (client.domain, instance_name)
    print("dumping files to: " + path)

    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        markdown = convert_json_to_markdown(json_definition)
        Helpers.save_as_file(type, markdown, path, "md")
        
    subprocess.Popen(["open", path])

def default_component_user_strings():
    d = collections.OrderedDict()
    d['overview'] = ''
    d['description'] = ''
    return d

def create_user_strings(type:str, path:str ,json_definition):
        
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
    path = "../output/Markdown/User_Strings/auto/" 
    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        user_strings = create_user_strings(type, path, json_definition)
    
    subprocess.Popen(["open", path])            

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
    
    dump = True
    print_md = False
    regenerate_component_string_files = False

    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    components = mdl.get_component_definitions(client)

    if regenerate_component_string_files:
        generate_component_string_files(components)

    if dump:
        dump_files(client, instance_name, components)
    elif print_md:
        for type,json_definition in components:
            markdown = convert_json_to_markdown(json_definition)
            print(markdown)

if __name__ == '__main__':
    main()
    
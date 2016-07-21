import VaultService
import datetime
import subprocess
import os
import mdl
import Helpers
import json
import ast
import component_schema as cs


def append_line(str_list, line):
    str_list.append(line)
    str_list.append('\n')


def to_string(str_list):
    return ''.join(str_list)

def get_user_strings():
    with open('user_strings.json') as data_file:  
        obj = json.load(data_file)
    
    return obj

def get_attribute(dictionary, key):
    if dictionary:
        d = dict(dictionary)
    if d.has_key(key):
        return d[key]

    return '' 

def convert_json_to_markdown(json_definition):

    markdown = []
    words = dict(get_user_strings())

    if json_definition:
        response = cs.Response(json_definition)
        if response.component:
            component = response.component
            append_line(markdown, "# " + component.name)
            
            if words.has_key(component.name +'_overview'):
                append_line(markdown, words[component.name +'_overview'])
                append_line(markdown, '')
                append_line(markdown, words[component.name +'_description'])

            append_line(markdown, '')
            append_line(markdown, words["abbreviation"] + " " + words["separator"] + " " + component.abbreviation)
            
            append_line(markdown, '## ' + words['component'])

            component_attribute_markdown = build_attribute_markdown(component, words)
            append_line(markdown, component_attribute_markdown)

            for sub in component.sub_components:
                append_line(markdown, '### ' + words['sub_component'] + ' ' + words["separator"] + ' ' + sub.name)
                sub_component_attribute_markdown = build_attribute_markdown(sub, words)
                append_line(markdown, sub_component_attribute_markdown)

            return to_string(markdown)
        else:   
            append_line(markdown, "# " + response.name)

    append_line(markdown, "*" + words["no_docs"] + "*")
    return to_string(markdown)

def build_attribute_markdown(component, words):
    md = []
    append_line(md,'')

    append_line(md, '|' + words['attribute']+ '|' + words['description'] + '|')
    append_line(md, '|-|-|')
    
    for attr in component.attributes:                
        append_line(md, '|`' + attr.name +'`|'+ get_attribute(words, component.name + '.' + attr.name) + '|')

    return ''.join(md)

def dump_files(client, instance_name):
    
    path = "../output/Markdown/%s/%s/" % (client.domain, instance_name)
    print "dumping files to: " + path

    if not os.path.exists(path):
        os.makedirs(path)
        
    components = mdl.get_component_definitions(client)
    for type,json_definition in components:
        markdown = convert_json_to_markdown(json_definition)
        Helpers.save_as_file(type, markdown, path, "md")
        
    subprocess.Popen(["open", path])

def main():
    print """
 _______ _______ _______ _______ _______ _______ _______ _______ 
|\     /|\     /|\     /|\     /|\     /|\     /|\     /|\     /|
| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
| |   | | |   | | |   | | |   | | |   | | |   | | |   | | |   | |
| |M  | | |A  | | |R  | | |K  | | |D  | | |O  | | |W  | | |N  | |
| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
    """

    dump = True
    
    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    if dump:
        dump_files(client, instance_name)
        
    
    components = mdl.get_component_definitions(client)
    for type,json_definition in components:
        markdown = convert_json_to_markdown(json_definition)
        if not dump:
            print markdown

if __name__ == '__main__':
    main()
    
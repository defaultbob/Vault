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

def convert_json_to_markdown(json_definition):

    markdown = []
    words = dict(mdh.get_common_strings())

    if json_definition:
        response = cs.Response(json_definition)
        
        #Helpers.append_line(markdown, '## ' + words['component'])
        if response.component:
            component = response.component

            component_attribute_markdown = build_attribute_markdown(component, words, component.name)
            Helpers.append_line(markdown, component_attribute_markdown)

            for sub in component.sub_components:            
                Helpers.append_line(markdown, '### ' + sub.name)
                sub_component_attribute_markdown = build_attribute_markdown(sub, words, component.name)
                Helpers.append_line(markdown, sub_component_attribute_markdown)

            return to_string(markdown)

    Helpers.append_line(markdown, "*" + words["no_docs"] + "*")
    return to_string(markdown)


def link_to_component(component:str):
    return '`{0}`'.format(component)

def get_attribute_allows(words, attribute:cs.Component_Attribute):
    cell = []
    # Type
    if attribute.component:
        type = link_to_component(attribute.component)
    else:
        type = attribute.type

    Helpers.append_line_html(cell, words["type"] + words["separator"] + type)
    
    if attribute.required:
        Helpers.append_line_html(cell, words["required"])
    
    if attribute.multi_value:
        Helpers.append_line_html(cell, words["multi_value"])
    
    if attribute.max_length > -1 and attribute.max_length < 2147483647:
        Helpers.append_line_html(cell, words["max_length"] + words["separator"] + str(attribute.max_length))
    if attribute.max_value > -1 and attribute.max_value < 2147483647:
        Helpers.append_line_html(cell, words["max_value"] + words["separator"] + str(attribute.max_value))
    if attribute.min_value > -1:
        Helpers.append_line_html(cell, words["min_value"] + words["separator"] + str(attribute.min_value))
        
    if attribute.ordered:
        Helpers.append_line_html(cell, words["ordered"] + words["separator"] + str(True))

    if attribute.type == 'Enum' and attribute.enums:
        # no need to append_line_html because of <ul>
        cell.append(words["enums"] + words["separator"])
        enums_str = '<ul>'
        for enum in attribute.enums:
            enums_str += '<li>{0}</li>'.format(str(enum).replace('_','\_'))
        enums_str += '</ul>'
        cell.append(enums_str)

    cell_str = ''.join(cell)    
    if cell_str.endswith('<br/>'):
        cell_str = cell_str[:-5]
    return cell_str



def build_attribute_markdown(component, common_words, string_file):
    md = []
    Helpers.append_line(md,'')

    # | Attribute | Allows | Description | 
    header_row = '' 
    header_row = mdh.add_column(header_row, common_words['attribute_header'])
    header_row = mdh.add_column(header_row, common_words['allows_header'])
    header_row = mdh.add_column(header_row, common_words['description_header'])
    Helpers.append_line(md, header_row)
    
    Helpers.append_line(md, mdh.header_seperator(3))
    
    for attr in component.attributes:       
        attribute_row = ''
        attribute_row = mdh.add_column(attribute_row, '`' + attr.name +'`')
        attribute_row = mdh.add_column(attribute_row, get_attribute_allows(common_words, attr))
        attribute_row = mdh.add_column(attribute_row, get_string_replacement_tag(component.name, attr.name, string_file))
        Helpers.append_line(md, attribute_row)

    return ''.join(md)

#components (source/mdl/components). These are called as partials
def dump_files(components):
    
    path = "output/components/"
    print('dumping post files to {0}'.format(path))

    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        markdown = convert_json_to_markdown(json_definition)
        Helpers.save_as_file('_{0}-attributes'.format(type), markdown, path, "md.erb")
        

def default_component_user_strings():
    d = collections.OrderedDict()
    d['overview'] = ''
    d['description'] = ''
    return d

def get_string_replacement_key(type:str, attribute:str):
    return '{0}'.format(attribute)

def get_user_string_row(type:str, attribute:str):
    return '- {0}: '.format(get_string_replacement_key(type, attribute))

def get_string_filename(type:str):  
    return '{0}_attr_description'.format(type)

def get_string_replacement_tag(type:str, attribute:str, file:str):
    # {{ site.data.mdl.Docrelationshiptype_attr_description.Docrelationshiptype-label }} {% assign attr = 'Docrelationshiptype-label' %}
    key = get_string_replacement_key(type, attribute)
    filename = get_string_filename(file)
    part1 = "data.{0}.mdl.each do |mdl| ".format(filename)
    part2 = "mdl.{0}".format(key)
    return "<% " + part1 + " %> <%= " + part2 + " %> <% end %>"

def append_attribute_user_string_row(user_strings:list, attributes:list, component:str):
    
    for attr in attributes:
	    Helpers.append_line(user_strings, get_user_string_row(component, attr.name)) 

def create_user_strings(type:str, path:str ,json_definition):
        
    user_strings = []
    Helpers.append_line(user_strings, "mdl:")
    Helpers.append_line(user_strings, get_user_string_row(type, "overview")) 
    Helpers.append_line(user_strings, get_user_string_row(type, "overview_description")) 
    
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

#yaml files
def generate_component_string_files(components: list):
    path = "output/yaml/" 
    print('dumping string files to {0}'.format(path))
    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        user_strings = create_user_strings(type, path, json_definition)

# pages (includes)
def generate_component_pages(components: list):
    path = "output/pages/" 
    print('dumping pages {0}'.format(path))
    if not os.path.exists(path):
        os.makedirs(path)
        
    for type,json_definition in components:
        create_component_page(type, path)

def create_component_page(type:str, path:str):
        
    md = []    
    Helpers.append_line(md,'# {0}'.format(type))
    Helpers.append_line(md,'')
            
    Helpers.append_line(md, get_string_replacement_tag(type, 'overview', type))
    Helpers.append_line(md, '')

    Helpers.append_line(md, get_string_replacement_tag(type, 'overview_description', type))
    Helpers.append_line(md, '')

    # Helpers.append_line(md,'- [Component Attributes](#component)')
    # Helpers.append_line(md,'- [Component Errors](#component-errors)')
    # Helpers.append_line(md,'')

    Helpers.append_line(md,'<%= partial "{0}-attributes" %> '.format(type))
    Helpers.append_line(md,'')

 # We are calling errors on a seperate page, dont need these here   
    # Helpers.append_line(md,'## Component Errors')
    # Helpers.append_line(md,'The MDL can raise errors while executing commands on the components for many reasons. The errors which are common to all component are defined in the [Common Errors]({% post_url 2014-12-23-common %}). The following errors (if any) are specific to this component type.')
    # Helpers.append_line(md,'')
    
    # Helpers.append_line(md,'{{% include_relative {0}-errors.markdown %}}'.format(type))  
    # Helpers.append_line(md,'')     
        
    Helpers.append_line(md, mdh.get_comment('Auto-generated at ' + str(datetime.datetime.now())))
    
    # Name of saved files, we want these pages as includes
    Helpers.save_as_file('_' + type, ''.join(md), path, 'md.erb')

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
    components3 = copy.deepcopy(components)

    dump_files(components)
    generate_component_string_files(components2)
    generate_component_pages(components3)

if __name__ == '__main__':
    main()
    
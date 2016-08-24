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
import markdown_helpers as mdh
import printProgress
import ApiClient

class Error(object):
    def __init__(self, reason, example, message):
        self.reason = reason
        self.examples = [example]    
        self.message = message

    def add_example(self, code:str):
        self.examples.append(code)

def build_markdown(generic_errors: dict):
    lines = []

    # mdh.append_line(lines, '# Generic Errors')
    
    common_strings = dict(mdh.get_common_strings())

    if len(generic_errors.keys()) > 0:
        
        header = mdh.add_column('', common_strings['error_code_header']) 
        header = mdh.add_column(header, common_strings['error_type_header']) 
        header = mdh.add_column(header, common_strings['error_examples_header']) 
        header = mdh.add_column(header, common_strings['error_message_header'])     
        
        mdh.append_line(lines, header)
        mdh.append_line(lines, mdh.header_seperator(4))
        
        for code in generic_errors:
            line = ''
            err = generic_errors[code]
            
            line = mdh.add_column(line, code)
            line = mdh.add_column(line, err.reason)
            line = mdh.add_column(line, '`' + '`<br/>`'.join(err.examples) + '`')
            line = mdh.add_column(line, err.message)
            
            mdh.append_line(lines, line)
    else:
        mdh.append_line(lines, mdh.block_quote(common_strings['error_no_errors']))    
        
    mdh.append_line(lines, mdh.get_comment('Auto-generated at ' + str(datetime.datetime.now())))
    return ''.join(lines)

def create_markdown_file(file_name, client, error_url,  generic_only=False):
    generic_errors = collections.OrderedDict()

    errors_resp = client.get_json(error_url)   
    for error in errors_resp["data"]:
        component = error['component'] 
        
        if (generic_only and component == "GEN") or (not generic_only and component != 'GEN'):
            code = error['code']  
            parts = code.split('-')
            code_num = int(parts.pop())  
            reason = error['reason']  
            message = error['developer_message_template']  

            if code_num not in generic_errors:
                generic_errors[code_num] = Error(reason, code, message)
                # print('Added ' + str(code_num))
            else:
                item = generic_errors[code_num]
                item.add_example(code)
                generic_errors[code_num] = item
    
    Helpers.save_as_file(file_name, build_markdown(generic_errors), '../vault_developer_portal/_posts/mdl/', 'markdown')

def main():
    print("""
▓█████  ██▀███   ██▀███   ▒█████   ██▀███    ██████ 
▓█   ▀ ▓██ ▒ ██▒▓██ ▒ ██▒▒██▒  ██▒▓██ ▒ ██▒▒██    ▒ 
▒███   ▓██ ░▄█ ▒▓██ ░▄█ ▒▒██░  ██▒▓██ ░▄█ ▒░ ▓██▄   
▒▓█  ▄ ▒██▀▀█▄  ▒██▀▀█▄  ▒██   ██░▒██▀▀█▄    ▒   ██▒
░▒████▒░██▓ ▒██▒░██▓ ▒██▒░ ████▓▒░░██▓ ▒██▒▒██████▒▒
░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
 ░ ░  ░  ░▒ ░ ▒░  ░▒ ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒  ░ ░
   ░     ░░   ░   ░░   ░ ░ ░ ░ ▒    ░░   ░ ░  ░  ░  
   ░  ░   ░        ░         ░ ░     ░           ░  
                                                    
    """)
    
    i = 0
    l = 0
    
    use_cache = True
    
    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    components = mdl.get_component_type_names(client, use_cache)
    l = len(components)
    printProgress.printProgress(
        i, l, prefix='Progress:', suffix='Complete', barLength=50)

    first = True
    for component_type in components:
            
        error_url = 'configuration/{0}/errors'.format(component_type)
        try:
            print(0)
            if first:
                create_markdown_file('common-errors', client, error_url, True)
                i+=1
                first = False
                
            create_markdown_file('{0}-errors'.format(component_type), client, error_url)

            printProgress.printProgress(
                i, l, prefix='Progress:', suffix='Complete' + " - " + component_type, barLength=50)
            
        except ApiClient.ApiException:
            print('Failed to get errors for {0} from the API'.format(component_type))

        i+=1
        
    print('Done!')

if __name__ == '__main__':
    main()
    
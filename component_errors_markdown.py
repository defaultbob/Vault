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
import Helpers
import printProgress
import ApiClient

class Error(object):
    def __init__(self, reason, example, message, user_msg = ""):
        self.reason = reason
        self.examples = [example]    
        self.message = message
        self.user_msg = user_msg

    def add_example(self, code:str):
        self.examples.append(code)

def build_markdown(generic_errors: dict):
    lines = []
    
    common_strings = dict(mdh.get_common_strings())

    if len(generic_errors.keys()) > 0:
        
        header = mdh.add_column('', common_strings['error_code_header']) 
        header = mdh.add_column(header, common_strings['error_type_header']) 
        header = mdh.add_column(header, common_strings['error_examples_header']) 
        header = mdh.add_column(header, common_strings['error_message_header'])     
        
        Helpers.append_line(lines, header)
        Helpers.append_line(lines, mdh.header_seperator(4))
        
        for code in generic_errors:
            line = ''
            err = generic_errors[code]
            
            line = mdh.add_column(line, code)
            line = mdh.add_column(line, err.reason)
            line = mdh.add_column(line, '`' + '`<br/>`'.join(err.examples) + '`')
            line = mdh.add_column(line, err.message)
            
            Helpers.append_line(lines, line)
    else:
        Helpers.append_line(lines, mdh.block_quote(common_strings['error_no_errors']))    
        
    Helpers.append_line(lines, mdh.get_comment('Auto-generated at ' + str(datetime.datetime.now())))
    return ''.join(lines)

def create_markdown_file(file_name, errors_resp,  generic_only=False):
    generic_errors = collections.OrderedDict()
   
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
    
    Helpers.save_as_file(file_name, build_markdown(generic_errors), '../output/vault_developer_portal/_posts/mdl/', 'markdown')

def export_csv(file_name, errors_resp,  generic_only=False):
    generic_errors = collections.OrderedDict()
    csv = []

    for error in errors_resp["data"]:
        component = error['component'] 
        
        if (generic_only and component == "GEN") or (not generic_only and component != 'GEN'):
            code_full = error['code']  
            parts = code_full.split('-')
            if(len(parts) == 3):
                type = parts[1]
            else:
                type = parts[2]
                    
            code = parts.pop()
            reason = error['reason']  
            
            key = code + reason + type

            if key not in generic_errors:
                message = '"{0}"'.format(error['developer_message_template'])  
                end_user = '"{0}"'.format(error['end_user_message_template'])  
            
                component_label = component
                if(generic_only):
                    component_label = 'GENERIC'
            
                row = [component_label, code, reason, type, message, end_user]

                Helpers.append_line(csv, ','.join(row))
                generic_errors[key] = 'X'
            
    Helpers.append_to_file(file_name, ''.join(csv), '../output/errors/', 'csv')

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
            errors_resp = client.get_json(error_url)
                
            if first:
                
                create_markdown_file('common-errors', errors_resp, True)
                
                header = ['Type', 'Code', 'Reason','Type', 'Developer message', 'End user message\n']
                Helpers.save_as_file('errors', ','.join(header), '../output/errors/', 'csv')
                
                export_csv('errors', errors_resp, True)
                
                i+=1
                first = False
                
            create_markdown_file('{0}-errors'.format(component_type), errors_resp)
            export_csv('errors', errors_resp)

            printProgress.printProgress(
                i, l, prefix='Progress:', suffix='Complete' + " - " + component_type, barLength=50)
            
        except ApiClient.ApiException:
            print('Failed to get errors for {0} from the API'.format(component_type))

        i+=1
        
    print('Done!')

if __name__ == '__main__':
    main()
    
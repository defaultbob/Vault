#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService
import mdl
import sys
import Helpers
import sys, getopt, os, requests, json, os.path
import Tkinter, tkSimpleDialog

def output_components(path, client, includeWorkflow):

    comps = VaultService.get_component_types(client)
    
    i = 0
    l = 0

    # build list of names first
    for component_json in comps:
        l += len(component_json["names"])

    printProgress.printProgress(
        i, l, prefix='Progress:', suffix='Complete', barLength=50)

    for component_json in comps:
        component_type = component_json["type"]
        type_folder = (path + "/%s") % (component_type) 

        for component_name in component_json["names"]:
            
            if not os.path.exists(type_folder):
                os.makedirs(type_folder)

            name = component_type + "." + component_name
            if includeWorkflow and component_type == "Workflow":
                wf = VaultService.get_workflow(client, component_name)
                Helpers.dump_json_file(component_name, wf, type_folder + "/")
            else:
                with open(type_folder + "/" + component_name + ".mdl", "w") as f:
                    mdl = VaultService.get_component(
                        client, name)
                    f.write(mdl.encode('utf-8'))
            
            i += 1
            printProgress.printProgress(
                i, l, prefix='Progress:', suffix='Complete' + " - " + name, barLength=50)
        
def main(argv):
              
    password = None
    username = None
    server = None
    filepath = "/"

    try:
        opts, args = getopt.getopt(argv,"hs:u:p:f:",["server=","username=", "password="])
    except getopt.GetoptError:
        print '\nERROR: Missing required option or argument.'
        print 'USAGE: upload.py -s <server> -u <username> [-p <password>]'
        sys.exit(2)

    if not opts:
        print '\nERROR: Missing required option or argument.'
        print 'USAGE: upload.py -s <server> -u <username> [-p <password>]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print '\nUSAGE: upload.py -s <server> -u <username> -p <password>'
            sys.exit()
        elif opt == '-p':
            password = arg
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            abc = arg
        #elif opt in ("-f", "--filepath"):
            #filepath = arg

    if None in (username, server, filepath):
        print '\nERROR: Missing required option or argument.'
        print 'USAGE: upload.py -s <server> -u <username> [-p <password>]'
        sys.exit(2)

    if not password:
        root = Tkinter.Tk()
        root.overrideredirect(True)
        root.geometry('0x0+200+200')
        root.lift()
        root.attributes('-topmost', True)
        password = tkSimpleDialog.askstring(title="Password", prompt="Enter Password", show="*" )
        if not password:
            print "\nERROR: Password is required."
            sys.exit()

    client = ApiClient.ApiClient(server, username, password, "18.2")
    
    
    path = "components"

    includeWorkflow = True 
    output_components(path, client, includeWorkflow)
    print "Done"

if __name__ == "__main__":
    main(sys.argv[1:])



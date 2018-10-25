import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService
import mdl
import sys
import Helpers

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
        
def main():
              
    print """
     ______                                             __      
    / ____/___  ____ ___  ____  ____  ____  ___  ____  / /______
    / /   / __ \/ __ `__ \/ __ \/ __ \/ __ \/ _ \/ __ \/ __/ ___/
    / /___/ /_/ / / / / / / /_/ / /_/ / / / /  __/ / / / /_(__  ) 
    \____/\____/_/ /_/ /_/ .___/\____/_/ /_/\___/_/ /_/\__/____/  
                                                                                    
    """
    
    client = VaultService.get_client()
    instance_name = datetime.datetime.now()
    path = "../output/MDL API/%s/%s" % (client.domain, instance_name)

    includeWorkflow = True 
    output_components(path, client, includeWorkflow)
    print "Done"

if __name__ == '__main__':
    sys.exit(int(main() or 0))



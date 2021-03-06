#import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService
import Helpers

def output_components(path, client):
    i = 0
    l = 0

    offset = 3000

    directory = client.get_json("query/components?q=SELECT component_name__v, checksum__v, component_type__v, LONGTEXT(mdl_definition__v), LONGTEXT(json_definition__v) FROM vault_component__v WHERE status__v='active__v' ORDER BY component_type__v LIMIT {0}".format(offset));

    l = directory["responseDetails"]["size"]
    printProgress.printProgress(
        i, l, prefix='Progress:', suffix='Complete', barLength=50)

    csv = []
    Helpers.append_line(csv, 'Component Type,Name,Checksum')

    for component in directory["data"]:
        name = component["component_name__v"]
        type = component["component_type__v"]
        checksum = component["checksum__v"]
        mdl = component["mdl_definition__v"]
        json_def = component["json_definition__v"]

        

        Helpers.append_line(csv, '{0},{1},{2}'.format(type, type+"."+name, checksum))

        type_folder = (path + "/%s") % (type)
        if not os.path.exists(type_folder):
            os.makedirs(type_folder)
        
        #json_folder = (type_folder + "/json/")
        #if not os.path.exists(json_folder):
        #    os.makedirs(json_folder)

        mdl_folder = (type_folder) # + "/mdl")
        if not os.path.exists(mdl_folder):
            os.makedirs(mdl_folder)

        #Helpers.dump_json_file(name, json_def, json_folder)
        
        with open(mdl_folder + "/" + name + ".txt", "w") as f:
            if (type == "Workflow"):
                Helpers.dump_json_file(name + ".json", json_def, mdl_folder + "/")
            else:
                f.write(mdl.encode('utf-8'))
            i += 1
            printProgress.printProgress(
                i, l, prefix='Progress:', suffix='Complete' + " - " + name, barLength=50)
            
    return csv

def main():
    print """
     _    ______    __       ______                                             __      
    | |  / / __ \  / /      / ____/___  ____ ___  ____  ____  ____  ___  ____  / /______
    | | / / / / / / /      / /   / __ \/ __ `__ \/ __ \/ __ \/ __ \/ _ \/ __ \/ __/ ___/
    | |/ / /_/ / / /___   / /___/ /_/ / / / / / / /_/ / /_/ / / / /  __/ / / / /_(__  ) 
    |___/\___\_\/_____/   \____/\____/_/ /_/ /_/ .___/\____/_/ /_/\___/_/ /_/\__/____/  
                                            /_/                                        
    """

    client = VaultService.get_client()
    instance_name = datetime.datetime.now()
    path = "../output/VQL/%s/%s" % (client.domain, instance_name)

    csv = output_components(path, client)
    Helpers.save_as_file('{0}_{1}'.format(client.domain, instance_name),''.join(csv), path,'csv')

    print "Done"

if __name__ == "__main__":
    main()
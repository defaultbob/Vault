#import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService

def output_components(path, client):
    i = 0
    l = 0

    directory = client.get_json("query/components?q=SELECT component_name__v, checksum__v, component_type__v, mdl_definition__v FROM vault_component__v ORDER BY component_type__v");

    l = directory["responseDetails"]["size"]
    printProgress.printProgress(
        i, l, prefix='Progress:', suffix='Complete', barLength=50)

    for component in directory["data"]:
        name = component["component_name__v"]
        type = component["component_type__v"]
        checksum = component["checksum__v"]
        mdl = component["mdl_definition__v"]

        type_folder = (path + "/%s") % (type)
        if not os.path.exists(type_folder):
            os.makedirs(type_folder)
        
        with open(type_folder + "/" + name + ".mdl", "w") as f:
            f.write(mdl.encode('utf-8'))
            i += 1
            printProgress.printProgress(
                i, l, prefix='Progress:', suffix='Complete' + " - " + name, barLength=50)
            


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

    output_components(path, client)

    print "Done"

if __name__ == "__main__":
    main()
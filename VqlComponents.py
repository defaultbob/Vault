import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService

print """
 _    ______    __       ______                                             __      
| |  / / __ \  / /      / ____/___  ____ ___  ____  ____  ____  ___  ____  / /______
| | / / / / / / /      / /   / __ \/ __ `__ \/ __ \/ __ \/ __ \/ _ \/ __ \/ __/ ___/
| |/ / /_/ / / /___   / /___/ /_/ / / / / / / /_/ / /_/ / / / /  __/ / / / /_(__  ) 
|___/\___\_\/_____/   \____/\____/_/ /_/ /_/ .___/\____/_/ /_/\___/_/ /_/\__/____/  
                                          /_/                                        
"""
i = 0
l = 0

client = VaultService.get_client()

instance_name = datetime.datetime.now()

# Read config
configParser = ConfigParser.RawConfigParser()
configParser.readfp(open(r'config.txt'))
test_mode = configParser.getboolean('credentials', 'test_mode')

if test_mode:
    instance_name = "TEST %s" % instance_name

directory = client.get_json("query/components?q=SELECT component_name__v, checksum__v, component_type__v, mdl_definition__v FROM vault_component__v ORDER BY component_type__v");

l = directory["responseDetails"]["size"]
printProgress.printProgress(
    i, l, prefix='Progress:', suffix='Complete', barLength=50)

for component in directory["data"]:
    name = component["component_name__v"]
    type = component["component_type__v"]
    checksum = component["checksum__v"]
    mdl = component["mdl_definition__v"]

    type_folder = "../output/VQL/%s/%s/%s" % (client.domain,instance_name, type)
    if not os.path.exists(type_folder):
        os.makedirs(type_folder)
    
    with open(type_folder + "/" + name + ".mdl", "w") as f:
        f.write(mdl.encode('utf-8'))
        i += 1
        printProgress.printProgress(
            i, l, prefix='Progress:', suffix='Complete' + " - " + name, barLength=50)
        if test_mode:
            print "Only output 1 mdl in test mode - done"
            quit()

print "Done"
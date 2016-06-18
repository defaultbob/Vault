"""VAULT API TESTING 01"""

import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService

# Read config
configParser = ConfigParser.RawConfigParser()
configParser.readfp(open(r'config.txt'))

domain = configParser.get('credentials', 'domain')
username = configParser.get('credentials', 'username')
password = configParser.get('credentials', 'password')
version = configParser.getint('credentials', 'version')
test_mode = configParser.getboolean('credentials', 'test_mode')

client = ApiClient.ApiClient(domain, username, password, version)

comps = VaultService.get_component_types(client)
instance_name = datetime.datetime.now()

if test_mode:
    instance_name = "TEST %s" % instance_name

i = 0
l = 0

# build list of names first
for component_json in comps:
    l += len(component_json["names"])

printProgress.printProgress(
    i, l, prefix='Progress:', suffix='Complete', barLength=50)

for component_json in comps:
    component_type = component_json["type"]
    type_folder = "../output/%s/%s/%s" % (domain,
                                       instance_name, component_type)

    os.makedirs(type_folder)
    for component_name in component_json["names"]:
        name = component_type + "." + component_name
        with open(type_folder + "/" + component_name + ".mdl", "w") as f:
            mdl = VaultService.get_component(
                client, name)
            f.write(mdl)
        i += 1
        printProgress.printProgress(
            i, l, prefix='Progress:', suffix='Complete' + " - " + name, barLength=50)
        if test_mode:
            print "Only output 1 mdl in test mode - done"
            quit()


print "Done"

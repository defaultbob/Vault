"""VAULT API TESTING 01"""

import datetime
import os
import VaultAPI

#domain = "pm8.vaultdev.com"
domain = "z-team-promomats.veevavault.com"
#username = "david.mills@mdltest.com"
username = "david.mills@z-team.com"
#password = "2:<A!zyRuyQr"
password = "ZZkWCp0YZA"
#version = 15
version = 14

test_mode = True

session = VaultAPI.get_session(domain, username, password, version)

comps = VaultAPI.get_component_types(domain, session)

instance_name = datetime.datetime.now()
if test_mode:
    instance_name = "TEST %s" % instance_name

for component_json in comps:
    component_type = component_json["type"]
    type_folder = "output/%s/%s/%s" % (domain, instance_name, component_type)

    os.makedirs(type_folder)
    for component_name in component_json["names"]:
        with open(type_folder + "/" + component_name + ".mdl", "w") as f:
            f.write(VaultAPI.get_component(domain, session,
                                           component_type + "." + component_name))
        if test_mode:
            quit()

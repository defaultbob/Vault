"""VAULT API TESTING 01"""

import config
import datetime
import os
import VaultAPI

session = VaultAPI.get_session(config.domain, config.username, config.password, config.version)

comps = VaultAPI.get_component_types(config.domain, session)

instance_name = datetime.datetime.now()
if config.test_mode:
    instance_name = "TEST %s" % instance_name

for component_json in comps:
    component_type = component_json["type"]
    type_folder = "output/%s/%s/%s" % (config.domain, instance_name, component_type)

    os.makedirs(type_folder)
    for component_name in component_json["names"]:
        with open(type_folder + "/" + component_name + ".mdl", "w") as f:
            f.write(VaultAPI.get_component(config.domain, session,
                                           component_type + "." + component_name))
        if config.test_mode:
            quit()

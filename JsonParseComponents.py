import ConfigParser
import datetime
import os
import ApiClient
import printProgress
import VaultService
import json
from xml.etree import ElementTree as ET
import logging

def process_components(data):
    for component in data:
        name = component["component_name__v"]
        type = component["component_type__v"]
        checksum = component["checksum__v"]
        mdl = component["mdl_definition__v"]
        json_str = component["json_definition__v"]

        valid = True
        
        # parse string to object
        try:
            json_object = json.loads(json_str)
        except (ValueError,TypeError):
            json_object = None
            valid = False
            
        folder_name = 'valid'
        if valid is False:
            folder_name = 'invalid'
        
        type_folder = "../output/JSON/%s/%s/%s/%s" % (client.domain, instance_name, folder_name, type)
        
        if not os.path.exists(type_folder):
            os.makedirs(type_folder)
        
        with open(type_folder + "/" + name + ".json", "w") as f:
            if valid is False:
                if json_str:
                    f.write(json_str.encode('utf-8'))
            else:
                json.dump(json_object, f, indent=4)            


def parse_xml(json_object):
    return False
    #  try:
    #      page_markup = json_object["page_markup"]
    #  except KeyError:
    #      return json_object
    #  except TypeError:
    #      if json_object[0] is None:
    #          return json_object
    #     page_markup = json_object[0]["page_markup"]
    
    # # # try:
    # #     x = ET.fromstring(page_markup)
    # # except ET.ParseError:
    # #     return False


print """
     _ ___  ___  _  _  __   ___   _    ___ ___   _ _____ ___ 
  _ | / __|/ _ \| \| | \ \ / /_\ | |  |_ _|   \ /_\_   _| __|
 | || \__ \ (_) | .` |  \ V / _ \| |__ | || |) / _ \| | | _| 
  \__/|___/\___/|_|\_|   \_/_/ \_\____|___|___/_/ \_\_| |___|
                                                              
"""

client = VaultService.get_client()

instance_name = datetime.datetime.now()
print "Components will be in folder: %s" % instance_name 

limit = 1000
size = 1000
offset = 0
i = 1

while size == limit:
    directory = client.get_json("query/components?q=SELECT component_name__v, checksum__v, component_type__v, LONGTEXT(json_definition__v), mdl_definition__v FROM vault_component__v LIMIT %s OFFSET %s" % (limit, offset));
    limit = directory["responseDetails"]["limit"]
    size = directory["responseDetails"]["size"]
    offset += limit
    process_components(directory["data"])
    print "Batch %s of %s" %(i, size)
    i+=1

client = None
print "Done"
logging.info("-------------------DONE------------------")






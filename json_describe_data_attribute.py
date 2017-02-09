import VaultService
import datetime
import subprocess
import os
import mdl
import Helpers
import ApiClient
        
def get_attributes(client, resource:str):
    try:
        json = client.get_json(resource)
        attributes = ''
        for attribute,value in json.items():
            if not attribute == "responseStatus":
                attributes = attributes + attribute + ','
    
    except ApiClient.ApiException:
        attributes = "ERROR"

    return attributes

def component_types_csv(client):
    csv = []
    Helpers.append_line(csv, 'Component Type, attributes')
    
    all_components = VaultService.get_component_types(client)
    for defn in all_components:
        type = defn["type"]
        if len(defn["names"]) > 0:
            instance = defn["names"][0]
        else:
            instance = None
        
        attributes = get_attributes(client, 'configuration/{0}'.format(type))
               
        Helpers.append_line(csv, '{0},{1}'.format(type, attributes))
        
        if not instance:
            instance = "NONE"
            instance_attributes = ""
        else:
            instance_attributes = get_attributes(client, 'configuration/{0}.{1}'.format(type, instance))

        Helpers.append_line(csv, '{0}.{1},{2}'.format(type, instance, instance_attributes))            
    
    return csv

def main():
    print ("------- data or collection? -------------")

    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    path = "../output/json_describe/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    csv = component_types_csv(client)
    Helpers.save_as_file('{0}_{1}'.format(client.domain, instance_name),''.join(csv), path,'csv')

    print("-----------DONE----------------------------")


if __name__ == '__main__':
    main()
    
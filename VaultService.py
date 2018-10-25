import json
try:
    import configparser as cp
except ImportError:
    import ConfigParser as cp
import ApiClient
import Helpers
import os

def get_client():
    # Read config
    configParser = cp.RawConfigParser()
    configParser.readfp(open(r'config.txt'))

    domain = configParser.get('credentials', 'domain')
    username = configParser.get('credentials', 'username')
    password = configParser.get('credentials', 'password')
    version = configParser.get('credentials', 'version')

    client = ApiClient.ApiClient(domain, username, password, version)
    return client

def get_component_types(client):
    
    data = client.get_mdl_json("components")
    return data["components"]

def get_component(client, component):
    """Get Components"""
    data = client.get_mdl("components/%s" % (component))
    return data.text

def get_workflow(client, component):
    
    data = client.get_json("/objects/workflows/configuration/%s" % (component))
    return data

def get_vcf_types(client):
    
    data = client.get_json("configuration/Componenttype")
    return data["data"]

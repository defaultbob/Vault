
import ConfigParser
import ApiClient

def get_client():
    # Read config
    configParser = ConfigParser.RawConfigParser()
    configParser.readfp(open(r'config.txt'))

    domain = configParser.get('credentials', 'domain')
    username = configParser.get('credentials', 'username')
    password = configParser.get('credentials', 'password')
    version = configParser.getint('credentials', 'version')

    client = ApiClient.ApiClient(domain, username, password, version)
    return client

def get_component_types(client):
    """Get Component Types"""
    data = client.get_mdl_json("components")

    return data["components"]

def get_component(client, component):
    """Get Components"""
    data = client.get_mdl("components/%s" % (component))
    return data.text

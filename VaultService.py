
import requests

def get_component_types(client):
    """Get Component Types"""
    data = client.get_mdl_json("components")

    return data["components"]

def get_component(client, component):
    """Get Components"""
    data = client.get_mdl("components/%s" % (component))
    return data.text
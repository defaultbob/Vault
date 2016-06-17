
import requests
import ApiClient

def get_component_types(client):
    """Get Component Types"""
    data = client.get_mdl_json("components")

    return data["components"]

def get_component(client, component):
    """Get Components"""
    data = client.get_mdl("components/%s" % (component))
    return data.text

def auth(domain, user, password, version):
    """Authenticate to Vault API"""
    url = "https://%s/api/v%s.0/auth" % (domain, version)

    querystring = {"username": user, "password": password}

    response = requests.request(
        "POST", url, params=querystring)
    response.raise_for_status()

    return response.json()

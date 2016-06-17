"""Vault API helpers"""

import requests


def get_session(domain, user, password, version):
    """Get the vault session"""
    data = auth(domain, user, password, version)
    return data["sessionId"]


def get_component_types(domain, session):
    """Get Component Types"""
    url = "https://%s/api/mdl/components" % (domain)
    headers = {
        'Authorization': session,
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return data["components"]


def get_component(domain, session, component):
    """Get Components"""
    url = "https://%s/api/mdl/components/%s" % (domain, component)
    headers = {
        'Authorization': session,
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.text


def auth(domain, user, password, version):
    """Authenticate to Valut API"""
    url = "https://%s/api/v%s.0/auth" % (domain, version)

    querystring = {"username": user, "password": password}

    response = requests.request(
        "POST", url, params=querystring)
    response.raise_for_status()

    return response.json()

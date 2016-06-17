"""Vault API client"""
import requests

class ApiClient:

    def __init__(self, domain, user, password, version):
        # initialize the session
        self.s = requests.Session()
        
        # Get the vault session
        data = ApiClient.auth(domain, user, password, version)

        self.domain = domain
        self.version = version

        self.s.headers.update({"Authorization": data["sessionId"]})

    def get_json(self, resource):
        response = self.get(resource)
        return self.parse_response(response)

    def get(self, resource):
        url = "https://%s/api/v%s.0/%s" % (self.domain,
                                           self.version, resource)
        response = self.s.get(url)
        response.raise_for_status()
        return response    

    def get_mdl_json(self, resource):
        response = self.get_mdl(resource)
        return self.parse_response(response)

    def get_mdl(self, resource):
        url = "https://%s/api/mdl/%s" % (self.domain, resource)
        response = self.s.get(url)
        response.raise_for_status()
        return response

    def parse_response(self, response):
        json = response.json()

        respStat = json["responseStatus"]
        if(respStat != "SUCCESS"):
            raise RuntimeError('request got responseStatus %s' % respStat)

        return response.json()

    @staticmethod
    def auth(domain, user, password, version):
        """Authenticate to Vault API"""
        url = "https://%s/api/v%s.0/auth" % (domain, version)

        querystring = {"username": user, "password": password}

        response = requests.request(
            "POST", url, params=querystring)
        response.raise_for_status()

        return response.json()



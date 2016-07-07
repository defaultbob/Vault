import ApiClient
import VaultService
import time

print """
 _____                 _ _               
/  ___|               | | |              
\ `--.  __ _ _ __   __| | |__   _____  __
 `--. \/ _` | '_ \ / _` | '_ \ / _ \ \/ /
/\__/ / (_| | | | | (_| | |_) | (_) >  < 
\____/ \__,_|_| |_|\__,_|_.__/ \___/_/\_\
"""

read_from_config = raw_input('Read credentials from config.txt? (y/n)')
client = None

if read_from_config == "y":
    client = VaultService.get_client()
else:
    domain = raw_input('Domain (e.g. usc8-promomats.veevavault.com): ')
    username = raw_input('What is your username? (e.g. david.mills@usc8.com): ')
    password = raw_input('What is your password?: ')
    version = 15
    client = ApiClient.ApiClient(domain, username, password, version)

print "... Authenticated Successfully "

name = raw_input('Sandbox name: ')
domain_name = raw_input('Domain name (e.g. usc8): ')

payload = "name=%s&type=demo&domain=%s" % (name, domain_name)
response = client.post_form("objects/sandbox", payload)
job_id = response["job_id"]

print "Job id: %s" % job_id
running = True
print "... Checking job status ..."

while running:
    
    status_resp = client.get_json("services/jobs/%s" % job_id)
    data = status_resp["data"]
    status = data["status"]
    
    if(status == u"SUCCESS" or status == u"FAILURE"):
        running = False
        print "Sandbox build complete with status = %s" % status
    else:
        print "... status = %s, waiting to check again ..." % status 
    time.sleep(15)



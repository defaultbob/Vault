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

how_many = raw_input('How many times?')
client = None


domain = 'align-master.vaultdev.com'
username = 'admin@dmills-prod.com'
password = '9exieF7f7MRP'
version = '18.2'
client = ApiClient.ApiClient(domain, username, password, version)

print "... Authenticated Successfully "

name = 'repeater'
domain_name = 'dmills-sbx.com'

payload = "name=%s&type=config&domain=%s" % (name, domain_name)
response = client.post_form("objects/sandbox", payload)
job_id = response["job_id"]
print "Job ID: %s" % job_id

running = True
print "... Checking job status ..."
count=1
while running:
    status_resp = client.get_json("services/jobs/%s" % job_id)
    data = status_resp["data"]
    status = data["status"]
    
    if(status == u"SUCCESS" or status == u"FAILURE"):
        
        print "Sandbox build complete with status = %s" % status
        if(status == u"FAILURE"):
            running = False
        else:
            count+=1
            print "sandbox created moving to next step %s" % count
    else:
        print "... status = %s, waiting to check again ..." % status 
        time.sleep(15)
    
    
    if(count == how_many):
        running = False
        print "got to count %s" % how_many
    



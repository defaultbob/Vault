import VqlComponents
import VaultService
import datetime
import Components
#import subprocess
import os

print """
       __           __   __         __        __   ___ 
 |\/| |  \ |       /  ` /  \  |\/| |__)  /\  |__) |__  
 |  | |__/ |___    \__, \__/  |  | |    /~~\ |  \ |___ 
                                                       
"""

client = VaultService.get_client()
instance_name = datetime.datetime.now()

path = "../output/MDL Compare/%s/%s/" % (client.domain, instance_name)

path_mdl = path + "MDL"
Components.output_components(path_mdl, client)

path_vql = path + "VQL"
VqlComponents.output_components(path_vql, client)

# subprocess.Popen(["open", path])
os.system('bcomp "%s" "%s"' %(path_mdl, path_vql))
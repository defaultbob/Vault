import VaultService
import datetime
import subprocess
import os
import mdl
import Helpers
        
def main():
    print """
     ___ ___    ___ ______   ____  ___     ____  ______   ____ 
    |   |   |  /  _]      | /    ||   \   /    ||      | /    |
    | _   _ | /  [_|      ||  o  ||    \ |  o  ||      ||  o  |
    |  \_/  ||    _]_|  |_||     ||  D  ||     ||_|  |_||     |
    |   |   ||   [_  |  |  |  _  ||     ||  _  |  |  |  |  _  |
    |   |   ||     | |  |  |  |  ||     ||  |  |  |  |  |  |  |
    |___|___||_____| |__|  |__|__||_____||__|__|  |__|  |__|__|                                                       
    """

    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    path = "../output/Metadata/%s/%s/" % (client.domain, instance_name)
    if not os.path.exists(path):
        os.makedirs(path)
        
    components = mdl.get_component_definitions(client)
    Helpers.dump_json_files(components, path)
    
    subprocess.Popen(["open", path])

if __name__ == '__main__':
    main()
    
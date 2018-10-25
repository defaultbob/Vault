import VaultService
import datetime
import subprocess
import os
import mdl
import Helpers
        
def main():
    print """
    VCFVCFVCFVCFVCFVCFVCFVCFVCFVCFVCFVCF                                                     
    """

    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    path = "../output/VCF/%s/%s/" % (client.domain, instance_name)
    if not os.path.exists(path):
        os.makedirs(path)
        
    components = mdl.get_vcf_definitions(client)
    Helpers.dump_json_files(components, path)
    
    subprocess.Popen(["open", path])

if __name__ == '__main__':
    main()
    
import VaultService
import datetime
import mdl
import Helpers
import component_schema as cs

def main():
    print("""
Subcomponent names
    """)
    
    csv = []
    Helpers.append_line(csv, 'Component,Sub component, json name')

    client = VaultService.get_client()
    instance_name = datetime.datetime.now()

    components = mdl.get_component_definitions(client)
    for type,json_definition in components:
        response = cs.Response(json_definition)
        if(response.component):        
            for sub in response.component.sub_components:
                Helpers.append_line(csv, '{0},{1},{2}'.format(type, sub.name, sub.json_name))

        # client.get_json('/api/{{version}}/configuration/Doclifecycle.claim__c')
    
    Helpers.save_as_file('subcomponents',''.join(csv), '../output/','csv')

if __name__ == '__main__':
    main()
    
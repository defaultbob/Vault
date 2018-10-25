import re
import VaultService
import ApiClient

def parse_mdl(mdl_str):
    mdl = str(mdl_str)
    statements = mdl.split(";")

    stmts = []
    for stmt in statements:
        if len(stmt.strip()) > 1:
            stmts.append(parse_statement(stmt.strip()))

    return stmts

def parse_statement(mdl_str):
    mdl = str(mdl_str)
    try:
        first_brace = mdl.index('(')
        last_brace = mdl.rindex(')')        
    except ValueError:
        return []
        pass

    component_inner_str = mdl[first_brace+1:last_brace+1]
    return parse_component(component_inner_str)

def parse_component(mdl_str):
    mdl = re.sub('\s+',' ', str(mdl_str))
    #print "STRIPPED MDL = " + mdl
    
    name=''
    values =[]
    name_start_index = 0
    name_end_index = mdl.find("(")
    at_end = False
    while name_end_index > -1 : # keep taking names until no more opening ( 
    
        name =  mdl[name_start_index:name_end_index].strip()
        if not name:
            break
        
        # find closing ) for a Value
        count = 0
        value_closing_shift = 1
        for i, c in enumerate(mdl[name_end_index:]):
            printed = c
            if c != ' ':
                if c == '(':
                    count+=1
                    printed += " + 1 = " + str(count)
                elif c == ')':
                    count-=1
                    printed += " - 1 = " + str(count)

                #print printed                
                if count == 0:
                    value_closing_shift = i+1
                    break
        
        value = mdl[name_end_index + 1:name_end_index + value_closing_shift -1]

        name_words = name.split()

        if len(name_words) > 1:
            value = parse_component(value)
        values.append((name, value))
        name_start_index = name_end_index + value_closing_shift + 1
        #print mdl[name_start_index:]
        name_end_index = name_start_index + mdl[name_start_index:].find("(")
        #print "next name starts at {0}, ends at {1}".format(name_start_index,name_end_index)

    return values
    
def print_component(lst, depth):
    
    for a,v in lst:
        if isinstance(v, list):
            print("\t"*depth + a)
            print_component(v, depth+1)
        else:
            print("\t"*(depth) + a + "."+ v)

def get_component_type_names(client):
    component_types_json = VaultService.get_component_types(client)

    component_type_names = []
    for item in component_types_json:
        component_type_names.append(item["type"])

    return component_type_names

def get_component_definition(name, client):
    resource = "metadata/components/{0}"
    try:
        definition = client.get_json(resource.format(name))
    except ApiClient.ApiException as e:
        definition = {
            "responseStatus":"FAILURE",
            "data": {
                "name": name
            },
            "error": str(e)
        }

    return definition     

def get_component_definitions(client):
    names = get_component_type_names(client)
    definitions = []
    for name in names:
        definitions.append(get_component_definition(name, client))
        
    return zip(names, definitions)

def get_vcf_type_names(client):
    component_types_json = VaultService.get_vcf_types(client)

    component_type_names = []
    for item in component_types_json:
        component_type_names.append(item["name"])

    return component_type_names

def get_vcf_definitions(client):
    names = get_vcf_type_names(client)
    definitions = []
    for name in names:
        definitions.append(get_component_definition(name, client))
        
    return zip(names, definitions)

def main():
    statements = parse_mdl("""
    RECREATE Docfield annotations_all__v (
        label('Annotations (All)'),
        active(true),
        type('Formula'),
        object(),
        display_section('Docfieldlayout.general__c'),
        default_value(),
        formula([passThrough(Document.annotationsAll_b)]),
        blank_fields('zeros'),   
        Doclifecyclestate dm_state__c (
            label('DM State'),
            active(false),
            Doclifecyclestate dm_state__c (
            label('DM State'),
                active(false)
            )
        )
    );
    """)

    for statement in statements:
        print_component(statement, 0)

if __name__ == '__main__':
    main()

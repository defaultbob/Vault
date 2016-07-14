import re

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
    
    first_brace = mdl.index('(')
    last_brace = mdl.rindex(')')

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
    
    # TESTING
    # name_end_index = -1
    # while name_end_index > -1 : # keep taking names until no more opening ( 
    #     name =  mdl[:name_end_index].strip()
    #     print "NAME: " + name
        
    #     partition_name = name.strip().partition(" ")
    #     if partition_name[1]: # a space => "SubcomponentType  name"
    #         print "Found a subcomponent: %s" % name

    #         # find end of subcomponents
    #         start_brace_index = name_end_index + 2
    #         end_brace_index = mdl[start_brace_index:].find(")")
            
    #         # while mdl[start_brace_index:end_brace_index].find("("):
    #         #     start_brace_index = end_brace_index +1
    #         #     end_brace_index = mdl[start_brace_index:].find(")")
    #         #     print "START %s END %s" % (start_brace_index,end_brace_index)

    #         print "found end at %s" % end_brace_index
    #         subcomponent_types.append(partition_name[0])
    #         subcomponent_names.append(partition_name[2])
    #         subcomponent_values.append(mdl[name_end_index +2:end_brace_index])
    #         mdl = mdl[end_brace_index +1:].lstrip(",")

    #     else:
    #         # find closing ) for a Value
    #         value_end_index = mdl.find(")")
    #         attribute_names.append(mdl[:name_end_index])
    #         attribute_values.append(mdl[name_end_index+1:value_end_index])
    
    #         mdl = mdl[value_end_index+1:].lstrip(",")
    
    #     name_end_index = mdl.find("(")
    
    
    

# TESTING

def print_component(lst, depth):
    
    for a,v in lst:
        if isinstance(v, list):
            print("\t"*depth + a)
            print_component(v, depth+1)
        else:
            print("\t"*(depth) + a + "."+ v)

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
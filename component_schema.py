
class Component_Schema(object):

    def __init__(self, json_definition):
        
        self.name = json_definition["data"]["name"]
        if json_definition["responseStatus"] == 'SUCCESS':
            self.abbreviation = json_definition["data"]["abbreviation"]
            self.attributes = self.build_attributes(json_definition)
            self.sub_components = self.build_sub_components(json_definition)
            self.populated = True
        else:
            self.populated = False

    def build_attributes(self, json_definition):
        json_attributes = json_definition["data"]["attributes"]
        attributes = []
        for attribute in json_attributes:
            attributes.append(Component_Attribute(attribute))

        return attributes 
    
    def build_sub_components(self, json_definition):
        subs = []
        data = dict(json_definition["data"])

        if data.has_key("sub_components"):
            json_subs = data["sub_components"]
            for sub in json_subs:
                subs.append(sub["name"])

        return subs 
    
class Component_Attribute(object):
    def __init__(self, attribute_definition):
        self.name = str(get_attribute(attribute_definition, "name"))
        self.type = str(get_attribute(attribute_definition, "type"))
        self.required = is_required(get_attribute(attribute_definition, "requiredness"))
        self.max_length = int(get_attribute(attribute_definition, "max_length") or -1)
        self.editable = bool(get_attribute(attribute_definition, "editable"))
        self.multi_value = bool(get_attribute( attribute_definition, "multi_value") or False)
        self.ordered = bool(get_attribute(attribute_definition, "ordered") or False)

        if self.type.upper() == 'COMPONENT':
            self.component = str(get_attribute(attribute_definition, "component"))
    



# Common Helpers

def is_required(str_requiredness):
    return str_requiredness == 'required'

def get_attribute(dictionary, key):
    if dictionary:
        d = dict(dictionary)
        if d.has_key(key):
            return d[key]

    return None 

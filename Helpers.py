import json

def append_line(str_list, line):
    str_list.append(line)
    str_list.append('\n')

def append_line_html(str_list, line):
    str_list.append(line)
    str_list.append('<br/>')

def dump_json_file(name, definition, path, sort = False):
    with open(path + name + ".json", "w") as f: 
        json.dump(definition, f, indent=4,sort_keys=sort)      

def dump_json_files(components, path):
    for name, definition in components:
        dump_json_file(name, definition, path)

def save_as_file(name, content, path, extension):
    with open(path + name + "." + extension, "w") as f: 
        f.write(content)

def append_to_file(name, content, path, extension):
    with open(path + name + "." + extension, "a") as f: 
        f.write(content)        

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except (ValueError, TypeError):
        return False

    if type(json_object) is int:
        return False
    return json_object
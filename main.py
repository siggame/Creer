from mako.template import Template, exceptions
from mako.lookup import TemplateLookup
from time import gmtime, strftime
import fnmatch
import os
import json
import sys
import argparse
import collections
import subprocess
import re

parser = argparse.ArgumentParser(description='Runs the Creer game generator with a main data file against imput templates to generate an output skeleton game framework')
parser.add_argument('-m, --main', action='store', dest='main', default='./main.data', help='the file that should be treated as the main data file for game generation')
parser.add_argument('-o, --output', action='store', dest='output', required=True, help='the path to the folder to put generated folders and files into.')
parser.add_argument('-i, --input', action='store', dest='input', nargs='+', required=True, help='the path(s) to look for templates in "_templates/" to build output from. can be a list of inputs seperated via spaces')
parser.add_argument('-c, --clean', action='store_true', dest='clean', default=False, help='if the output directory should be cleaned of existing files and folders before outputing generated files.')

args = parser.parse_args()

def extend(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = extend(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def list_dirs(path):
    folders = []
    while path != "" and path != None:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)
            break
    folders.reverse()
    return folders


def uncapitalize(s):
    return s[:1].lower() + s[1:] if s else ''

def extract_str(raw_string, start_marker, end_marker):
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def camel_case_to_underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

def copy_dict(source_dict, diffs):
    result=dict(source_dict) # Shallow copy
    result.update(diffs)
    return result


datas = {}
def parse_data(key, path):
    try:
        f = open(path)
        print("--PARSING", path)
        data = json.load(f)
        f.close()
    except ValueError as e:
        print("Error reading data file '" + path + "' -", e)
        sys.exit()
    else:
        datas[key] = data

try:
    git_hash = (subprocess.check_output(['git', 'rev-parse', 'HEAD'])).decode("utf-8").rstrip()
except:
    git_hash = "Error: git probably not installed"

parse_data("main", args.main)

extension = ".data"
for root, dirnames, filenames in os.walk('datas'):
    for filename in fnmatch.filter(filenames, "*" + extension):
        parse_data(os.path.splitext(filename)[0], os.path.join(root, filename))



### parsing the main data ###

parent_keys = ['main']
parent_datas = []
while len(parent_keys) > 0:
    parent_key = parent_keys.pop()
    parent_data = datas[parent_key]
    parent_datas.append(parent_data)

    # now look if that data had parent data to continue investigating
    if not '_parentDatas' in parent_data:
        parent_data['_parentDatas'] = []

    for new_parent_key in parent_data['_parentDatas']:
        parent_keys.append(new_parent_key)

parent_datas.append(datas['base']) # all games get this base data

prototype = {}
while len(parent_datas) > 0:
    extend(prototype, parent_datas.pop())

def default_game_obj(obj, key):
    if not 'description' in obj:
        raise Exception("no 'description' in obj '{0}'".format(key))

    if not 'parentClasses' in obj:
        obj['parentClasses'] = [] # parentClasses are classes defined in the data

    if not 'serverParentClasses' in obj:
        obj['serverParentClasses'] = [] # these are defined on the server and not exposed to clients

    if not 'attributes' in obj:
        obj['attributes'] = {}

    if not 'attributes' in obj:
        obj['attributes'] = {}

    for attribute_key, attribute_parms in obj['attributes'].items():
        if not 'description' in attribute_parms:
            raise Exception("no 'description' in obj '{0}'s attribute '{1}'.".format(key, attribute_key))
        if not 'type' in attribute_parms:
            raise Exception("no 'type' in obj '{0}'s attribute '{1}'.".format(key, attribute_key))
        if not 'default' in attribute_parms:
            attribute_parms['default'] = None

    default_functions_for(obj, key)

def default_functions_for(obj, key):
    if not 'functions' in obj:
        obj['functions'] = {}

    for function_key, function_parms in obj["functions"].items():
        if not 'description' in function_parms:
            raise Exception("no 'description' in obj '{0}'s function '{1}'".format(key, function_key))

        if not 'arguments' in function_parms:
            function_parms['arguments'] = []
        argument_names = []
        for i, arg_parms in enumerate(function_parms['arguments']):
            if not 'name' in arg_parms:
                raise Exception("no 'name' in obj '{0}'s function '{1}'s parameter at index {2}".format(key, function_key, i))
            if not 'description' in arg_parms:
                raise Exception("no 'description' in obj '{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms.name))
            if not 'type' in arg_parms:
                raise Exception("no 'type' in obj '{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms.name))
            if not 'default' in arg_parms:
                arg_parms['default'] = None
            argument_names.append(arg_parms['name'])
        function_parms['argument_names'] = argument_names

        if 'returns' in function_parms:
            if not 'description' in function_parms['returns']:
                raise Exception("no 'description' in obj '{0}'s function '{1}'s return".format(key, function_key))
            if not 'type' in function_parms['returns']:
                raise Exception("no 'type' in obj '{0}'s function '{1}'s return".format(key, function_key))
            if not 'default' in function_parms['returns']:
                function_parms['returns']['default'] = None
        else:
            function_parms['returns'] = None

game_objects = {}

game = prototype['Game']
game_name = game['name']
default_game_obj(game, game_name)

ai = prototype['AI']
del prototype['AI']
default_functions_for(ai, "AI")

if len(game['serverParentClasses']) == 0:
    game['serverParentClasses'].append("BaseGame")


for obj_key, obj in prototype.items():
    if obj_key == "Game" or obj_key[0] == "_":
        continue

    default_game_obj(obj, obj_key)

    if len(obj['parentClasses']) == 0 and len(obj['serverParentClasses']) == 0:
        obj['parentClasses'].append("GameObject")

    game_objects[obj_key] = obj


# attach parent attributes/functions

def inheritInto(obj, parent_class):
    parent = game_objects[parent_class]
    for parm_type in ["attributes", "functions"]:
        for parm_key, parm_parms in parent[parm_type].items():
            obj['inherited' + parm_type.capitalize()][parm_key] = copy_dict(parm_parms, {
                'inheritedFrom': parent_class
            })

    for parent_parent_class in parent['parentClasses']:
        inheritInto(obj, parent_parent_class)



for obj_key, obj in (copy_dict(game_objects, {'Game': game}).items()):
    obj['inheritedAttributes'] = {}
    obj['inheritedFunctions'] = {}

    for parent_class in obj['parentClasses']:
        inheritInto(obj, parent_class)




MERGE_KEYWORD_START_PRE = "<<-- Creer-Merge: "
MERGE_KEYWORD_START_POST = " -->>"
MERGE_KEYWORD_END_PRE = "<<-- /Creer-Merge: "
MERGE_KEYWORD_END_POST = " -->>"

def merge_with_data(data, pre_comment, key, alt):
    merged = []
    merged.extend([pre_comment, MERGE_KEYWORD_START_PRE, key, MERGE_KEYWORD_START_POST," - whatever you put inbetween this comment and the / will be auto-merged.\n"])
    if key in data:
        merged.append(data[key])
    else:
        merged.append(alt)
    merged.extend([pre_comment, MERGE_KEYWORD_END_PRE, key, MERGE_KEYWORD_END_POST])
    return "".join(merged)

def generate_merge_data(file_contents):
    data = {}
    recording = None
    for line in file_contents:
        if MERGE_KEYWORD_END_PRE in line:
            recording = None
        elif MERGE_KEYWORD_START_PRE in line:
            split = line.split()
            recording = extract_str(line, MERGE_KEYWORD_START_PRE, MERGE_KEYWORD_START_POST)
            data[recording] = []
        elif recording:
            data[recording].append(line)

    merge_data = {}
    for key, lines in data.items():
        merge_data[key] = "".join(lines)
    return merge_data



### generate templates ###

templates_folder = "_templates"
generated_files = []
template_header = ("Generated by Creer at " + strftime("%I:%M%p on %B %d, %Y UTC", gmtime()) + ", git hash: '" + git_hash + "'").replace("\n", ""). replace("\n", "") # yuk
for input_directory in args.input:
    full_path = os.path.join(input_directory, templates_folder)
    for root, dirnames, filenames in os.walk(full_path):
        for filename in filenames:
            extensionless, extension = os.path.splitext(filename)

            if extension == '.noCreer':
                continue

            filepath = os.path.join(root, filename)
            dirs = list_dirs(filepath)
            output_path = ""
            for i, d in enumerate(dirs):
                if d == templates_folder:
                    if i > 0:
                        output_path = os.path.join(dirs[i-1], *dirs[i+1:])
                    else:
                        output_path = os.path.join(*dirs[i+1:])
                    break

            print("templating", output_path)
            with open(filepath, "r") as read_file:
                lookup = TemplateLookup(directories=[os.path.dirname(filepath)])
                filecontents_template = Template(read_file.read(), lookup=lookup)

            filepath_template = Template(output_path, lookup=lookup)

            base_parameters = {
                'game': game,
                'game_name': game_name,
                'game_objs': game_objects,
                'ai': ai,
                'uncapitalize': uncapitalize,
                'camel_case_to_underscore': camel_case_to_underscore,
                'header': template_header,
                'json': json,
                'shared': {},
            }
            parameters = []

            if 'obj_key' in extensionless: # then we are templating for all the game + game objects
                parameters.append(copy_dict(base_parameters, {
                    'obj_key': "Game",
                    'obj': game,
                }))

                for obj_key, obj in game_objects.items():
                    parameters.append(copy_dict(base_parameters, {
                        'obj_key': obj_key,
                        'obj': obj
                    }))
            else:
                parameters.append(base_parameters)

            for p in parameters:
                try:
                    templated_path = filepath_template.render(**p)
                    system_path = os.path.join(args.output, templated_path)

                    merge_data = {}
                    if not args.clean and os.path.isfile(system_path): # then we need to have merge data in the existing file with the new one we would be creating
                        with open(system_path) as f:
                            content = f.readlines()
                            merge_data = generate_merge_data(content)

                    print("  -> generating", system_path)

                    def merge(pre_comment, key, alt):
                        print("    + merging", key)
                        return merge_with_data(merge_data, pre_comment, key, alt)
                    p['merge'] = merge

                    
                    generated_files.append({
                        'contents': filecontents_template.render(**p),
                        'path': system_path,
                    })
                except:
                    print(exceptions.text_error_template().render())
                    sys.exit()



### create the files ###

if args.clean:
    for the_file in os.listdir(args.output):
        file_path = os.path.join(args.output, the_file)
        try:
            os.unlink(file_path)
        except e:
            print(e)

for generated_file in generated_files:
    path =  generated_file['path']
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    contents = generated_file['contents']

    with open(path, 'wb') as temp_file:
        temp_file.write(bytes(contents, 'UTF-8'))

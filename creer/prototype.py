from creer.utilities import extend, copy_dict, sort_dict_keys
import creer.default as default
import creer.validate
import hashlib
import json

def _copy_from(obj, keys):
    d = {}
    for key in keys:
        d[key] = obj[key]
    return d

def _clean_functions(obj):
    cleaned = {}
    if 'functions' in obj:
        for func_name, func_data in obj['functions'].items():
            cleaned[func_name] = {
                'arguments': [],
                'returns': None,
            }

            for attr in func_data['arguments']:
                cleaned[func_name]['arguments'].append(_copy_from(attr, ['name', 'optional', 'type']))

            if func_data['returns']:
                cleaned[func_name]['returns'] = _copy_from(func_data['returns'], ['type'])
    return cleaned

def _clean_attributes(obj):
    cleaned = {}
    if 'attributes' in obj:
        for attr_name, attr_data in obj['attributes'].items():
            cleaned[attr_name] = _copy_from(attr_data, ['type'])
    return cleaned

def _proto_clean(proto):
    cleaned = {
        'AI': { 'functions': _clean_functions(proto['ai']) },
        'Game': {'attributes': _clean_attributes(proto['game']) },
    }

    for game_obj_name, game_obj in proto['game_objects'].items():
        cleaned[game_obj_name] = {
            'attributes': _clean_attributes(game_obj),
            'functions': _clean_functions(game_obj),
        }

    return cleaned

def _inherit_into(obj, parent_class, game_objects):
    parent = game_objects[parent_class]
    for parm_type in ["attributes", "functions"]:
        for parm_key, parm_parms in parent[parm_type].items():
            obj['inherited' + parm_type.capitalize()][parm_key] = copy_dict(parm_parms, {
                'inheritedFrom': parent_class
            })

    for parent_parent_class in parent['parentClasses']:
        _inherit_into(obj, parent_parent_class, game_objects)

def build(datas):
    parent_keys = ['main']
    parent_datas = []
    parent_data_names = []
    while len(parent_keys) > 0:
        parent_key = parent_keys.pop()
        parent_data = datas[parent_key]
        if parent_key != 'main':
            parent_data_names.append(parent_key)
        parent_datas.append(parent_data)

        # now look if that data had parent data to continue investigating
        if not '_parentDatas' in parent_data:
            parent_data['_parentDatas'] = []

        for new_parent_key in parent_data['_parentDatas']:
            parent_keys.append(new_parent_key)

    parent_datas.append(datas['base']) # all games get the base data

    # merge all the prototypes inherited into one prototype
    prototype = {}
    for parent_data in reversed(parent_datas):
        extend(prototype, parent_data)

    # extend won't do this correctly. multiple data may pre-define parent classes and will get overwritten via extend. this appends each additional class name
    for proto_key, proto in prototype.items():
        if proto_key[0] == "_":
            continue

        newServerParentClasses = []
        if 'serverParentClasses' in proto:
            for parent_data in reversed(parent_datas):
                if proto_key in parent_data and 'serverParentClasses' in parent_data[proto_key]:
                    for parent_class_name in parent_data[proto_key]['serverParentClasses']:
                        newServerParentClasses.append(parent_class_name)
        proto['serverParentClasses'] = newServerParentClasses

    game_objects = {}
    game = prototype['Game']
    if not 'name' in game:
        raise Exception("Error: no name given for the main game data. Name your Game!!!")
    default.game_obj(game, "Game")

    ai = prototype['AI']
    del prototype['AI']
    default.functions_for(ai, "AI")

    if len(game['serverParentClasses']) == 0:
        game['serverParentClasses'].append("BaseGame")

    for obj_key, obj in prototype.items():
        if obj_key == "Game" or obj_key[0] == "_":
            continue

        if obj_key == "GameObject" and len(obj['serverParentClasses']) == 0:
            obj['serverParentClasses'] = [ 'BaseGameObject' ]

        default.game_obj(obj, obj_key)

        if obj_key != "GameObject" and len(obj['parentClasses']) == 0:
            obj['parentClasses'].append("GameObject")

        game_objects[obj_key] = obj

    for obj_key, obj in (copy_dict(game_objects, {'Game': game}).items()):
        obj['inheritedAttributes'] = {}
        obj['inheritedFunctions'] = {}

        for parent_class in obj['parentClasses']:
            _inherit_into(obj, parent_class, game_objects)

    # now all the prototypes should be built, so sort the attribute/function keys
    for proto_key, proto in prototype.items():
        if proto_key[0] == '_':
            continue

        proto['function_names'] = sort_dict_keys(proto['functions'])
        proto['attribute_names'] = sort_dict_keys(proto['attributes'])
        proto['inheritedFunction_names'] = sort_dict_keys(proto['inheritedFunctions'])
        proto['inheritedAttribute_names'] = sort_dict_keys(proto['inheritedAttributes'])
    ai['function_names'] = sort_dict_keys(ai['functions'])

    creer.validate.validate(prototype)

    proto = {
        'game_objects': game_objects,
        'game': game,
        'ai': ai
    }

    min_game_data = _proto_clean(proto)
    as_string = json.dumps(min_game_data, sort_keys=True)
    as_bytes = bytes(as_string, 'utf8')

    sha = hashlib.sha256()
    sha.update(as_bytes)

    proto['parent_data_names'] = parent_data_names
    proto['game_version'] = sha.hexdigest()

    return proto

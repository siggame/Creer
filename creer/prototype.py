from creer.utilities import extend, copy_dict, sort_dict_keys
import creer.default as default

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
    while len(parent_keys) > 0:
        parent_key = parent_keys.pop()
        parent_data = datas[parent_key]
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

        if len(obj['parentClasses']) == 0 and len(obj['serverParentClasses']) == 0:
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
    ai['function_names'] = sort_dict_keys(ai['functions'])

    return {
        'game_objects': game_objects,
        'game': game,
        'ai': ai
    }

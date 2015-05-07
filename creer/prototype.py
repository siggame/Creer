from creer.utilities import extend, copy_dict
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

    parent_datas.append(datas['base']) # all games get this base data

    prototype = {}
    while len(parent_datas) > 0:
        extend(prototype, parent_datas.pop())

    game_objects = {}
    game = prototype['Game']
    default.game_obj(game, "Game")

    ai = prototype['AI']
    del prototype['AI']
    default.functions_for(ai, "AI")

    if len(game['serverParentClasses']) == 0:
        game['serverParentClasses'].append("BaseGame")

    for obj_key, obj in prototype.items():
        if obj_key == "Game" or obj_key[0] == "_":
            continue

        default.game_obj(obj, obj_key)

        if len(obj['parentClasses']) == 0 and len(obj['serverParentClasses']) == 0:
            obj['parentClasses'].append("GameObject")

        game_objects[obj_key] = obj

    for obj_key, obj in (copy_dict(game_objects, {'Game': game}).items()):
        obj['inheritedAttributes'] = {}
        obj['inheritedFunctions'] = {}

        for parent_class in obj['parentClasses']:
            _inherit_into(obj, parent_class, game_objects)

    return {
        'game_objects': game_objects,
        'game': game,
        'ai': ai
    }

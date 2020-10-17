# this validates a prototype to ensure none of the data/types/setup will screw with an output template
# basically, this validates Creer input data after it has been parsed

import re

_primitives = [
    'string',
    'boolean',
    'int',
    'float',
    'list',
    'dictionary'
]

_dangerous_names = [
    'true',
    'false',
    'if',
    'else',
    'continue',
    'for',
    'end',
    'function',
    'pass',
    'assert',
    'eval',
    'break',
    'import',
    'from',
    'catch',
    'finally',
    'null',
    'while',
    'double',
    'float',
    'goto',
    'return'
]

_valid_types = []
_game_classes = []

def _check(obj, location, key, expected_type):
    if type(obj) != dict:
        raise Exception(location + " is not a dict to check if it contains " + key)

    if not key in obj:
        raise Exception("No '{}' in {}".format(key, location))

    if type(obj[key]) != expected_type:
        raise Exception("{}[{}] is not the expected type '{}'".format(location, key, expected_type))



def _validate_type(obj, location, type_key="type"):
    _check(obj, location, type_key, dict)
    type_obj = obj[type_key]

    _check(type_obj, location + "'s type", "name", str)
    name = type_obj['name']

    if name == "list" or name == "dictionary":
        _validate_type(type_obj, "{}.{}[valueType]".format(location, name), "valueType")

        if name == "dictionary":
            if not 'keyType' in type_obj:
                raise Exception("No 'keyType' for type '{}' at '{}'".format(name, location))

            _validate_type(type_obj, "{}.{}[keyType]".format(location, name), "keyType")

    if not name in _valid_types:
        raise Exception("Type named '{}' is not a primitive or custom class in {}.".format(name, location))

def _validate_description(obj, location):
    _check(obj, location, "description", str)
    desc = obj["description"]

    for c in ['"', "\n", "\t", "\r"]:
        if c in desc:
            escaped = c.translate(str.maketrans({"-":  r"\-", "]":  r"\]", "\\": r"\\", "^":  r"\^", "$":  r"\$", "*":  r"\*", ".":  r"\."}))
            raise Exception("{} description contains illegal character {}".format(location, escaped))

    if desc[0].upper() != desc[0]:
        raise Exception("Capitalize your doc string in " + location + "'s description")

    if desc[-1] != ".":
        raise Exception("End your doc strings as sentences with periods in " + location + "'s description")

_required = {
    'type': _validate_type,
    'description': _validate_description
}

def _check_required(obj, location, additional_reqs=None):
    for key, call in _required.items():
        call(obj, location)

    if additional_reqs:
        for key, expected_type in additional_reqs.items():
            _check(obj, location, key, expected_type)

def _validate_name(key, obj, pascal=False):
    base_err = '"{}" is not a valid name for {}. '.format(key, obj)

    search_re = '([A-Z][a-z]+)+' if pascal else '([a-z]+([A-Za-z])?)+'
    casing = 'PascalCase' if pascal else 'camelCase'
    match = re.search(search_re, key)
    if not match or match[0] != key:
        raise Exception(base_err + 'Name must be in {}.'.format(casing))

    if key.lower() in _primitives:
        raise Exception(base_err + 'Too similar to primitive type.')

    if key.lower() in _dangerous_names:
        raise Exception(base_err + 'Name too similar to popular programming keywords for some clients.')


###############################################################################
##                          Public Function To Call                          ##
###############################################################################

def validate(prototype):
    for primitive in _primitives:
        _valid_types.append(primitive)

    for key, value in prototype.items():
        if key[0] != "_" and key != "Game" and key != "AI":
            _validate_name(key, "custom Game Object", pascal=True)

            _game_classes.append(key)
            _valid_types.append(key)

    for key, value in prototype.items():
        if key.startswith("_"):
            continue

        if key is not "AI":
            _validate_description(value, key)
            _check(value, key, 'attributes', dict)

            for attr_key, attr in value['attributes'].items():
                _check_required(attr, key + "." + attr_key)

            if key is not "Game" and key is not "GameObject":
                if not "parentClasses" in value:
                    raise Exception(key + " expected to be game object sub class, but has no parent class(es)")
                for parent_class in value['parentClasses']:
                    if not parent_class in _game_classes:
                        raise Exception("{} has invalid parentClass '{}'".format(key, parent_class))

        for attr_name, attr in value['attributes'].items():
            _validate_name(attr_name, 'an attribute in ' + key)

        _check(value, key, 'functions', dict)
        for funct_key, funct in value['functions'].items():
            loc = key + "." + funct_key
            _check(funct, loc, "description", str)
            if "arguments" in funct:
                _check(funct, loc, "arguments", list)
                optional = None
                for i, arg in enumerate(funct['arguments']):
                    arg_loc = "{}.arguments[{}]".format(loc, i)
                    _check_required(arg, arg_loc, {'name': str })
                    _validate_name(arg['name'], arg_loc)
                    arg_loc += " (" + arg['name'] + ")"

                    if 'default' in arg and arg['default'] != None:
                        default = arg['default']
                        optional = i
                        def_type = arg['type']['name']
                        type_of_default = type(default)
                        if def_type == "string":
                            if type_of_default != str:
                                raise Exception("{} default value should be a string, not a {}".format(arg_loc, type_of_default))
                        elif def_type == "int":
                            if type_of_default != int:
                                raise Exception("{} default value should be an integer, not a {}".format(arg_loc, type_of_default))
                        elif def_type == "float":
                            if type_of_default != int and type_of_default != float:
                                raise Exception("{} default value should be a float, not a {}".format(arg_loc, type_of_default))
                        elif def_type == "boolean":
                            if type_of_default != bool:
                                raise Exception("{} default value should be a bool, not a {}".format(arg_loc, type_of_default))
                        else: # dict, list, or GameObject
                            if type_of_default != type(None):
                                raise Exception("{} default value must be null for dictionaries/lists/GameObjects, not a {}".format(arg_loc, type_of_default))

                    if optional != None and not 'default' in arg:
                        raise Exception("{} has no default to make it optional, by prior index {} was optional. Optional args must all be at the end.".format(arg_loc, i))

            if 'returns' in funct and funct['returns'] != None:
                _check_required(funct['returns'], loc + ".returns")
                if 'invalidValue' not in funct['returns']:
                    raise Exception("{} requires an invalidValue for the return".format(loc))

                type_of_invalidValue = type(funct['returns']['invalidValue'])
                expected_type_name_of_invalidValue = funct['returns']['type']['name']
                if expected_type_name_of_invalidValue == 'string' and type_of_invalidValue != str:
                    raise Exception("{}.invalidValue is not of expected string type (was {})".format(loc, type_of_invalidValue))
                if expected_type_name_of_invalidValue == 'boolean' and type_of_invalidValue != bool:
                    raise Exception("{}.invalidValue is not of expected boolean type (was {})".format(loc, type_of_invalidValue))
                if expected_type_name_of_invalidValue == 'int' and type_of_invalidValue != int:
                    raise Exception("{}.invalidValue is not of expected int type (was {})".format(loc, type_of_invalidValue))
                if expected_type_name_of_invalidValue == 'float' and type_of_invalidValue != int and type_of_invalidValue != float:
                    raise Exception("{}.invalidValue is not of expected int type (was {})".format(loc, type_of_invalidValue))

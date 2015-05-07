def default_type(obj, key):
    if not 'type' in obj:
        raise Exception("no type to default for " + key)

    if obj['type'] == "array" or obj['type'] == "dictionary":
        if not 'valueType' in obj:
            raise Exception("no valueType for " + key)
    else:
        obj['valueType'] = None

    if obj['type'] == "dictionary":
        if not 'keyType' in obj:
            raise Exception("no keyType for " + key)
    else:
        obj['keyType'] = None

    if obj['type'] == "dictionary" and obj['type'] == "array":
        if not 'valueType' in obj:
            raise Exception("no valueType for " + key)
    else:
        obj['valueType'] = None

def game_obj(obj, key):
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
        default_type(attribute_parms, "'{0}'s attribute '{1}'.".format(key, attribute_key))
        if not 'description' in attribute_parms:
            raise Exception("no 'description' in obj '{0}'s attribute '{1}'.".format(key, attribute_key))
        if not 'default' in attribute_parms:
            attribute_parms['default'] = None

    functions_for(obj, key)

def functions_for(obj, key):
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
            default_type(arg_parms, "'{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms['name']))
            if not 'description' in arg_parms:
                raise Exception("no 'description' in obj '{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms.name))
            if not 'default' in arg_parms:
                arg_parms['default'] = None
            argument_names.append(arg_parms['name'])
        function_parms['argument_names'] = argument_names

        if 'returns' in function_parms:
            default_type(function_parms['returns'], "obj '{0}'s function '{1}'s return".format(key, function_key))
            if not 'description' in function_parms['returns']:
                raise Exception("no 'description' in obj '{0}'s function '{1}'s return".format(key, function_key))
            if not 'default' in function_parms['returns']:
                function_parms['returns']['default'] = None
        else:
            function_parms['returns'] = None
def default_type(obj, type_key='type', parent_name='"no parent name"'):
    if not type_key in obj:
        raise Exception("no type to default for " + parent_name)

    if isinstance(obj[type_key], str): # transform it to a dict
        obj[type_key] = { 'name': obj[type_key] }

    this_type = obj[type_key]

    if not 'name' in this_type:
        raise Exception("no name for type in " + parent_name)

    if this_type['name'] == "list" or this_type['name'] == "dictionary":
        if not 'valueType' in this_type:
            raise Exception("no valueType for " + parent_name)
        else:
            default_type(this_type, 'valueType', parent_name)
    else:
        this_type['valueType'] = None

    if this_type['name'] == "dictionary":
        if not 'keyType' in this_type:
            raise Exception("no keyType for " + parent_name)
        else:
            default_type(this_type, 'keyType', parent_name)
    else:
        this_type['keyType'] = None

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
        default_type(attribute_parms, 'type', "'{0}'s attribute '{1}'.".format(key, attribute_key))
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

        if not 'serverPredefined' in function_parms:
            function_parms['serverPredefined'] = False

        if not 'arguments' in function_parms:
            function_parms['arguments'] = []
        argument_names = []
        must_be_optional = False
        for i, arg_parms in enumerate(function_parms['arguments']):
            if not 'name' in arg_parms:
                raise Exception("no 'name' in obj '{0}'s function '{1}'s parameter at index {2}".format(key, function_key, i))
            default_type(arg_parms, 'type', "'{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms['name']))
            if not 'description' in arg_parms:
                raise Exception("no 'description' in obj '{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms['name']))
            if not 'default' in arg_parms:
                if must_be_optional:
                    raise Exception("all args must be optional from this point in obj '{0}'s function '{1}'s parameter '{2}'".format(key, function_key, arg_parms['name']))
                arg_parms['default'] = None
                arg_parms['optional'] = False
            else: # they defined a default value, so this argument is optional
                arg_parms['optional'] = True
                if not 'optionals_start_index' in function_parms:
                    function_parms['optionals_start_index'] = i
                    function_parms['optionals'] = 0
                function_parms['optionals'] += 1
                must_be_optional = True
            argument_names.append(arg_parms['name'])
        function_parms['argument_names'] = argument_names

        if 'returns' in function_parms:
            default_type(function_parms['returns'], 'type', "obj '{0}'s function '{1}'s return".format(key, function_key))
            if not 'description' in function_parms['returns']:
                raise Exception("no 'description' in obj '{0}'s function '{1}'s return".format(key, function_key))
            if not 'default' in function_parms['returns']:
                function_parms['returns']['default'] = None
        else:
            function_parms['returns'] = None
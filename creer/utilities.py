import re
import os
import collections.abc as collections
import operator

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

def camel_case_to_hyphenate(name):
    s1 = first_cap_re.sub(r'\1-\2', name)
    return all_cap_re.sub(r'\1-\2', s1).lower()

def copy_dict(source_dict, diffs):
    result=dict(source_dict) # Shallow copy
    result.update(diffs)
    return result

def sort_dict_keys(d):
    return sorted(d)

def sort_dict_values(d):
    return sorted(d.items(), key=operator.itemgetter(0))

def upcase_first(s):
    return s[0].upper() + s[1:]

def lowercase_first(s):
    return s[0].lower() + s[1:]

def human_string_list(strs, conjunction='or'):
    n = len(strs)
    if n == 0:
        return ''
    if n == 1:
        return str(strs[0])
    if n == 2:
        return '{} {} {}'.format(strs[0], conjunction, strs[1])
    # else list of >= 3
    strs_safe = list(strs)
    strs_safe[-1] = '{} {}'.format(conjunction, strs_safe[-1])
    return ', '.join(strs_safe)

def is_primitive_type(type_obj):
    return (type_obj['name'] in ['null', 'boolean', 'int', 'float', 'string', 'list', 'dictionary'])

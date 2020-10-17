import os
import json
import yaml
import fnmatch
import creer

_parser = {
    'json': json,
    'data': json,
    'yaml': yaml
}


def _parse_data(datas, key, path):
    filename, ext = os.path.splitext(path)

    try:
        print("-- PARSING", path)
        with open(path, 'r') as file:
            data = _parser[ext[1:].lower()].safe_load(file)
    except ValueError as e:
        print("Error reading data file '" + path + "' -", e)
        raise Exception("Error reading data file")
    else:
        datas[key] = data


def parse(main_path):
    datas = {}
    found = os.path.isfile(main_path)
    if not found:
        for extension in _parser.keys():
            generic_path = os.path.join(creer.GAMES_DIR, main_path, 'creer.' + extension)
            found = os.path.isfile(generic_path)
            if found:
                main_path = generic_path
                break

    if not found:
        raise Exception("main.data path (" + main_path + ") not valid as generic path or actual path.")

    _parse_data(datas, "main", main_path)

    for extension in _parser.keys():
        for root, dirnames, filenames in os.walk('datas'):
            for filename in fnmatch.filter(filenames, "*" + extension):
                _parse_data(datas, os.path.splitext(filename)[0], os.path.join(root, filename))

    return datas

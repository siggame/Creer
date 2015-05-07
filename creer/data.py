import os
import json
import fnmatch

def _parse_data(datas, key, path):
    try:
        f = open(path)
        print("--PARSING", path)
        data = json.load(f)
        f.close()
    except ValueError as e:
        print("Error reading data file '" + path + "' -", e)
        raise Exception("Error reading data file")
    else:
        datas[key] = data

def parse(main_path):
    datas = {}
    _parse_data(datas, "main", main_path)

    extension = ".data"
    for root, dirnames, filenames in os.walk('datas'):
        for filename in fnmatch.filter(filenames, "*" + extension):
            _parse_data(datas, os.path.splitext(filename)[0], os.path.join(root, filename))

    return datas

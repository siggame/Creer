import glob
from os import path
from creer.template import templates_folder

def validate(inputs):
    validated_inputs = []
    for input_dir in inputs:
        dirs = glob.glob(input_dir)
        if not dirs:
            raise Exception("No directories matching {}".format(input_dir))

        if not glob.glob(path.join(input_dir, templates_folder)):
            raise Exception("Cannot template a directory with no Creer templates!\nNo template directory '{}' in {}".format(templates_folder, input_dir))
        validated_inputs.extend(dirs)

    for validated_input in validated_inputs:
        print(">> Input Directory:", validated_input)

    return validated_inputs

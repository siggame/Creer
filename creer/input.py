import glob

def validate(inputs):
    validated_inputs = []
    for input_dir in inputs:
        dirs = glob.glob(input_dir)
        if not dirs:
            raise Exception("No directories matching {}".format(input_dir))
        validated_inputs.extend(dirs)

    for validated_input in validated_inputs:
        print(">> Input Directory:", validated_input)

    return validated_inputs

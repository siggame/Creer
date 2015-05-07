import os

def write(generated_files):
    for generated_file in generated_files:
        path =  generated_file['path']
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        contents = generated_file['contents']

        with open(path, 'wb') as temp_file:
            temp_file.write(bytes(contents, 'UTF-8'))

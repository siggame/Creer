import os
from shutil import copyfile

def write(generated_files):
    for generated_file in generated_files:
        if 'copy-from' in generated_file:
            # we just need to copy the file from to dest
            copyfile(generated_file['copy-from'], generated_file['copy-dest'])
        else:
            # we have templated contents to write
            path = generated_file['path']
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            contents = generated_file['contents']

            with open(path, 'wb') as temp_file:
                temp_file.write(bytes(contents, 'UTF-8'))

import creer.data
import creer.prototype
import creer.template
import creer.writer
import creer.input

def run(game, inputs, output, merge=False, tagless=False, no_write=False):
    datas = creer.data.parse(game)

    proto = creer.prototype.build(datas)

    inputs = creer.input.validate(inputs)

    generated_files = creer.template.build_all(proto, inputs, output, merge, tagless)

    if not no_write:
        creer.writer.write(generated_files)
    else:
        print("Creer Success! Not writing any files.")

import creer.data as data
import creer.prototype as prototype
import creer.template as template
import creer.writer as writer

def run(main, input, output, merge=False):
    datas = data.parse(main)

    proto = prototype.build(datas)

    generated_files = template.build_all(proto, input, output, merge)

    writer.write(generated_files)

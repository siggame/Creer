import os
import creer.data
import creer.prototype
import creer.template
import creer.writer
import creer.input

GAMES_DIR = '../Games/'


def run(games, inputs, output, merge=False, tagless=False, no_write=False):
    if len(games) == 0:
        raise Exception('No game(s) provided to run Creer against')

    if len(games) == 1 and games[0].lower() == 'all':
        # then games is actually the list of all the game names, by dir names
        games = [
            name for name in sorted(os.listdir(GAMES_DIR))
            if os.path.isdir(os.path.join(GAMES_DIR, name))
        ]

    all_generated_files = []
    for game in games:
        print('~~~~~~ {} ~~~~~~'.format(game))
        datas = creer.data.parse(game)

        proto = creer.prototype.build(datas)

        inputs = creer.input.validate(inputs)

        all_generated_files.append(
            creer.template.build_all(proto, inputs, output, merge, tagless)
        )

    if not no_write:
        for generated_files in all_generated_files:
            creer.writer.write(generated_files)
    else:
        print("Creer Success! Not writing any files.")

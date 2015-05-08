import argparse
import creer

parser = argparse.ArgumentParser(description='Runs the Creer game generator with a main data file against imput templates to generate an output skeleton game framework')
parser.add_argument('-g, --game', action='store', dest='game', default='./main.data', help='the file that should be treated as the main data file for game generation')
parser.add_argument('-o, --output', action='store', dest='output', help='the path to the folder to put generated folders and files into. If omitted it will output and overwrite the input files')
parser.add_argument('-i, --input', action='store', dest='input', nargs='+', help='the path(s) to look for templates in "_templates/" to build output from. can be a list of inputs seperated via spaces. defaults to all the siblings directories with creer templates.')
parser.add_argument('--clean', action='store_true', dest='clean', default=False, help='if the output files should NOT be merged with existing files')

args = parser.parse_args()

creer.run(args.game, args.input, args.output, args.clean)

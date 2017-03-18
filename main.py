import argparse
import creer

parser = argparse.ArgumentParser(description='Runs the Creer game generator with a main data file against imput templates to generate an output skeleton game framework')
parser.add_argument('games', nargs='*', action='store', help='the file(s) or game names that should be treated as the main data file/folder for game generation. Must be json or yaml')
parser.add_argument('-o, --output', action='store', dest='output', help='the path to the folder to put generated folders and files into. If omitted it will output and overwrite the input files')
parser.add_argument('-i, --input', action='store', dest='inputs', nargs='+', help='the path(s) to look for templates in "_templates/" to build output from. can be a list of inputs seperated via spaces. defaults to all the siblings directories with creer templates.')
parser.add_argument('--merge', action='store_true', dest='merge', default=False, help='if the output files should be merged with existing files')
parser.add_argument('--tagless', action='store_true', dest='tagless', default=False, help='if the Creer-Merge tags should be omitted (a merge is still possible if the input sources have tags).')
parser.add_argument('--test', action='store_true', dest='no_write', default=False, help='If you do not want files to be output (basically validates the generation)')

args = parser.parse_args()

creer.run(**vars(args))

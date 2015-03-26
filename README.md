# Creer
The automatic code generating script for the Cadre framework

## How to use
`python main.py -m {main.data file} -i {../list/of/folders ./that/have/a/_templates/folder/ in/them} -o {path/to/output/folder}`

## Templates
Every folder in the `-i` input folders should have a `_templates/` folder present inside it. the folder/file names inside it should be using Mako syntax. if the file contains `${obj_key}` then every game class within the game data you are evaluating for will be generated. For examples look at the Cerveau and Joeur clients that are part of the Cadre framework.

## Other notes
Try to have git installed via your command line `git` so the version of this repo can be added to the generated files.

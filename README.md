# Creer
The automatic code generating script for the Cadre framework, intending to create base code for a simple game strcture for the rest of the framework.

![{Cadre}](http://i.imgur.com/17wwI3f.png)

All inspiration taken from [MS&T's SIG-GAME framework](https://github.com/siggame), and most of the terminology is assuming some familiarity with it as this is a spiritual successor to it.

## How to use
`python main.py -m {main.data file} -i {../list/of/folders ./that/have/a/_templates/folder/ in/them} -o {path/to/output/folder}`

## Templates
Every folder in the `-i` input folders should have a `_templates/` folder present inside it. the folder/file names inside it should be using Mako syntax. if the file contains `${obj_key}` then every game class within the game data you are evaluating for will be generated. For examples look at the Cerveau and Joeur clients that are part of the Cadre framework.

## Other notes
Try to have git installed via your command line `git` so the version of this repo can be added to the generated files. This will help in tracking if files were updated when pushed.

## Other notes

This is a polished proof-of-concept part of the Cadre framework. There are plently of bugs and issues present. The purpose at this time is not to be perfect, but to show that this framework is robust and meets all the needs of MS&T's ACM SIG-GAME.

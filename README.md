# Creer
The automatic code generating script for the Cadre framework, intending to create base code for a simple game structure for the rest of the framework.

![{Cadre}](http://i.imgur.com/17wwI3f.png)

All inspiration taken from [MST's SIG-GAME framework](https://github.com/siggame), and most of the terminology is assuming some familiarity with it as this is a spiritual successor to it.

## Requirements
[Python](https://www.python.org/) 3.4.3+ is required, as are the python packages [Mako](http://www.makotemplates.org/), [binaryornot](https://github.com/audreyr/binaryornot), and [PyYAML](http://pyyaml.org/wiki/PyYAML).

To install all these python packages, using `pip` is probably your best bet.

`pip install -r requirements.txt`

## How to use
First, pull cadre
'git clone https://github.com/siggame/Cadre.git'

Next, go into the cadre foldier and run this:
'./init.sh'
You should get messages out it successfully downloading the different repositories. If it fails:
replace "git@github.com:" in each of the url paths with "https://github.com/"
If it still doesn't work, contact fellow siggame members for support.
This is then the point where you would run `pip install -r requirements.txt`

Finally you can type the gen command. use --test to just test if it works without writing anything.
'python main.py [game name] -i ../Cerveau -o .. --test'

you may remove the -o and it will dump it in the default output file, and you may replace .. with whatever destination you wish.

### Merging
One of the biggest pains with the old codegen was manually merging code between codegen runs. Creer is smart and can do the merging for you! Just add the `--merge` tag and target the Cadre repo you want to merge as the input and output, and it will automatically merge your code changes via code introspection.

## Templates
Every folder in the `-i` input folders should have a `_templates/` folder present inside it. the folder/file names inside it should be using Mako syntax. if the file contains `${obj_key}` then every game class within the game data you are evaluating for will be generated. For examples look at the Cerveau and Joueur clients that are part of the Cadre framework.

The syntax is all [Mako](http://www.makotemplates.org/), to give you the full power of Python when templating your Cadre projects.

If your file is a binary files (such as an image), it's file path will still be templated, however it's contents will not and it will just be copied to the output directory/directories like any other file.

## Game Structure
Games are defined by a data file that describes the Game, GameObjects within it, and the AI competitors code, and the entire structure is incredibly flexible.

### Data File
Each main data file should describe your game structure, and can inherit from other data files to keep games DRY.

All of these are kept within the `data/` directory. `base.yaml` is the base game prototype. It will be included in every game, regardless if you explicitly included it or not.

The rest are optional. Though generally for MegaMinerAI type games you will want to include `turnBased` and `twoPlayer` as parent datas.

For examples on other data files, see the various already completed [Cadre games](https://github.com/siggame/Creer/tree/master/datas).

### Types
All variables are cross language safe and can be any type of:
* `void`: No type (null)
* `int`: Integer
* `float`: Floating Point Number
* `string`: Text
* `boolean`: True or False
* `GameObject`: An instance of a game object class defined in the data file. Considered "primitive" to clients to support cool things like cycles.
* `list<valueType>`: An ordered container of another game object. Can be multi-dimensional (e.g. a list of lists of ints)
* `dictionary<keyType, valueType>`: A mapping of keys to values, and just as lists can be multi-dimensional.

Obviously different languages support these "primitives" in different ways, but all Creer compatible projects should use the fastest, most popular and easy to understand implementation (e.g. use standard libraries and practices).

With support for basically all the primitives, and more complex containers and classes *any* game structure should be possible. Supporting more complex ideas such as cycles (e.g. a GameObject having reference to itself), and multi-dimensional containers prevents "hacks" that other games using older frameworks needs such as "UnitTypes" classes which held static variables on "Unit" classes.

**Note**: Just because you can make weird data structures, like a dictionary indexed by lists mapping to another dictionary...and so on, does no mean you should. Generally we only recommend lists and dictionaries be valued by non list/dictionary primitives. Multi-dimensional data structures get weird cross language, and you are probably making your game API too complex for competitors at that point.

### Functions
All functions, both as part of GameObjects and the AI classes can take any number of arguments of any of the above types (with optional args), and returns any type. AI returns are sent back to the server and GameObject returns are purely server side with the result "returned" over the TCP socket connection to clients.

### Documentation
Every class, attribute, function, argument, etc **must** be documented. If you fail to provide a description in your data somewhere Creer will tell you. This is so heavily enforced because Creer writes code that other developers and competitors need to understand quickly, so proper and robust documentation is key.

## Other notes
Try to have git installed via your command line `git` so the version of this repo can be added to the generated files. This will help in tracking if files were updated when pushed.

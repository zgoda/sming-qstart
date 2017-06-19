# Sming-Quickstart

Quickstarts your [Sming](https://github.com/SmingHub/Sming) project. This program checks if your environment is sane and creates basic project structure using [sming-skel](https://github.com/zgoda/sming-skel) as a base. It is written in Python and does not require anything besides Python stdlib.

Linux only, tested on Python 2.7 and 3.5 (will not work with Python 2.6 or earlier, may work with Python 3.6 or newer).

## Invocation

```
$ python sming-qstart.py --help
usage: sming-qstart.py [-h] [-v | -s] [--skip-sanity-check] [--skip-git-init]
                       [--skip-git-commit]
                       name

Sming project quickstart

positional arguments:
  name                 project directory name, may be relative or absolute
                       path

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        run in verbose mode [default: False]
  -s, --silent         run in silent mode [default: False]
  --skip-sanity-check  skip environment sanity check
  --skip-git-init      skip local git repository initialization
  --skip-git-commit    skip initial git commit
```

## Sanity checks

At the beginning this program will check if you have defined `ESP_HOME` and `SMING_HOME` in your environment and will warn you if not. You can continue and set it up later in `Makefile-user.mk` but [Visual Studio Code](https://code.visualstudio.com/) integration will not function properly until these variables are present or you manually edit `.vscode/c_cpp_properties.json` and set search/include paths. No action will be required if you followed [Sming installation instructions](https://github.com/SmingHub/Sming/wiki/Linux-Quickstart).

## Git initialization

This program will initialize empty local git repository and add initial commit when all project initialization is done. You will be asked if you want this and the step will be skipped if you opt to not initialize repository. This step will be skipped silently if git executable is not found in `$PATH`.

## Licensing

The program itself is licensed under GPL v3. It may be safely used commercially unless you want to modify it and distribute. The skeleton that makes the base of new project is licensed under MIT license so you are free to use it as you see fit. I explicitly **do not require** that you put any attribution to sming-skel in your project source files nor in any textual documentation, although this will be nice.

import importlib
from os import listdir
from os.path import join, isdir, dirname, abspath

here = abspath(dirname(__file__))
langs = [f for f in listdir(here) if isdir(join(here, f)) and not f.startswith('__')]

TRANSLATION = {}
BLOCKS = {}

for lang in langs:
    TRANSLATION[lang] = importlib.import_module(f'constants.{lang}.translation')
    BLOCKS[lang] = importlib.import_module(f'constants.{lang}.blocks')

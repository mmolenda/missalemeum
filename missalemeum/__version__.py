import os
try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__')) as fh:
        __version__ = fh.read().strip()
except FileNotFoundError:
    __version__ = "UNVERSIONED"

"""
This file is the main entry point for Pygrr PolyArt.
"""

# import used functions from modules sys and os
from sys import path, argv
from os import path as ospath, chdir

# add polyart's location to the module search paths

path.append(ospath.abspath(ospath.join(ospath.dirname(__file__), "..")))
try:
    chdir(argv[0])
except Exception:
    pass

# print blankline
print("")
# run polyart
import polyart

"""
 ______________________________________________
{                                              }
{  CREDITS:                                    }
{                                              }
{  'pygrr polyart' was made by IsaacTFM        }
{  This includes the code, concept, and logo.  }
{  (unless otherwise specified)                }
{                                              }
{  Find me at: www.isaactfm.com                }
{______________________________________________}
          |    |                |    |
          |    |                |    |
         _|____|_              _|____|_
        /________\            /________\

"""

# Polyart MUST be run by importing the package, __main__, or __init__.

# if this is the origin file (not imported)
if __name__ == "__main__":
    # open __main__ - the entry point
    from sys import path
    from os import path as ospath
    path.append(ospath.abspath(ospath.join(ospath.dirname(__file__), "..")))
    import polyart
    # exit this runtime
    quit()


# ------------------------------------------------------------------------ #
#                          validate version                                #
# ------------------------------------------------------------------------ #
# region validate version


__minpyversion__ = (3, 7)  # 3.7+
from sys import version_info
assert version_info >= __minpyversion__


# endregion
# ------------------------------------------------------------------------ #
#                          initialise code                                 #
# ------------------------------------------------------------------------ #
# region initialise code


# setup notice
__version__ = "1.0 Alpha"
__date__ = "2021"
__dependencies__ = {
        "Smallest enclosing circle - Library (Python)": "Copyright (c) 2020 Project Nayuki - https://www.nayuki.io/page/smallest-enclosing-circle",
}


# endregion
# ------------------------------------------------------------------------ #
#                          constants                                       #
# ------------------------------------------------------------------------ #
# region constants

# program settings
SCALE = 20
GRIDSIZE = 20
POINTSIZE = 5
POINTSELECTDISTANCE = POINTSIZE * 1.5
ORIGINSIZE = 10
CENTERHULLGRAPHICSIZE = 3

# program colors
GRIDCOLOR = "#eaeaea"
COLLIDERCOLOR = "#ff0000"
POINTCOLOR = "#000000"
BACKGROUNDCOLOR = "#ffffff"
ORIGINCOLOR = "#000000"

# ui colors
HEADERCOLOR = "#151515"
SUBHEADERCOLOR = "#7a7a7a"
FOREGROUNDCOLOR = "#303030"
BUTTONCOLOR = "#f7f7f7"
UIBACKGROUNDCOLOR = "#f0f0f0"
UIOUTLINECOLOR = "#797979"

# import _common submodule (required to initialise constants further)
from ._common import *

# canvas data
CANVASWIDTH = 700
CANVASHEIGHT = 600
CENTER = (snap(CANVASWIDTH / 2), snap(CANVASHEIGHT / 2))


INITIALMODELSIZE = snap(100)
INITIALMODEL = [(CENTER[0] - INITIALMODELSIZE, CENTER[1] - INITIALMODELSIZE),
                (CENTER[0] - INITIALMODELSIZE, CENTER[1] + INITIALMODELSIZE),
                (CENTER[0] + INITIALMODELSIZE, CENTER[1] + INITIALMODELSIZE),
                (CENTER[0] + INITIALMODELSIZE, CENTER[1] - INITIALMODELSIZE)]

# endregion
# ------------------------------------------------------------------------ #
#                          variables                                       #
# ------------------------------------------------------------------------ #
# region constants

# objects
_points = []
grid_lines = []
vertical_origin = None
horizontal_origin = None
model = None
hull = None
circle_hull = None
center_graphic = None
model_distance = 0
model_center = CENTER
index_moving = None

# user interface
snapped = True
showing_points = True
showing_collider = False

# model data
smoothed = False
fillcolor = ""
outlinecolor = "black"
outlinewidth = 3
model_data = INITIALMODEL

# endregion
# ------------------------------------------------------------------------ #
#                          initialise submodules                           #
# ------------------------------------------------------------------------ #
# region initialise submodules

from ._commits import *

from . import _ui as ui, __main__

from ._canvas import *

from ._input import *


# import smallestenclosingcircle module
# noinspection PyUnresolvedReferences
from _smallestenclosingcircle_ import smallestenclosingcircle as SmallestEnclosingCircle

# import cachedmath module
# noinspection PyUnresolvedReferences
from common.cachedmath import *


# endregion
# ------------------------------------------------------------------------ #
#                          notices                                         #
# ------------------------------------------------------------------------ #
# region notices

__notice__ = "Pygrr Polyart Version <" + __version__ + ">. Copyright " + __date__ + " IsaacTFM. https://isaactfm.com/pygrr"
__versioninfo__ = f"Minimum Python version: {'.'.join([str(item) for item in __minpyversion__])}, running: {'.'.join([str(item) for item in version_info])}"
__versioninfo__ = f"{int((len(__notice__) / 2) - int(len(__versioninfo__) / 2) - 1) * ' '}{__versioninfo__}"
print(f"{len(__notice__) * '='}\n{__notice__}\n{__versioninfo__}\n{len(__notice__) * '='}")
__dependencies__ = ["> " + key + " ~ " + __dependencies__[key] for key in __dependencies__]
print("Dependencies:\n" + "\n".join(__dependencies__) + "\n")

# endregion
# ------------------------------------------------------------------------ #
#                          final code                                      #
# ------------------------------------------------------------------------ #
# region final code

create_grid(GRIDSIZE, GRIDCOLOR)
create_model()
draw_points()
draw_origin()

bind_inputs()

ui.root.mainloop()

# endregion
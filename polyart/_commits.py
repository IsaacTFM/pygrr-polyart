"""
This file handles all user presses or inputs - such as buttons and entry widgets.
"""

# if this is the origin file (not imported)
if __name__ == "__main__":
    # print the documentation
    print(__doc__)
    # add sysmessages module location to path
    from sys import path

    path.append('..')
    # run sysmessages
    import common.sysmessages


# import parent package
import polyart

# ------------------------------------------------------------------------ #
#                          initialise code                                 #
# ------------------------------------------------------------------------ #
# region initialise code

# import convex hull code
# noinspection PyUnresolvedReferences
from common import convexhull as ConvexHull

# import json module to load and dump data
from json import loads as load, dumps as dump

# import tkinter tools
from tkinter import messagebox
from tkinter import filedialog
from tkinter.colorchooser import askcolor


# endregion
# ------------------------------------------------------------------------ #
#                          toggle commands                                 #
# ------------------------------------------------------------------------ #
# region toggle commands

def toggle_smooth():
    """
    Called when the user presses the "smooth" button.
    """
    # toggle the smoothed property
    polyart.smoothed = not polyart.smoothed
    if polyart.smoothed:
        # configure button
        polyart.ui.smooth_button.configure(text="Smooth (on)")
        # configure model
        polyart.ui.canvas.itemconfigure(polyart.model, smooth=True)
    else:
        # configure button
        polyart.ui.smooth_button.configure(text="Smooth (off)")
        # configure model
        polyart.ui.canvas.itemconfigure(polyart.model, smooth=False)


def toggle_snap():
    """
    Called when the user presses the "snap" button.
    """
    # toggle the snapped property
    polyart.snapped = not polyart.snapped
    if polyart.snapped:
        # configure button
        polyart.ui.snap_button.configure(text="Snap (on)")
        # configure grid lines
        for line in polyart.grid_lines:
            polyart.ui.canvas.itemconfigure(line, fill=polyart.GRIDCOLOR)
    else:
        # configure button
        polyart.ui.snap_button.configure(text="Snap (off)")
        # configure grid lines
        for line in polyart.grid_lines:
            polyart.ui.canvas.itemconfigure(line, fill="")


def toggle_points():
    """
    Called when the user presses the "points" button.
    """
    # toggle the showing_points property
    polyart.showing_points = not polyart.showing_points
    if polyart.showing_points:
        # configure button
        polyart.ui.point_button.configure(text="Points (on)")
        # configure point graphics
        for point in polyart._points:
            polyart.ui.canvas.itemconfigure(point, fill=polyart.BACKGROUNDCOLOR, outline=polyart.POINTCOLOR)
    else:
        # configure button
        polyart.ui.point_button.configure(text="Points (off)")
        # configure point graphics
        for point in polyart._points:
            polyart.ui.canvas.itemconfigure(point, fill="", outline="")


def toggle_collider():
    """
    Called when the user presses the "collider" button.
    """
    # toggle the showing_collider property
    polyart.showing_collider = not polyart.showing_collider
    if polyart.showing_collider:
        # configure the button
        polyart.ui.collider_button.configure(text="Collider (on)")
        # configure the center graphic
        polyart.ui.canvas.tag_raise(polyart.center_graphic)
        polyart.ui.canvas.itemconfigure(polyart.center_graphic, fill=polyart.COLLIDERCOLOR)
        # configure the hull
        polyart.ui.canvas.itemconfigure(polyart.hull, outline=polyart.COLLIDERCOLOR)
        # configure the circular hull
        polyart.ui.canvas.itemconfigure(polyart.circle_hull, outline=polyart.COLLIDERCOLOR)
    else:
        # configure the button
        polyart.ui.collider_button.configure(text="Collider (off)")
        # configure the center graphic
        polyart.ui.canvas.itemconfigure(polyart.center_graphic, fill="")
        # configure the hull
        polyart.ui.canvas.itemconfigure(polyart.hull, outline="")
        # configure the circular hull
        polyart.ui.canvas.itemconfigure(polyart.circle_hull, outline="")


# endregion
# ------------------------------------------------------------------------ #
#                          file commands                                   #
# ------------------------------------------------------------------------ #
# region file commands

def clear():
    """
    Called when the user presses the "clear" button.
    """
    # ask the user if they want to clear their model
    if messagebox.askokcancel("PolyArt", "Are you sure you want to clear?\nAll unsaved data will be lost."):
        # make the model not smoothed
        if polyart.smoothed:
            toggle_smooth()

        # reset the fill color
        _fill = ""
        polyart.ui.fillcolor_entry.delete(0, "end")
        polyart.ui.fillcolor_entry.insert("end", _fill)
        set_fillcolor(None)

        # reset the outline color
        _outline = "black"
        polyart.ui.outlinecolor_entry.delete(0, "end")
        polyart.ui.outlinecolor_entry.insert("end", _outline)
        set_outlinecolor(None)

        # reset the outline widths
        _width = 3
        polyart.ui.outlinewidth_entry.delete(0, "end")
        polyart.ui.outlinewidth_entry.insert("end", _width)
        set_outlinewidth(None)

        # reset the model data
        polyart.model_data = [(polyart.CENTER[0] - polyart.INITIALMODELSIZE, polyart.CENTER[1] - polyart.INITIALMODELSIZE),
                              (polyart.CENTER[0] - polyart.INITIALMODELSIZE, polyart.CENTER[1] + polyart.INITIALMODELSIZE),
                              (polyart.CENTER[0] + polyart.INITIALMODELSIZE, polyart.CENTER[1] + polyart.INITIALMODELSIZE),
                              (polyart.CENTER[0] + polyart.INITIALMODELSIZE, polyart.CENTER[1] - polyart.INITIALMODELSIZE)]

        # refresh the canvas
        polyart.refresh()


def save():
    """
    Called when the user presses the "save" button.
    """

    # open the saveasfilename window
    files = [('Pygrr model File', '*.pygrrmodel'), ('All Files', '*.*')]
    filename = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)

    # if user did NOT cancel
    if filename != "":
        try:
            # store the points of the model
            _polydata = []
            for point in polyart.model_data:
                # make point orient from the center
                x = -(polyart.CENTER[0] - point[0])
                y = -(point[1] - polyart.CENTER[1])
                # divide size by scale
                x /= polyart.SCALE
                y /= polyart.SCALE
                # add to array
                _polydata.append((round(x, 3), round(y, 3)))

            # store the points of the hull
            _hulldata = []
            for point in ConvexHull.compute_hull(polyart.model_data):
                # make point orient from the center
                x = -(polyart.CENTER[0] - point[0])
                y = -(point[1] - polyart.CENTER[1])
                # divide size by scale
                x /= polyart.SCALE
                y /= polyart.SCALE
                # add to array
                _hulldata.append((round(x, 3), round(y, 3)))

            # make the model_center orient from the center
            x = -(polyart.CENTER[0] - polyart.model_center[0])
            y = -(polyart.model_center[1] - polyart.CENTER[1])
            # divide size by scale
            x /= polyart.SCALE
            y /= polyart.SCALE
            # create tuple
            _center = (round(x, 3), round(y, 3))

            # create the collider data
            collider_data = {
                    "type": "SIMPLE",
                    "center": _center,
                    "radius": polyart.model_distance,
                    "hull": _hulldata,
            }

            # combine all data
            data = {
                    "type": "POLYGON",
                    "smooth": polyart.smoothed,
                    "fill": polyart.fillcolor,
                    "outline": polyart.outlinecolor,
                    "width": polyart.outlinewidth,
                    "points": _polydata,
                    "collider": collider_data,
            }

            # dump the data to json
            json = dump(data, indent=4)

            # write to the file
            w = open(filename, "w+")
            w.write(json)
            w.close()

            # alert the user that it was saved successfully
            messagebox.showinfo("PolyArt", "File successfully saved.")
        except Exception:
            # handle errors
            messagebox.showerror("PolyArt", "Could not save file.")


def openfile():
    """
    Called when the user presses the "open" button.
    """

    # open the openfilename window
    files = [('Pygrr model File', '*.pygrrmodel'), ('All Files', '*.*')]
    filename = filedialog.askopenfilename(filetypes=files)

    # if user did NOT cancel
    if filename != "":

        # confirm that they want to open the file
        if messagebox.askyesno("PolyArt", "Are you sure you want to open this file? All unsaved changes will be lost."):
            try:
                # read the file
                r = open(filename, "r")
                # load the json data
                data = load(r.read())
                r.close()

                # set smooth property
                _smooth = data["smooth"]
                if _smooth != polyart.smoothed:
                    toggle_smooth()

                # set the fill color
                _fill = data["fill"]
                polyart.ui.fillcolor_entry.delete(0, "end")
                polyart.ui.fillcolor_entry.insert("end", _fill)
                set_fillcolor(None)

                # set the outline color
                _outline = data["outline"]
                polyart.ui.outlinecolor_entry.delete(0, "end")
                polyart.ui.outlinecolor_entry.insert("end", _outline)
                set_outlinecolor(None)

                # set the outline width
                _width = data["width"]
                polyart.ui.outlinewidth_entry.delete(0, "end")
                polyart.ui.outlinewidth_entry.insert("end", _width)
                set_outlinewidth(None)

                # read all of the points
                _points = data["points"]
                new_points = []
                for point in _points:
                    # multiply point by scale
                    x = point[0] * polyart.SCALE
                    y = point[1] * polyart.SCALE
                    # make point global not local
                    x = x + polyart.CENTER[0]
                    y = polyart.CENTER[1] - y
                    # add to array
                    new_points.append((x, y))

                # set the model data's points
                polyart.model_data = new_points

                # refresh the canvas
                polyart.refresh()
            except Exception:
                # handle errors
                messagebox.showerror("PolyArt", "Could not open file.")


# endregion
# ------------------------------------------------------------------------ #
#                          choosecolor commands                            #
# ------------------------------------------------------------------------ #
# region choosecolor commands


def open_fillcolor():
    """
    Called when the user opens the fillcolor choosecolor window.
    """

    # open the choosecolor window
    color = askcolor(polyart.fillcolor)[1]

    # if the user did NOT cancel
    if color != None:
        # set the fillcolor
        polyart.fillcolor = color

        # configure the model
        polyart.ui.canvas.itemconfigure(polyart.model, fill=polyart.fillcolor)

        # configure the entry
        polyart.ui.fillcolor_entry.delete(0, "end")
        polyart.ui.fillcolor_entry.insert("end", polyart.fillcolor)

    # reset focus on canvas
    polyart.ui.root.focus_set()


def open_outlinecolor():
    """
    Called when the user opens the outlinecolor choosecolor window.
    """

    # open the choosecolor window
    color = askcolor(polyart.outlinecolor)[1]

    # if the user did NOT cancel
    if color != None:
        # set the outlinecolor
        polyart.outlinecolor = color

        # configure the model
        polyart.ui.canvas.itemconfigure(polyart.model, outline=polyart.outlinecolor)

        # configure the entry
        polyart.ui.outlinecolor_entry.delete(0, "end")
        polyart.ui.outlinecolor_entry.insert("end", polyart.outlinecolor)

    # reset focus on canvas
    polyart.ui.root.focus_set()


# endregion
# ------------------------------------------------------------------------ #
#                          entry widget commands                           #
# ------------------------------------------------------------------------ #
# region entry widget commands

def set_fillcolor(event):
    """
    Called when the user hits <return/enter> inside the fillcolor entry.
    """

    # get data from the entry widget
    new_fillcolor = polyart.ui.fillcolor_entry.get()

    # if the color is valid
    try:
        # configure the model
        polyart.ui.canvas.itemconfigure(polyart.model, fill=new_fillcolor)

        # set the fillcolor
        polyart.fillcolor = new_fillcolor

    # if the color is invalid
    except Exception:
        # reset the entry widget
        polyart.ui.fillcolor_entry.delete(0, "end")
        polyart.ui.fillcolor_entry.insert("end", polyart.fillcolor)

        # show error
        messagebox.showerror("PolyArt", "'" + new_fillcolor + "' isn't a valid color!")

    # reset the focus on the canvas
    polyart.ui.root.focus_set()


def set_outlinecolor(event):
    """
    Called when the user hits <return/enter> inside the outlinecolor entry.
    """

    # get data from the entry widget
    new_outlinecolor = polyart.ui.outlinecolor_entry.get()

    # if the color is valid
    try:
        # configure the model
        polyart.ui.canvas.itemconfigure(polyart.model, outline=new_outlinecolor)

        # set the outlinecolor
        polyart.outlinecolor = new_outlinecolor

    # if the color is invalid
    except Exception:
        # reset the entry widget
        polyart.ui.outlinecolor_entry.delete(0, "end")
        polyart.ui.outlinecolor_entry.insert("end", polyart.outlinecolor)

        # show error
        messagebox.showerror("PolyArt", "'" + new_outlinecolor + "' isn't a valid color!")

    # reset the focus on the canvas
    polyart.ui.root.focus_set()


def set_outlinewidth(event):
    """
    Called when the user hits <return/enter> inside the outlinewidth entry.
    """

    # get data from the entry widget
    new_outlinewidth = polyart.ui.outlinewidth_entry.get()

    # if the number is valid
    try:
        # configure the model
        polyart.ui.canvas.itemconfigure(polyart.model, width=new_outlinewidth)

        # set the outlinewidth
        polyart.outlinewidth = new_outlinewidth

    # if the number is invalid
    except Exception:
        # reset the entry widget
        polyart.ui.outlinewidth_entry.delete(0, "end")
        polyart.ui.outlinewidth_entry.insert("end", polyart.outlinewidth)

        # show error
        messagebox.showerror("PolyArt", "'" + new_outlinewidth + "' isn't a valid number!")

    # reset the focus on the canvas
    polyart.ui.root.focus_set()

# endregion

"""
This file handles the GUI of PolyArt.
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

# import tkinter
from tkinter import *

# ------------------------------------------------------------------------ #
#                          initialise root                                 #
# ------------------------------------------------------------------------ #
# region initialise root


# create root
root = Tk()
root.title("Pygrr PolyArt")

# set root size
root.resizable(False, False)
size = str(polyart.CANVASWIDTH + 200) + "x" + str(polyart.CANVASHEIGHT)
root.geometry(size)

# register icon files
from os import path as ospath
colormixer = PhotoImage(file=ospath.dirname(__file__) + "/colormixer.png")
icon = PhotoImage(file=ospath.dirname(__file__) + "/pygrr_icon.png")

root.iconphoto(True, icon)

# set the default background color
root.tk_setPalette(background=polyart.UIBACKGROUNDCOLOR)


# endregion
# ------------------------------------------------------------------------ #
#                          left sidebar                                    #
# ------------------------------------------------------------------------ #
# region left sidebar


# setup sidebar frame
left_frame = Frame(root, padx=10)
left_frame.pack(side="left")

# create text widget
model_settings = Label(left_frame, text="Model data:", fg=polyart.HEADERCOLOR, height=0).pack(side="top", pady=5)

# create smooth button frame (frames must be created for each button or entry widget to apply the outline color properly)
smooth_frame = Frame(left_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
smooth_frame.pack(side="top", pady=5)
# create smooth button
smooth_button = Button(smooth_frame,
                       text="Smooth (off)",
                       command=polyart.toggle_smooth,
                       bd=0,
                       width=10,
                       fg=polyart.FOREGROUNDCOLOR,
                       activeforeground=polyart.FOREGROUNDCOLOR,
                       bg=polyart.BUTTONCOLOR,
                       activebackground=polyart.BUTTONCOLOR)
smooth_button.pack()

# create entry label
fillcolor_text = Label(left_frame, text="Fill color:", height=0, fg=polyart.SUBHEADERCOLOR).pack()
# create fillcolor entry frame
fillcolor_frame = Frame(left_frame, bd=0, highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
fillcolor_frame.pack(side="top", pady=0)
# create fillcolor entry
fillcolor_entry = Entry(fillcolor_frame, width=8, exportselection=0, bg=polyart.BUTTONCOLOR)
fillcolor_entry.bind('<Return>', polyart.set_fillcolor)
fillcolor_entry.pack(side="left")
fillcolor_entry.insert(END, polyart.fillcolor)
# create fillcolor window button
fillcolor_mixer = Button(fillcolor_frame,
                         command=polyart.open_fillcolor,
                         bd=0,
                         image=colormixer,
                         width=18,
                         height=18,
                         bg=polyart.UIOUTLINECOLOR,
                         activebackground=polyart.UIOUTLINECOLOR)
fillcolor_mixer.pack()

# create entry label
outlinecolor_text = Label(left_frame, text="Outline color:", height=0, fg=polyart.SUBHEADERCOLOR).pack()
# create outlinecolor entry frame
outlinecolor_frame = Frame(left_frame, bd=0, highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
outlinecolor_frame.pack(side="top", pady=0)
# create outlinecolor entry
outlinecolor_entry = Entry(outlinecolor_frame, width=8, exportselection=0, bg=polyart.BUTTONCOLOR)
outlinecolor_entry.bind('<Return>', polyart.set_outlinecolor)
outlinecolor_entry.pack(side="left")
outlinecolor_entry.insert(END, polyart.outlinecolor)
# create outlinecolor window button
outlinecolor_mixer = Button(outlinecolor_frame,
                            command=polyart.open_outlinecolor,
                            bd=0,
                            image=colormixer,
                            width=18,
                            height=18,
                            bg=polyart.UIOUTLINECOLOR,
                            activebackground=polyart.UIOUTLINECOLOR)
outlinecolor_mixer.pack()

# create entry label
outlinewidth_text = Label(left_frame, text="Outline width:", height=0, fg=polyart.SUBHEADERCOLOR).pack()
# create outlinewidth entry frame
outlinewidth_frame = Frame(left_frame, bd=0, highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
outlinewidth_frame.pack(side="top", pady=0)
# create outlinewidth entry
outlinewidth_entry = Entry(outlinewidth_frame, width=12, exportselection=0, bg=polyart.BUTTONCOLOR)
outlinewidth_entry.bind('<Return>', polyart.set_outlinewidth)
outlinewidth_entry.pack()
outlinewidth_entry.insert(END, polyart.outlinewidth)

# create gap in sidebar
gap = Label(left_frame, height=5).pack(side="top")

# create text widget
editor_settings = Label(left_frame, text="Editor data:", fg=polyart.HEADERCOLOR, height=0).pack(side="top", pady=5)

# create snap button frame
snap_frame = Frame(left_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
snap_frame.pack(side="top", pady=5)
# create snap button
snap_button = Button(snap_frame,
                     text="Snap (on)",
                     command=polyart.toggle_snap,
                     bd=0,
                     width=10,
                     fg=polyart.FOREGROUNDCOLOR,
                     activeforeground=polyart.FOREGROUNDCOLOR,
                     bg=polyart.BUTTONCOLOR,
                     activebackground=polyart.BUTTONCOLOR)
snap_button.pack()

# create point button frame
point_frame = Frame(left_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
point_frame.pack(side="top", pady=5)
# create point button
point_button = Button(point_frame,
                      text="Points (on)",
                      command=polyart.toggle_points,
                      bd=0,
                      width=10,
                      fg=polyart.FOREGROUNDCOLOR,
                      activeforeground=polyart.FOREGROUNDCOLOR,
                      bg=polyart.BUTTONCOLOR,
                      activebackground=polyart.BUTTONCOLOR)
point_button.pack()

# create collider button frame
collider_frame = Frame(left_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
collider_frame.pack(side="top", pady=5)
# create collider button
collider_button = Button(collider_frame,
                         text="Collider (off)",
                         command=polyart.toggle_collider,
                         bd=0,
                         width=10,
                         fg=polyart.FOREGROUNDCOLOR,
                         activeforeground=polyart.FOREGROUNDCOLOR,
                         bg=polyart.BUTTONCOLOR,
                         activebackground=polyart.BUTTONCOLOR)
collider_button.pack()

# create gap in sidebar to push everything up
gap_1 = Label(left_frame, height=50).pack(side="top")


# endregion
# ------------------------------------------------------------------------ #
#                          right sidebar                                    #
# ------------------------------------------------------------------------ #
# region right sidebar


# setup sidebar frame
right_frame = Frame(root, padx=10)
right_frame.pack(side="right")

# create clear button frame
clear_frame = Frame(right_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
clear_frame.pack(side="top", pady=10)
# create clear button
clear_button = Button(clear_frame,
                      text="Clear",
                      command=polyart.clear,
                      bd=0,
                      width=10,
                      fg=polyart.FOREGROUNDCOLOR,
                      activeforeground=polyart.FOREGROUNDCOLOR,
                      bg="white",
                      activebackground="white")
clear_button.pack()

# create save button frame
save_frame = Frame(right_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
save_frame.pack(side="top", pady=0)
# create save button
save_button = Button(save_frame,
                     text="Save",
                     command=polyart.save,
                     bd=0,
                     width=10,
                     fg=polyart.FOREGROUNDCOLOR,
                     activeforeground=polyart.FOREGROUNDCOLOR,
                     bg="white",
                     activebackground="white")
save_button.pack()

# create open button frame
open_frame = Frame(right_frame, bd=0, cursor="tcross", highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
open_frame.pack(side="top", pady=10)
# create open button
open_button = Button(open_frame,
                     text="Open",
                     command=polyart.openfile,
                     bd=0,
                     width=10,
                     fg=polyart.FOREGROUNDCOLOR,
                     activeforeground=polyart.FOREGROUNDCOLOR,
                     bg="white",
                     activebackground="white")
open_button.pack()

# create gap in sidebar to push everything up
gap_2 = Label(right_frame, height=50).pack(side="top")


# endregion
# ------------------------------------------------------------------------ #
#                          initialise canvas                               #
# ------------------------------------------------------------------------ #
# region initialise canvas

# create canvas frame
canvas_frame = Frame(root, highlightthickness=0.5, highlightbackground=polyart.UIOUTLINECOLOR)
canvas_frame.pack(side="left")
# create canvas
canvas = Canvas(canvas_frame, width=polyart.CANVASWIDTH, height=polyart.CANVASHEIGHT, background=polyart.BACKGROUNDCOLOR)
canvas.pack()

# endregion

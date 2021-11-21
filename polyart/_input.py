"""
This file handles the input of PolyArt.
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

# import used functions from math
from math import cos, atan, sin, radians


# ------------------------------------------------------------------------ #
#                          rotation                                        #
# ------------------------------------------------------------------------ #
# region rotation


def rotate_left(event):
    """
    Wrapper for rotating the model anti-clockwise.
    """

    # if the focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if polyart.snapped:
        # if snapped, rotate 22.5 degrees
        rotate(-22.5)
    else:
        # else, rotate 1 degrees
        rotate(-1)


def rotate_right(event):
    """
    Wrapper for rotating the model clockwise.
    """

    # if the focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if polyart.snapped:
        # if snapped, rotate 22.5 degrees
        rotate(22.5)
    else:
        # else, rotate 1 degrees
        rotate(1)


def rotate(angle):  # assumes anti-clockwise
    """
    Rotates the model.
    """

    angle *= -1  # makes it clockwise

    if angle < 0:  # this cleanses the number to ensure it is between 0 and 360
        angle = -(abs(angle) % 360)
    else:
        angle = angle % 360

    new_points = []
    for point in polyart.model_data:
        x = point[0] - polyart.CENTER[0]
        y = -(point[1] - polyart.CENTER[1])

        # point_rotation = the angle from the center of the model to the point
        if x == 0 and y == 0:  # ignore this point, it is in the centre
            new_points.append((polyart.CENTER[0] + x, polyart.CENTER[1] - y))
        else:
            if x == 0:
                if y > 0:  # it is directly up
                    point_rotation = radians(0 - 90)
                else:  # it is directly down
                    point_rotation = radians(180 - 90)
            elif y == 0:
                if x > 0:  # it is directly right
                    point_rotation = radians(90 - 90)
                else:  # it is directly left
                    point_rotation = radians(270 - 90)

            else:
                if x > 0 and y > 0:
                    point_rotation = atan(x / y) + radians(0 - 90)
                elif x > 0 and y < 0:
                    point_rotation = atan(x / y) + radians(180 - 90)
                elif x < 0 and y > 0:
                    point_rotation = atan(x / y) + radians(360 - 90)
                else:  # x < 0 and y < 0:
                    point_rotation = atan(x / y) + radians(180 - 90)

            theta = radians(
                    angle) - point_rotation  # theta is equal to the rotation of the object added to the angle, minus the model rotation of the point

            radius = polyart.cached_hypot(x, y)  # get distance from the point to the center of the object

            new_xdiff = radius * cos(theta)
            new_ydiff = radius * sin(theta)

            new_points.append((polyart.CENTER[0] + new_xdiff, polyart.CENTER[1] - new_ydiff))

    # update model_data
    polyart.model_data = new_points
    # refresh the canvas
    polyart.refresh()


# endregion
# ------------------------------------------------------------------------ #
#                          mouse                                           #
# ------------------------------------------------------------------------ #
# region mouse


def left_click(event):
    """
    Either creates a new point, or chooses the point to move (index_moving).
    """

    # if the focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    # get mouse position
    mouse = (event.x, event.y)

    # iterate through model_data
    for i in range(len(polyart.model_data)):
        point = polyart.model_data[i]
        # calculate the distance between the mouse and point
        distance = polyart.distance(mouse, point)

        if distance <= polyart.POINTSELECTDISTANCE:
            # if the distance is less than or equal to the point_select_distance
            polyart.index_moving = i
            break

    if polyart.index_moving == None:
        # if no point is selected, assume that the user is trying to create a new point

        # iterate through model_data
        for i in range(len(polyart.model_data)):

            # get the parent points of the line
            a = polyart.model_data[i % len(polyart.model_data)]
            c = polyart.model_data[(i + 1) % len(polyart.model_data)]

            if polyart.is_between(a, mouse, c):
                # if the mouse position lies on that line

                # work out index
                index = (i + 1) % len(polyart.model_data)

                if polyart.snapped:
                    # position is snapped
                    position = (polyart.snap(mouse[0]), polyart.snap(mouse[1]))
                else:
                    # position not snapped
                    position = mouse

                # insert new point
                polyart.model_data.insert(index, position)
                # refresh the canvas
                polyart.refresh()

                # force only one point to be made
                break


def left_release(event):
    """
    Sets the selected point (index_moving) to None.
    """

    # if the focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    polyart.index_moving = None


def right_click(event):
    """
    Deletes the point hovered over.
    """

    # if the focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if len(polyart.model_data) > 3 and polyart.index_moving == None:
        # if there are less than 4 points, deleting a point should NOT be allowed to happen
        # if a point is selected, the same goes

        # get the mouse position
        mouse = (event.x, event.y)

        # iterate through model_data
        for point in polyart.model_data:
            if polyart.distance(mouse, point) <= polyart.POINTSELECTDISTANCE:
                # if the distance is less than or equal to the point_select_distance

                # remove the point
                polyart.model_data.remove(point)

                # force only one point to be deleted
                break

        # refresh the canvas
        polyart.refresh()


def motion(event):
    """
    Moves the selected point, if there is one.
    """

    # get the moue position
    mouse = (event.x, event.y)

    if polyart.index_moving is not None:
        # if a point is selected

        if polyart.snapped:
            # if snapped, snap the position
            new_position = (polyart.snap(mouse[0]), polyart.snap(mouse[1]))
        else:
            # if not, do not snap the position
            new_position = mouse

        # update variable model_data
        polyart.model_data[polyart.index_moving] = new_position
        # refresh the canvas
        polyart.refresh()


# endregion
# ------------------------------------------------------------------------ #
#                          movement                                        #
# ------------------------------------------------------------------------ #
# region movement


def left(event):
    """
    Moves the model left.
    """

    # if focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if polyart.snapped:
        # if snapped, move vector is effectively snapped
        move = (-polyart.GRIDSIZE, 0)
    else:
        move = (-1, 0)

    # iterate through model data
    for i in range(len(polyart.model_data)):
        x = polyart.model_data[i][0]
        y = polyart.model_data[i][1]

        # offset each point by the move vector
        polyart.model_data[i] = (x + move[0], y - move[1])

    # refresh the canvas
    polyart.refresh()


def right(event):
    """
    Moves the model right.
    """

    # if focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if polyart.snapped:
        # if snapped, move vector is effectively snapped
        move = (polyart.GRIDSIZE, 0)
    else:
        move = (1, 0)

    # iterate through model data
    for i in range(len(polyart.model_data)):
        x = polyart.model_data[i][0]
        y = polyart.model_data[i][1]

        # offset each point by the move vector
        polyart.model_data[i] = (x + move[0], y - move[1])

    # refresh the canvas
    polyart.refresh()


def up(event):
    """
    Moves the model up.
    """

    # if focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if polyart.snapped:
        # if snapped, move vector is effectively snapped
        move = (0, polyart.GRIDSIZE)
    else:
        move = (0, 1)

    # iterate through model data
    for i in range(len(polyart.model_data)):
        x = polyart.model_data[i][0]
        y = polyart.model_data[i][1]

        # offset each point by the move vector
        polyart.model_data[i] = (x + move[0], y - move[1])

    # refresh the canvas
    polyart.refresh()


def down(event):
    """
    Moves the model down.
    """

    # if focus is on an entry widget, return
    try:
        if polyart.ui.root.focus_get().winfo_class() == "Entry":
            return
    except Exception:
        pass

    if polyart.snapped:
        # if snapped, move vector is effectively snapped
        move = (0, -polyart.GRIDSIZE)
    else:
        move = (0, -1)

    # iterate through model data
    for i in range(len(polyart.model_data)):
        x = polyart.model_data[i][0]
        y = polyart.model_data[i][1]

        # offset each point by the move vector
        polyart.model_data[i] = (x + move[0], y - move[1])

    # refresh the canvas
    polyart.refresh()


# endregion
# ------------------------------------------------------------------------ #
#                          binding                                         #
# ------------------------------------------------------------------------ #
# region binding


def bind_inputs():
    """
    Binds the inputs to each function in this file.
    """

    # bind the mouse movement on the canvas to the motion function
    polyart.ui.canvas.bind("<Motion>", motion)

    # bind the mouse presses on the root to the correct functions
    polyart.ui.root.bind("<ButtonPress-1>", left_click)
    polyart.ui.root.bind("<ButtonRelease-1>", left_release)
    polyart.ui.root.bind("<ButtonPress-3>", right_click)

    # bind the rotate functions to E and Q
    polyart.ui.root.bind("e", rotate_right)
    polyart.ui.root.bind("q", rotate_left)

    # bind the arrow keys to the movement functions
    polyart.ui.root.bind("<Key-Left>", left)
    polyart.ui.root.bind("<Key-Right>", right)
    polyart.ui.root.bind("<Key-Up>", up)
    polyart.ui.root.bind("<Key-Down>", down)

    # bind the WSAD keys to the movement functions
    polyart.ui.root.bind("<a>", left)
    polyart.ui.root.bind("<d>", right)
    polyart.ui.root.bind("<w>", up)
    polyart.ui.root.bind("<s>", down)


# endregion

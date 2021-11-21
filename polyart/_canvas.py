"""
This file handles the canvas.
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
#                          refresh functions                               #
# ------------------------------------------------------------------------ #
# region refresh functions


def refresh():
    """
    The driver function for refreshing the canvas
    """

    # refresh the model
    refresh_model()
    # refresh the hull and collider
    refresh_hull()
    # draw the points
    draw_points()
    # draw the origin
    draw_origin()
    # raise the center_graphic so it is on top
    polyart.ui.canvas.tag_raise(polyart.center_graphic)


def refresh_model():
    """
    Refreshes the model.
    """

    # create new array for the points
    # this is necessary as the .coords method will only take a flat list
    new_points = []
    for point in polyart.model_data:
        new_points.append(point[0])
        new_points.append(point[1])

    # configure model
    polyart.ui.canvas.coords(polyart.model, new_points)


def refresh_hull():
    """
    Refreshes the collider.
    """

    # compute the hull's points
    _hull = polyart.ConvexHull.compute_hull(polyart.model_data)
    # create new array for the points
    # this is necessary as the .coords method will only take a flat list
    hull_points = []
    for point in _hull:
        hull_points.append(point[0])
        hull_points.append(point[1])

    # configure hull
    polyart.ui.canvas.coords(polyart.hull, hull_points)

    # compute the smallest enclosing circle
    enclosing_circle = polyart.SmallestEnclosingCircle.make_circle(_hull)
    # set the model distance and center
    polyart.model_distance = enclosing_circle[2]
    polyart.model_center = (enclosing_circle[0], enclosing_circle[1])

    # calculate the circle hull's bounds
    a = (polyart.model_center[0] - polyart.model_distance, polyart.model_center[1] - polyart.model_distance)
    b = (polyart.model_center[0] + polyart.model_distance, polyart.model_center[1] + polyart.model_distance)
    # configure the circle hull
    polyart.ui.canvas.coords(polyart.circle_hull, a[0], a[1], b[0], b[1])

    # calculate the center graphic's bounds
    a = (polyart.model_center[0] - polyart.CENTERHULLGRAPHICSIZE, polyart.model_center[1] - polyart.CENTERHULLGRAPHICSIZE)
    b = (polyart.model_center[0] + polyart.CENTERHULLGRAPHICSIZE, polyart.model_center[1] + polyart.CENTERHULLGRAPHICSIZE)
    # configure the center graphic
    polyart.ui.canvas.coords(polyart.center_graphic, a[0], a[1], b[0], b[1])


def draw_points():
    """
    Refreshes the point graphics on the model.
    """

    # delete the old point graphics
    for old in polyart._points:
        polyart.ui.canvas.delete(old)
    # empty array
    polyart._points = []

    if polyart.showing_points:
        # if points should be visible
        fillcolor = polyart.BACKGROUNDCOLOR
        outlinecolor = polyart.POINTCOLOR
    else:
        # if points should be invisible
        fillcolor = ""
        outlinecolor = ""

    # create the new points
    for point in polyart.model_data:
        new = polyart.ui.canvas.create_oval(point[0] - polyart.POINTSIZE,
                                            point[1] - polyart.POINTSIZE,
                                            point[0] + polyart.POINTSIZE,
                                            point[1] + polyart.POINTSIZE,
                                            fill=fillcolor,
                                            outline=outlinecolor,
                                            width=3)
        # add to array
        polyart._points.append(new)


def draw_origin():
    """
    Refreshes the origin.
    """

    # delete the old origin objects
    polyart.ui.canvas.delete(polyart.vertical_origin)
    polyart.ui.canvas.delete(polyart.horizontal_origin)

    # create the vertical origin
    polyart.vertical_origin = polyart.ui.canvas.create_line(polyart.CENTER[0],
                                                            polyart.CENTER[1] + polyart.ORIGINSIZE,
                                                            polyart.CENTER[0],
                                                            polyart.CENTER[1] - polyart.ORIGINSIZE - 8,
                                                            width=2,
                                                            fill=polyart.ORIGINCOLOR,
                                                            arrow="last")

    # create the horizontal origin
    polyart.horizontal_origin = polyart.ui.canvas.create_line(polyart.CENTER[0] + polyart.ORIGINSIZE,
                                                              polyart.CENTER[1],
                                                              polyart.CENTER[0] - polyart.ORIGINSIZE,
                                                              polyart.CENTER[1],
                                                              width=2,
                                                              fill=polyart.ORIGINCOLOR)


# endregion
# ------------------------------------------------------------------------ #
#                          create functions                                #
# ------------------------------------------------------------------------ #
# region create functions

def create_grid(step, color):
    """
    Creates the grid line objects.
    """

    # create y axis lines
    for x in range(0, polyart.CANVASWIDTH, step):
        # create object
        line = polyart.ui.canvas.create_line(x, 0, x, polyart.CANVASHEIGHT, fill=color)
        # add to array
        polyart.grid_lines.append(line)

    # create x axis lines
    for y in range(0, polyart.CANVASHEIGHT, step):
        # create object
        line = polyart.ui.canvas.create_line(0, y, polyart.CANVASWIDTH, y, fill=color)
        # add to array
        polyart.grid_lines.append(line)


def create_model():
    """
    Creates the model and hull objects.
    """

    # create the model object
    polyart.model = polyart.ui.canvas.create_polygon(polyart.model_data, fill=polyart.fillcolor, outline=polyart.outlinecolor, width=polyart.outlinewidth)
    # create the hull object
    polyart.hull = polyart.ui.canvas.create_polygon(polyart.ConvexHull.compute_hull(polyart.model_data), fill="", outline="", width=1.5)
    # create the circle hull
    polyart.circle_hull = polyart.ui.canvas.create_oval(0, 0, 1, 1, fill="", outline="")
    # create the center graphic
    polyart.center_graphic = polyart.ui.canvas.create_oval(0, 0, 1, 1, fill="", outline="")
    # force a refresh
    refresh()

# endregion

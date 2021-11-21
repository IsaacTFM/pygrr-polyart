"""
This file defines functions used within polyart.
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


def dot(a, b):
    """
    Returns the dot-product of vectors a and b.

    :param a: Vector A
    :param b: Vector B
    """
    return (a[0] * b[0]) + (a[1] * b[1])


def cross(a, b):
    """
    Returns the cross-product of vectors a and b.

    :param a: Vector A
    :param b: Vector B
    """
    return (a[0] * b[1]) - (a[1] * b[0])


def is_between(a, b, c):
    """
    Returns if point B is in-between points A and C.

    :param a: Point A of line
    :param b: Point in question
    :param c: Point B of line
    """

    # if snap is on, snap the points
    if polyart.snapped:
        a = (snap(a[0]), snap(a[1]))
        b = (snap(b[0]), snap(b[1]))
        c = (snap(c[0]), snap(c[1]))

    v = (a[0] - b[0], a[1] - b[1])
    w = (b[0] - c[0], b[1] - c[1])

    return abs(cross(v, w)) <= 2500 and dot(v, w) > 0


def snap(number):
    """
    Returns the number snapped (or rounded to) the grid size.

    :param number: The number to snap
    """
    return int(round(number / polyart.GRIDSIZE) * polyart.GRIDSIZE)


def distance(a, b):
    """
    Calculates the distance between points a and b.

    :param a: Point A
    :param b: Point B
    """

    # calculate difference
    x = abs(a[0] - b[0])
    y = abs(a[1] - b[1])

    # use pythagoras' theorum to calculate hypotenuse
    hypot = polyart.cached_hypot(x, y)

    return hypot

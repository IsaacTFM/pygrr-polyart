"""
This module calculates the convex hull of a set of points, using Jarvis March.
"""


# create a point class that can be accessed with point.x and point.y as well as indexes
from collections import namedtuple

# import type annotations
from typing import List

Point = namedtuple("Point", "x y")


def is_clockwise(origin: Point, point_1: Point, point_2: Point) -> bool:
    """
    Returns true if point_1 is clockwise from point_2 based on the origin.

    :param origin: The base point
    :param point_1: Point in question
    :param point_2: Point from
    """

    # convert the points to a vector from the origin
    x = point_1[0] - origin[0]
    y = point_1[1] - origin[1]
    point_1 = (x, y)

    x = point_2[0] - origin[0]
    y = point_2[1] - origin[1]
    point_2 = (x, y)

    # calculate the cross-product of the two vectors
    a = (point_2[0] * point_1[1])
    b = (point_1[0] * point_2[1])
    k = a - b

    # if k is negative, it is clockwise
    return k <= 0


def compute_hull(points: List[tuple]) -> List[Point]:
    """
    Returns the convex hull of the set of points.

    :param points: The set of points in question
    """

    # convert every tuple in the set to be a Point object, for easier access
    points: List[Point] = [Point(current_point[0], current_point[1]) for current_point in points]

    # find leftmost point
    leftmost = points[0]
    for point in points:
        if point.x < leftmost.x:
            leftmost = point

    # create the list that will store the hull's points
    hull = [leftmost]

    point_on = leftmost
    for i in range(len(points)):
        # find the initial max
        for point in points:
            if point != point_on:
                point_1 = point
                break
        far_point = point_1

        for point_2 in points:
            # ensure not comparing to self or point_1
            if point_2 == point_on or point_2 == point_1:
                pass
            else:
                if not is_clockwise(point_on, far_point, point_2):
                    # if point is anti-clockwise
                    far_point = point_2

        hull.append(far_point)
        point_on = far_point

    # hull is structured with the first point being repeated at the end, like a loop;
    # this is unwanted behaviour, so we splice it at the second last point
    return hull[:-1]

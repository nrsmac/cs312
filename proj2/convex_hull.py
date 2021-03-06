from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
def sort_points(points):
    points.sort(key=lambda p: p.x())
    return points


def slope(p1, p2):
    return (p2.y() - p1.y()) / (p2.x() - p1.x())


class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        # TODO: SORT THE POINTS BY INCREASING X-VALUE
        sorted_points = sort_points(points)
        t2 = time.time()

        t3 = time.time()
        # this is a dummy polygon of the first 3 unsorted points
        # polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
        lines = self.convex_hull(points)
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        t4 = time.time()
        # self.showHull(lines, RED)
        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(lines, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    def convex_hull(self, points):
        hull_points = self.help_a_hull_out(points)
        lines = []
        for i in range(len(hull_points) - 1):
            line = QLineF(hull_points[i], hull_points[i + 1])
            lines.append(line)
        lines.append(QLineF(hull_points[-1], hull_points[0]))

        return lines

    def help_a_hull_out(self, points):
        # Base case: 2 points
        if len(points) <= 2:
            return sorted(points, key=lambda x:x.x())

        # Divide points into L and R
        l_points, r_points = points[0:len(points) // 2], points[len(points) // 2:]
        l_hull = self.help_a_hull_out(l_points)
        r_hull = self.help_a_hull_out(r_points)

        return self.merge(l_hull, r_hull)

    def merge(self, l_hull: [], r_hull: []):  # Accepts two hulls as lists of points
        upper_tangent_left, upper_tangent_right = self.upper_tangent(l_hull, r_hull)
        lower_tangent_left, lower_tangent_right = self.lower_tangent(l_hull, r_hull)

        return self.one_with_everything(l_hull, r_hull, upper_tangent_left, upper_tangent_right, lower_tangent_left,
                                        lower_tangent_right)

    def one_with_everything(self, l_hull, r_hull, upper_tangent_left, upper_tangent_right, lower_tangent_left,
                            lower_tangent_right):
        the_whole_hull_nothing_but_the_hull = []

        # The left upper half
        ant_place = 0
        while l_hull[ant_place] != upper_tangent_left:
            the_whole_hull_nothing_but_the_hull.append(l_hull[ant_place])
            ant_place += 1
        the_whole_hull_nothing_but_the_hull.append(upper_tangent_left)

        # the right upper half!
        ant_place = r_hull.index(upper_tangent_right)
        while r_hull[ant_place] != lower_tangent_right:
            the_whole_hull_nothing_but_the_hull.append(r_hull[ant_place])
            ant_place = (ant_place + 1) % len(r_hull)
        the_whole_hull_nothing_but_the_hull.append(lower_tangent_right)

        # the left lower half
        ant_place = l_hull.index(lower_tangent_left)
        while ant_place != 0:
            if l_hull[ant_place] not in the_whole_hull_nothing_but_the_hull:
                the_whole_hull_nothing_but_the_hull.append(l_hull[ant_place])
            ant_place = (ant_place + 1) % len(l_hull)

        return the_whole_hull_nothing_but_the_hull

    def upper_tangent(self, l, r):
        p = max(l, key=lambda x: x.x())  # Rightmost point in l
        q = r[0]  # Leftmost point in r
        found = False
        current_slope = slope(p, q)

        while not found:
            found = True
            next_p = l[(l.index(p) - 1) % len(l)]
            while current_slope > slope(next_p, q):  # Go CCW around l
                p = next_p
                current_slope = slope(p, q)
                found = False

            next_q = r[(r.index(q) + 1) % len(r)]
            while current_slope < slope(p, next_q):
                q = next_q
                current_slope = slope(p, q)
                found = False

        return p, q

    def lower_tangent(self, l, r):
        p = max(l, key=lambda x: x.x())  # Rightmost point in l
        q = r[0]  # Leftmost point in r
        found = False
        current_slope = slope(p, q)

        while not found:
            found = True
            next_p = l[(l.index(p) + 1) % len(l)]
            while current_slope < slope(next_p, q):  # Go CCW around l
                p = next_p
                current_slope = slope(p, q)
                found = False

            next_q = r[(r.index(q) - 1) % len(r)]
            while current_slope > slope(p, next_q):
                q = next_q
                current_slope = slope(p, q)
                found = False

        return p, q

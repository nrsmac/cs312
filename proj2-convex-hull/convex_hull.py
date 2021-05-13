# this is 4-5 seconds slower on 1000000 points than Ryan's desktop...  Why?


from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal

import time


class ConvexHullSolverThread(QThread):
    def __init__(self, unsorted_points, demo):
        self.demo = demo
        self.points = unsorted_points
        self.pause = demo
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    # These two signals are used for interacting with the GUI.
    show_hull = pyqtSignal(list, tuple)
    display_text = pyqtSignal(str)

    # Some additional thread signals you can implement and use for debugging,
    # if you like
    show_tangent = pyqtSignal(list, tuple)
    erase_hull = pyqtSignal(list)
    erase_tangent = pyqtSignal(list)

    def set_points(self, unsorted_points, demo):
        self.points = unsorted_points

    def run(self):
        assert (type(self.points) == list and type(self.points[0]) == QPointF)

        n = len(self.points)
        print('Computing Hull for set of {} points'.format(n))

        t1 = time.time()
        # TODO: SORT THE POINTS BY INCREASING X-VALUE
        self.points = self.sort_points(self.points)

        assert (self.points[0].x() < self.points[1].x())
        assert (self.points[0].x() < self.points[-1].x())

        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2 - t1))

        t3 = time.time()
        # TODO: COMPUTE THE CONVEX HULL USING DIVIDE AND CONQUER
        t4 = time.time()

        USE_DUMMY = True
        if USE_DUMMY:
            # This is a dummy polygon of the first 3 unsorted points
            polygon = [QLineF(self.points[i], self.points[(i + 1) % 3]) for i in range(3)]

            # When passing lines to the display, pass a list of QLineF objects.
            # Each QLineF object can be created with two QPointF objects
            # corresponding to the endpoints
            assert (type(polygon) == list and type(polygon[0]) == QLineF)

            # Send a signal to the GUI thread with the hull and its color
            self.show_hull.emit(polygon, (0, 255, 0))

        else:
            # TODO: PASS THE CONVEX HULL LINES BACK TO THE GUI FOR DISPLAY
            pass

        # Send a signal to the GUI thread with the time used to compute the
        # hull
        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    def convex_hull(self, sorted_points):
        if len(sorted_points) <= 3:
            return sorted_points

        l = self.convex_hull(sorted_points[0:len(sorted_points // 2)])
        r = self.convex_hull(sorted_points[(len(sorted_points) // 2) + 1:])
        hull = self.merge(l, r)
        return hull

    def merge(self, l, r):
        upper_tangent = self.find_upper_tangent(l, r)
        lower_tangent = self.find_lower_tangent(l, r)

        pass

    def find_upper_tangent(self, l, r):
        pass

    def find_lower_tangent(self, l, r):
        pass

    def slope(self, p1, p2):
        pass

    def sort_points(self, points):
        #  TODO: Deal with empty lists returned from sort_helper()
        if points[-1].x() > points[0].x():
            first_half = points[0:len(points) // 2]
            second_half = points[len(points) // 2 + 1:]
            return self.sort_helper(self.sort_points(first_half), self.sort_points(second_half))
        else:
            return points

    def sort_helper(self, u, v):
        if u[0].x() < v[0].x():
            return u[0:1].append(self.sort_helper(u[1:], v))
        else:
            return v[0:1].append(self.sort_helper(u, v[1:]))
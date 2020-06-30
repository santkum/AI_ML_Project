"""
AI_Project
City.py

@author: Santosh Kumar Nunna (sn7916@rit.edu)
@author: Mouna Reddy Kallu (mk9014@rit.edu)
@author: Gautham Gadipudi (gg7148@rit.edu)

This class represents each city we create as a coordinate of x and y. This class also contains a distance function
which calculates the distance between two points and returns it.
"""
from math import sqrt


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, obj):
        """
        Function in the city class, which calculates the distance between two points or coordinates
        :param obj: input object
        :return: distance between the input object and self.x, self.y
        """
        x_diff = abs(self.x - obj.x)
        y_diff = abs(self.y - obj.y)

        return sqrt(x_diff**2 + y_diff**2)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

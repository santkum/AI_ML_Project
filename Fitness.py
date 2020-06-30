"""
AI_Project
Fitness.py

@author: Santosh Kumar Nunna (sn7916@rit.edu)
@author: Mouna Reddy Kallu (mk9014@rit.edu)
@author: Gautham Gadipudi (gg7148@rit.edu)

This class is associated with the fitness function which is used to select and validate the population created.
"""


class Fitness:
    def __init__(self, route):
        self.route = route
        self.dist = 0
        self.fitness = 0.0

    def distance_route(self):
        """
        This function calculates the distance covered over the selected route. This is nothing but the total distance
        travelled from the start point to the same point again which in between visits all the available cities in the
        list.
        :return: total distance travelled from start point and reaching back to the start point again.
        """
        if self.dist == 0:
            route_dist = 0
            for val in range(0, len(self.route)):
                start = self.route[val]
                if val + 1 < len(self.route):
                    destination = self.route[val + 1]
                else:
                    destination = self.route[0]
                route_dist += start.distance(destination)
            self.dist = route_dist
        return self.dist

    def fitness_evaluator(self):
        """
        The fitness evaluator calculates the fitness of the route selected or we can say the sample selected. If the
        fitness is 0, then we calculate it over the distance covered for the given route.
        :return: Fitness value calculated.
        """
        if self.fitness == 0:
            self.fitness = 1 / float(self.distance_route())
        return self.fitness

import numpy as np
from numpy import inf
import matplotlib.pyplot as plt

class Ants():
    def __init__(self):


        self.distance = np.array([[0, 10, 12, 11, 14]  # distance between the cities
                           ,      [10, 0, 13, 15, 8]
                           ,      [12, 13, 0, 9, 14]
                           ,      [11, 15, 9, 0, 16]
                           ,      [14, 8, 14, 16, 0]]
                                   )

        self.iteration = 1
        self.num_ants = 5
        self.num_cities = 5             # depended on the distance array!!!

        self.evaporation = .5           # evaporation rate of pheromone
        self.pheromone_factor = 1
        self.visibility_factor = 2

        self.visibility = 1 / self.distance             # calculating visibility between 2 cities
        self.visibility[self.visibility == inf] = 0

        self.pheromone = .1*np.ones((self.num_ants, self.num_cities)) # All paths have the same intensity at the start
        self.route = np.ones((self.num_ants, self.num_cities + 1))    # The add 1 is to come back

    # Drawing the ants paths in real time

    def draw(self):
        plt.axes().get_xaxis().set_visible(False)
        plt.axis([0, self.num_cities, 0, self.num_ants])
        plt.ylabel('Cities')
        plt.plot(self.route.transpose())
        plt.draw()
        plt.pause(2)
        plt.clf()

    # Ants algorithm
    def algo(self):
        for iteration in range(self.iteration):

            self.route[:, 0] = 1 # initial starting and ending position of every ant

            for i in range(self.num_ants):

                temp_visibility = np.array(self.visibility)  # creating a copy of visibility

                for j in range(self.num_cities - 1):

                    ant_cur_city = int(self.route[i, j] - 1)  # current city of the ant

                    temp_visibility[:, ant_cur_city] = 0  # making visibility of the current city as zero

                    p_feature = np.power(self.pheromone[ant_cur_city, :], self.visibility_factor)[:, np.newaxis]       # calculating pheromone feature
                    v_feature = np.power(temp_visibility[ant_cur_city, :], self.pheromone_factor)[:, np.newaxis]          # calculating visibility feature

                    pv_feature = np.multiply(p_feature, v_feature)  # calculating the combine of pheromone and visibility

                    pv_total = np.sum(pv_feature)  # sum of all the feature

                    cum_probability = np.cumsum(pv_feature / pv_total)                 # calculating cumulative sum
                    rant_num = np.random.random_sample()                     # random number in [0,1]

                    self.route[i, j + 1] = np.nonzero(cum_probability > rant_num)[0][0] + 1  # adding city to route
                    self.draw()

                final_city = list(set([i for i in range(1, self.num_cities + 1)]) - set(self.route[i, :-2]))[0]  # finding the last not visited city to route

                self.route[i, -2] = final_city  # adding last not visited city to route
            self.find_best_distances()

    def path(self):
        self.algo()
        self.displayResults()

    def find_best_distances(self):
        self.route_optimal = np.array(self.route)  # initializing optimal route
        self.dist_cost = np.zeros((self.num_ants, 1))

        for i in range(self.num_ants):
            d = 0
            for j in range(self.num_cities - 1):
                d = d + self.distance[
                    int(self.route_optimal[i, j]) - 1, int(self.route_optimal[i, j + 1]) - 1]  # calculating total tour distance

            self.dist_cost[i] = d  # storing distance of tour for 'i'th ant at location 'i'

        self.dist_min_loc = np.argmin(self.dist_cost)  # finding location of minimum of dist_cost
        self.dist_min_cost = self.dist_cost[self.dist_min_loc]  # finding min of dist_cost

        self.best_route = self.route[self.dist_min_loc, :]  # initializing current traversed as best route
        self.pheromone = (1 - self.evaporation) * self.pheromone  # evaporation of pheromone

        for i in range(self.num_ants):
            for j in range(self.num_cities - 1):
                dt = 1 / self.dist_cost[i]
                self.pheromone[int(self.route_optimal[i, j]) - 1, int(self.route_optimal[i, j + 1]) - 1] = self.pheromone[int(
                    self.route_optimal[i, j]) - 1, int(self.route_optimal[i, j + 1]) - 1] + dt
                # updating the pheromone with delta_distance
                # delta_distance will be more with min_dist i.e adding more weight to that route  pheromone

    # Displays all the paths of the ants, the best path and the cost of it
    def displayResults(self):
        best_path_cost = int(self.dist_min_cost[0]) + self.distance[int(self.best_route[-2]) - 1, 0]
        print('Route of all the ants at the end :')
        print(self.route_optimal)
        print()
        print('Best path :', self.best_route)
        print('Cost of the best path :', best_path_cost)

import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
import PySimpleGUI as psg
import time as time
import psutil

class Ants():
    def __init__(self):


        #self.distance = np.array([[0, 10, 12, 11, 14], # distance between 5 cities
        #                          [10, 0, 13, 15, 8],
        #                          [12, 13, 0, 9, 14],
        #                          [11, 15, 9, 0, 16],
        #                          [14, 8, 14, 16, 0]])

      # self.distance = np.array([[0, 25, 25, 64, 49, 121, 100, 144],  # distance between 8 cities
      #                          [25, 0, 16, 36, 49, 81, 81, 144,],
      #                          [25, 16, 0, 9, 9, 36, 25, 64,],
      #                          [64, 36, 9, 0, 16, 9, 16, 49,],
      #                          [49, 49, 9, 16, 0, 16, 9, 25,],
      #                          [121, 81, 36, 9, 16, 0, 4, 16,],
      #                          [100, 81, 25, 16, 9, 4, 0, 9,],
      #                          [144, 144, 64, 49, 25, 16, 9, 0]])


        self.distance = np.array([[0, 25, 25, 64, 49, 121, 100, 144, 100, 169],  # distance between 10 cities
                                  [25, 0, 16, 36, 49, 81, 81, 144, 64, 121],
                                  [25, 16, 0, 9, 9, 36, 25, 64, 25, 64],
                                  [64, 36, 9, 0, 16, 9, 16, 49, 4, 25],
                                  [49, 49, 9, 16, 0, 16, 9, 25, 25, 49],
                                  [121, 81, 36, 9, 16, 0, 4, 16, 4, 9],
                                  [100, 81, 25, 16, 9, 4, 0, 9, 16, 9],
                                  [144, 144, 64, 49, 25, 16, 9, 0, 36, 25],
                                  [100, 64, 25, 4, 25, 4, 16, 36, 0, 9],
                                  [169, 121, 64, 25, 49, 9, 9, 25, 9, 0]])

        self.iteration = 5
        self.num_ants = 10
        self.num_cities = 10             # depended on the distance array!!!

        self.evaporation = .5           # evaporation rate of pheromone
        self.pheromone_factor = 1
        self.visibility_factor = 2

        self.visibility = 1 / self.distance             # calculating visibility between 2 cities
        self.visibility[self.visibility == inf] = 0

        self.pheromone = .1*np.ones((self.num_ants, self.num_cities)) # All paths have the same intensity at the start
        self.route = np.ones((self.num_ants, self.num_cities + 1))    # The add 1 is to come back



    # Input window for the user
    def inputWindow(self):
        layout = [
            [psg.Text('Please enter your configuration')],
            [psg.Text('Iterations', size=(15, 1)), psg.InputText(self.iteration, key='iteration'), ],
            [psg.Text('Number of Ants', size=(15, 1)), psg.InputText(self.num_ants, key='num_ants')],
            [psg.Text('Number of Cities', size=(15, 1)), psg.InputText(self.num_cities, key='num_cities')],
            [psg.Text('Evaporation Rate', size=(15, 1)), psg.InputText(self.evaporation, key='evaporation')],
            [psg.Text('Pheromone Factor', size=(15, 1)), psg.InputText(self.pheromone_factor, key='pheromone_factor')],
            [psg.Text('Visibilitiy Factor', size=(15, 1)), psg.InputText(self.visibility_factor, key='visibility_factor')],
            [psg.Submit(), psg.Cancel()]
        ]

        iwindow = psg.Window('Ants variables entry window', layout)
        event, values = iwindow.read()
        if event == 'Submit':
            self.iteration = int(values['iteration'])
            self.num_ants = int(values['num_ants'])
            self.num_cities = int(values['num_cities'])
            self.evaporation = float(values['evaporation'])
            self.pheromone_factor = int(values['pheromone_factor'])
            self.visibility_factor = int(values['visibility_factor'])
            self.path()
            iwindow.close()
        elif event == 'Cancel':
            iwindow.close()


    # Drawing the ants paths in real time
    def draw(self):
        #plt.axes().get_xaxis().set_visible(False)
        plt.axis([0, self.num_ants, 0, self.num_cities])
        plt.title('Ant Colony', fontsize = 20)
        plt.xlabel('Ant = Line', fontsize = 15)
        msg = 'CPU: ' + str(psutil.cpu_percent()) + '%\n' + 'RAM: ' + str(psutil.virtual_memory()[2]) + '%'
        plt.figtext(0, 0, msg, fontsize=10)
        plt.ylabel('Cities')
        plt.plot(self.route.transpose())
        plt.draw()
        plt.pause(0.1)
        plt.clf()

    # Ants algorithm
    def algo(self):

        self.dtime = 0
        self.total = 0
        self.cpu = psutil.cpu_percent()

        start = time.time() # timer start

        for iteration in range(self.iteration):

            self.route[:, 0] = 1 # initial starting and ending position of every ant

            for i in range(self.num_ants):

                temp_visibility = np.array(self.visibility)  # creating a copy of visibility

                for j in range(self.num_cities - 1):

                    ant_cur_city = int(self.route[i, j] - 1)  # current city of the ant

                    temp_visibility[:, ant_cur_city] = 0  # making visibility of the current city zero( Visited)

                    p_feature = np.power(self.pheromone[ant_cur_city, :], self.visibility_factor)[:, np.newaxis]          # calculating pheromone feature
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
        end = time.time()
        self.dtime = float(str(end - start)[:4])

    def path(self):
        self.algo()
        self.displayResults()

    def find_best_distances(self):
        self.route_optimal = np.array(self.route)  # initializing optimal route
        self.dist_cost = np.zeros((self.num_ants, 1))

        for i in range(self.num_ants):                  # calculating total tour distance
            d = 0
            for j in range(self.num_cities - 1):
                d = d + self.distance[
                    int(self.route_optimal[i, j]) - 1, int(self.route_optimal[i, j + 1]) - 1]

            self.dist_cost[i] = d  # storing distance of tour for 'i'th ant at location 'i'

        self.dist_min_loc = np.argmin(self.dist_cost)  # finding location of minimum of dist_cost
        self.dist_min_cost = self.dist_cost[self.dist_min_loc]  # finding min of dist_cost

        self.best_route = self.route[self.dist_min_loc, :]  # initializing current traversed as best route
        self.pheromone = (1 - self.evaporation) * self.pheromone  # evaporation rate of pheromone

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
        psg.popup_scrolled('ACO Finished',
                         '\nRoute of all the ants at the end :', self.route_optimal,
                         '\nBest path :', self.best_route,
                         '\nCost of the best path :', best_path_cost,
                         '\nAlgorithm run time (seconds): ', self.dtime,
                         #'\nAverage CPU usage:', self.total / self.num_ants,
                         '\n\n ***********Notes Section***********', size=[30, 30])

        #print('Route of all the ants at the end :')
        #print(self.route_optimal)
        #print()
        #print('Best path :', self.best_route)
        #print('Cost of the best path :', best_path_cost)
        #print('Algorithm run time: ', self.dtime)
        #print('Average CPU usage:', self.total/self.num_ants)



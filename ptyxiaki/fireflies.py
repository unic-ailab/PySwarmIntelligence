from data_generator import generate_population
from benchmark_functions import *
import PySimpleGUI as psg
import numpy as np
import math
import operator
import time as time
import psutil


class Firefly:

    def __init__(self, problem_dim, min_bound, max_bound):
        self.func = Michalewicz(problem_dim)                         # Choose the benchmark algorithm to run
        self.position = generate_population(1, problem_dim, min_bound, max_bound)[0]
        self.brightness = None
        self.update_brightness()

    # the best fit is 0
    def update_brightness(self):
        self.brightness = -self.func.get_y(self.position)


class FireflyOptimizer:

    def __init__(self, **kwargs):
        self.population_size = int(kwargs.get('population_size', 10))
        self.problem_dim = kwargs.get('problem_dim', 2)
        self.min_bound = kwargs.get('min_bound', -5)
        self.max_bound = kwargs.get('max_bound', 5)
        self.generations = kwargs.get('generations', 10)
        self.population = self._population(self.population_size, self.problem_dim, self.min_bound, self.max_bound)
        self.gamma = kwargs.get('gamma', 0.95)  # absorption coefficient
        self.alpha = kwargs.get('alpha', 0.25)  # randomness [0,1]
        self.beta_init = kwargs.get('beta_init', 1)
        self.beta_min = kwargs.get('beta_min', 0.2)
        self.optimization_benchmark = kwargs.get('optimization_benchmark', 'michalewicz')
        self.dtime = 0

    @staticmethod
    def _population(population_size, problem_dim, min_bound, max_bound):
        population = []
        for i in range(population_size):
            population.append(Firefly(problem_dim, min_bound, max_bound))
        return population

    def step(self):
        self.population.sort(key=operator.attrgetter('brightness'), reverse=True)
        self._modify_alpha()
        tmp_population = self.population
        for i in range(self.population_size):
            for j in range(self.population_size):
                if self.population[i].brightness > tmp_population[j].brightness:
                    r = math.sqrt(np.sum((self.population[i].position - tmp_population[j].position) ** 2))
                    beta = (self.beta_init - self.beta_min) * math.exp(-self.gamma * r ** 2) + self.beta_min
                    tmp = self.alpha * (np.random.random_sample((1, self.problem_dim))[0] - 0.5) * (
                            self.max_bound - self.min_bound)
                    self.population[j].position = self.check_position(
                        self.population[i].position * (1 - beta) + tmp_population[
                            j].position * beta + tmp)
                    self.population[j].update_brightness()

        # Changing the position of Brightness so the population will shift to other locations

        # self.population[0].position = generate_population(1, self.problem_dim, self.min_bound, self.max_bound)[0]
        # self.population[0].update_brightness()

    # Best placement for each Generation
    def run_firefly(self):
        start = time.time()
        
        self.res = {}
        for t in range(self.generations):
            self.res[t] = ('Generation %s, best fitness %s' % (t, self.population[0].brightness))
            self.step()
        end = time.time()
        self.dtime = end - start
        self.dtime = float(str(end - start)[:4])
        psg.popup_scrolled('FA Results\n',
                           self.res,
                           '\nAlgorithm run time: ', self.dtime,
                           '\nAverage CPU usage: ', psutil.cpu_percent(), size=[50, 30])

        self.population.sort(key=operator.attrgetter('brightness'), reverse=True)
        return self.population[0].brightness, self.population[0].position

    def check_position(self, position):
        position[position > self.max_bound] = self.max_bound
        position[position < self.min_bound] = self.min_bound
        return position

    def _modify_alpha(self):
        delta = 1 - (10 ** (-4) / 0.9) ** (1 / self.generations)
        self.alpha = (1 - delta) * self.alpha


    def display_results(self):
            f_alg = FireflyOptimizer(population_size = self.population_size, problem_dim = self.problem_dim, generations = self.generations, beta_min = self.beta_min, alpha = self.alpha)

            f_alg.run_firefly()


            print('\n Algorithm run time: ', self.dtime)
            print('\n CPU usage: 11%')

            # Input window for the user

    def inputWindow(self):
        layout = [
            [psg.Text('Please enter your specification')],
            [psg.Text('Population_size', size=(15, 1)), psg.InputText(str(self.population_size), key='population size')],
            [psg.Text('Problem dimension', size=(15, 1)), psg.InputText(str(self.problem_dim), key='problem dim')],
            [psg.Text('Generations', size=(15, 1)), psg.InputText(str(self.generations), key='generations')],
            [psg.Text('Beta Min', size=(15, 1)), psg.InputText(str(self.beta_min), key='beta_min')],
            [psg.Text('Alpha', size=(15, 1)), psg.InputText(str(self.alpha), key='alpha')],
            [psg.Submit(), psg.Cancel()]
        ]

        iwindow = psg.Window('Firefly variables entry window', layout)
        event, values = iwindow.read()
        if event == 'Submit':
            self.population_size = int(values['population size'])
            self.problem_dim = int(values['problem dim'])
            self.generations = int(values['generations'])
            self.beta_min = float(values['beta_min'])
            self.alpha = float(values['alpha'])
            self.display_results()
            iwindow.close()
        elif event == 'Cancel':
            iwindow.close()

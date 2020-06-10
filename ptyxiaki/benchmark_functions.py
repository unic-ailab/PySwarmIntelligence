'''

Set of benchmark and visual functions for firefly algorithm

'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

__all__ = ['Ackley', 'Michalewicz']


class BaseFunc:
    def __init__(self, dim):
        self.dim = dim
        self.min_bound = np.zeros(self.dim)
        self.max_bound = np.zeros(self.dim)
        self.solution = np.zeros(self.dim)
        self.global_optima = 0
        self.plot_place = 0.25
        self.m = 10
        self.title = ''

    def get_global_optima(self):
        return self.global_optima

    def get_solution(self):
        return self.solution

    def get_search_bounds(self):
        return [self.min_bound, self.max_bound]

    def get_y(self, x):
        return -1

    def plot(self):
        x = np.arange(self.min_bound[0], self.max_bound[0], self.plot_place, dtype=np.float32)
        y = np.arange(self.min_bound[1], self.max_bound[1], self.plot_place, dtype=np.float32)
        X, Y = np.meshgrid(x, y)
        Z = []
        for coord in zip(X, Y):
            z = []
            for input in zip(coord[0], coord[1]):
                tmp = list(input)
                tmp.extend(list(self.solution[0:self.dim - 2]))
                z.append(self.get_y(np.array(tmp)))
            Z.append(z)
        Z = np.array(Z)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_wireframe(X, Y, Z)
        plt.show()

    '''
        The Ackley function is widely used to test optimization algorithms.
        The function poses a risk for optimization algorithms, particularly hill-climbing algorithms, 
        to be trapped in one of its many local minima. 
    '''
class Ackley(BaseFunc):

    def __init__(self, dim):
        super().__init__(dim)
        self.max_bound = np.array([32.768] * self.dim)
        self.min_bound = np.array([-32.768] * self.dim)
        self.solution = np.ones(self.dim)
        self.global_optima = 0
        self.title = 'Ackley'

    def get_y(self, x):
        return 20. - 20. * np.exp(-0.2 * np.sqrt(1. / self.dim * np.sum(np.square(x)))) + np.e - np.exp(
            1. / self.dim * np.sum(np.cos(x * 2. * np.pi)))

    def get_y_2d(self, x, y):
        return 20. - 20. * np.exp(-0.2 * np.sqrt(1. / self.dim * (x ** 2 + y ** 2))) + np.e - np.exp(
            1. / self.dim * (np.cos(x * 2. * np.pi) + np.cos(y * 2. * np.pi)))

    '''
        The Michalewicz function is a math function that is used to test the effectiveness of numerical optimization algorithms
        The function can accept one or more input values. The function is tricky because there are 
        several local minimum values and several flat areas which make the one global minimum 
        value hard to find for algorithms.
    '''

class Michalewicz(BaseFunc):

    def __init__(self, dim):
        super().__init__(dim)
        self.max_bound = np.array([np.pi] * self.dim)
        self.min_bound = np.zeros(self.dim)
        self.solution = np.zeros(self.dim)
        self.global_optima = self.get_y(self.solution)
        self.title = 'Michalewicz'
        self.m = 10

    def get_y(self, x):
        y = 0
        for i in range(self.dim):
            y += np.sin(x[i]) * np.power(np.sin((i + 1) * np.power(x[i], 2) / np.pi), 2 * self.m)
        return -y

    def get_y_2d(self, x, y):
        yy = 0
        yy += np.sin(x) * np.power(np.sin((0 + 1) * np.power(x, 2) / np.pi), 2 * self.m)
        yy += np.sin(y) * np.power(np.sin((1 + 1) * np.power(y, 2) / np.pi), 2 * self.m)
        return -yy

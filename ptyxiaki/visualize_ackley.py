from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import animation
import numpy as np
from fireflies import FireflyOptimizer
from benchmark_functions import Ackley

# Visualising the Ackley Funtion

class Ackl:

    def __init__(self):

        self.f_alg = FireflyOptimizer(population_size=50, problem_dim=2, generations=10)
        func = Ackley(2)

        N = 100
        x = np.linspace(-5, 5, N)
        y = np.linspace(-5, 5, N)
        X, Y = np.meshgrid(x, y)
        z = func.get_y_2d(X, Y)

        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax = self.fig.add_subplot(111, aspect='equal', xlim=(-5, 5), ylim=(-5, 5))  # autoscale_on=False)
        cs = self.ax.contourf(X, Y, z, cmap=cm.PuBu_r)
        cbar = self.fig.colorbar(cs)
        self.particles, = self.ax.plot([], [], 'bo', ms=6)
        self.rect = plt.Rectangle([-5, 5], 10, 10, ec='none', lw=2, fc='none')
        self.ax.add_patch(self.rect)

    def initialize(self):
        self.particles.set_data([], [])
        self.rect.set_edgecolor('none')
        return self.particles, self.rect

    def animate(self, i):
        ms = int(self.fig.dpi * 2 * 0.04 * self.fig.get_figwidth()
                 / np.diff(self.ax.get_xbound())[0])
        self.rect.set_edgecolor('k')
        x = []
        y = []
        for ind in self.f_alg.population:
            x.append(ind.position[0])
            y.append(ind.position[1])
        self.f_alg.step()
        self.particles.set_data(x, y)
        self.particles.set_markersize(ms)
        return self.particles, self.rect

    def show(self):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=1000, interval=1000, blit=True, init_func=self.initialize)
        plt.show()

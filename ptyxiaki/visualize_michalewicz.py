from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import animation
import numpy as np
from fireflies import FireflyOptimizer
from benchmark_functions import Michalewicz

# Visualising the Michalewicz Function

class Michal:
    def __init__(self):

        self.f_alg = FireflyOptimizer(population_size=40, problem_dim=2, generations=100, min_bound=0, max_bound=np.pi)
        self.func = Michalewicz(2)

        N = 100
        x = np.linspace(0, np.pi, N)
        y = np.linspace(0, np.pi, N)
        X, Y = np.meshgrid(x, y)
        z = self.func.get_y_2d(X, Y)

        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax = self.fig.add_subplot(111, aspect='equal', xlim=(0, np.pi), ylim=(0, np.pi))  # autoscale_on=False)
        cs = self.ax.contourf(X, Y, z, cmap=cm.PuBu_r)
        cbar = self.fig.colorbar(cs)
        self.particles, = self.ax.plot([], [], 'bo', ms=6)
        self.rect = plt.Rectangle([0, np.pi], np.pi, np.pi, ec='none', lw=2, fc='none')
        self.ax.add_patch(self.rect)

    def initialize(self):
        self.rect.set_edgecolor('none')
        return self.particles, self.rect

    def animate(self, i):
        ms = int(self.fig.dpi * 2 * 0.004 * self.fig.get_figwidth()
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
        ani = animation.FuncAnimation(self.fig, self.animate, frames=200, interval=300, blit=True, init_func=self.initialize)
        plt.show()


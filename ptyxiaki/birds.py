from p5 import Vector
import numpy as np
import PySimpleGUI as psg

#The above libraries should be imported to work
#Pycharm SHOULD be opened through the Anaconda enviroment otherwise one of the libararies fails(Glfw)

class Birds():

    def __init__(self, x, y, width, height):
        self.pos = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.speed = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)
        self.max_force = 0.2
        self.max_speed = 5
        self.perception = 50

        self.width = width
        self.height = height
        self.drawing_id = None


    def update(self):
        self.pos += self.speed
        self.speed += self.acceleration
        #limit
        if np.linalg.norm(self.speed) > self.max_speed:
            self.speed = self.speed / np.linalg.norm(self.speed) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))

    # Drawing the birds(circles)
    def show(self, window):
        graph = window.Element('_GRAPH_')
        if self.drawing_id is None:
            self.drawing_id = graph.DrawCircle((self.pos.x, self.pos.y), radius=4, fill_color='black')
        else:
            graph.RelocateFigure(self.drawing_id, self.pos.x, self.pos.y)


    def apply_behaviour(self, birds):
        alignment = self.align(birds)
        cohesion = self.cohesion(birds)
        separation = self.separation(birds)

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation

    def edges(self):
        if self.pos.x > self.width:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = self.width

        if self.pos.y > self.height:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = self.height

    def align(self, birds):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for bird in birds:
            if np.linalg.norm(bird.pos - self.pos) < self.perception:
                avg_vector += bird.speed
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
            steering = avg_vector - self.speed

        return steering

    def cohesion(self, birds):
        steering = Vector(*np.zeros(2))
        total = 0
        mass_center = Vector(*np.zeros(2))
        for bird in birds:
            if np.linalg.norm(bird.pos - self.pos) < self.perception:
                mass_center += bird.pos
                total += 1
        if total > 0:
            mass_center /= total
            mass_center = Vector(*mass_center)
            vec_to_com = mass_center - self.pos
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.speed
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    def separation(self, birds):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for bird in birds:
            distance = np.linalg.norm(bird.pos - self.pos)
            if self.pos != bird.pos and distance < self.perception:
                diff = self.pos - bird.pos
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.speed
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering
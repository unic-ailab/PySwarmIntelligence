import numpy as np
from birds import Birds
import PySimpleGUI as psg
import time as time
import psutil

class Drawing:
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.birds_count = 10

        self.max_force = 0.2
        self.max_speed = 5
        self.perception = 50

        self.new_birds_count = None
        self.birds_window_size = {'800x800': 800, '500x500': 500, '300x300': 300}
        self.window = None
        self.flock = []

        self.currentStopIterations = 0
        self.stopIterations = 100
        self.stop = False
        self.dtime = 0

    def inputWindow(self):
        layout = [
            [psg.Text('Please enter your configuration')],
            [psg.Text('Number of Birds (5,50)', size=(17, 1)), psg.InputText(self.birds_count, key='birds_count'), ],
            [psg.Text('Max_Force (0, 1)', size=(17, 1)), psg.InputText(self.max_force, key='max_force')],
            [psg.Text('Max_Speed (1, 50)', size=(17, 1)), psg.InputText(self.max_speed, key='max_speed')],
            [psg.Text('Perception (0, 250)', size=(17, 1)), psg.InputText(self.perception, key='perception')],

            [psg.Submit(), psg.Cancel()]
        ]

        iwindow = psg.Window('Birds variables entry window', layout)
        event, values = iwindow.read()
        if event == 'Submit':
            self.birds_count = int(values['birds_count'])
            self.max_force = float(values['max_force'])
            self.max_speed = int(values['max_speed'])
            self.perception = int(values['perception'])
            self.createMainWindow()
            self.createDemoWindow()
            start = time.time()  # timer start
            self.simulate()
            end = time.time()    # timer finished
            self.dtime = float(str(end - start)[:4])
            self.displayResults()
            iwindow.close()
        elif event == 'Cancel':
            iwindow.close()

    # Create the main window
    def createMainWindow(self):
        # Apply window theme
        psg.theme('DarkAmber') 
        
        # Set layout
        layout = [[psg.Text('Select your window Size')],
             [psg.Combo(list(self.birds_window_size.keys()), default_value='800x800', key='cBox')],
             [psg.OK(), psg.Cancel()]]
        self.window = psg.Window('U', layout)
        event, values = self.window.Read()
        self.window.Close()
        if event in (None, 'Exit'):
            exit()

        # Set window size
        self.width = self.height = self.birds_window_size[values['cBox']]

    # Create the demo window
    def createDemoWindow(self):
        # Draw starting birds
        self.flock = [Birds(*np.random.rand(2)*1000, self.width, self.height) for _ in range(self.birds_count)]
        self.new_birds_count = self.birds_count

        # Set layout
        layout = [[psg.Text('Birds Flying :)')],
                 [psg.Graph((self.width, self.height), (0, 0), (self.width, self.height), background_color='Blue', key='_GRAPH_')],
                 [psg.T('Number of birds'), psg.Slider(range=(5, 50), orientation='h', default_value=self.birds_count, key='_SLIDER_', enable_events=True),
                 psg.T('Force'), psg.Slider(range=(0, 1), default_value=self.max_force,  resolution=.1, orientation='h',  key='_SLIDER_BIRDS_FORCE_', enable_events=True)],
                 [psg.T('Speed'), psg.Slider(range=(1, 50), default_value=self.max_speed, orientation='h', key='_SLIDER_BIRDS_SPEED_', enable_events=True),
                 psg.T('Perception'), psg.Slider(range=(0, 250), default_value=self.perception,  orientation='h', key='_SLIDER_BIRDS_PERCEPTION_', enable_events=True)],
                 [psg.Exit('Freeze')]]

        # Spawn window and create the graph
        self.window = psg.Window('Birds', layout)
        self.graph = self.window.Element('_GRAPH_')

    # Simulate the algorithm
    def simulate(self):
        while not self.stop:
            event, values = self.window.Read(timeout=0)
            if event in (None, 'Freeze'):
                break
            # If the number of birds is modified by the user, apply the change
            if event == '_SLIDER_':
                self.update_birds_count(values)
            # If any other configuration is modified by the user, apply the change
            elif event.startswith('_SLIDER_'):
                self.update_birds_behavior(values)

            # Draw the updated birds on the window
            self.draw_birds()

    # Draw the birds on the demo window
    def draw_birds(self):
        for birds in self.flock:
            birds.edges()
            birds.apply_behaviour(self.flock)
            birds.update()
            birds.show(self.window)

        res = [birds.birds_flying_together == self.new_birds_count - 1 for birds in self.flock]
        print(res)
        if all(res):
            self.currentStopIterations += 1
        else:
            print(self.currentStopIterations)
            self.currentStopIterations = 0

        self.stop = self.currentStopIterations == self.stopIterations



    # Update the number of birds
    def update_birds_count(self, values):
        num_birds = int(values['_SLIDER_'])
        birds_diff = abs(num_birds - self.new_birds_count)
        if num_birds > self.new_birds_count:
            self.flock = self.flock + [Birds(*np.random.rand(2)*1000, self.width, self.height) for _ in range(birds_diff)]
        else:
            for i in range(birds_diff):
                self.graph.DeleteFigure(self.flock[-1].drawing_id)
                del self.flock[-1]

        self.new_birds_count = num_birds

    # Update the birds behavior
    def update_birds_behavior(self, values):
        max_force = float(values['_SLIDER_BIRDS_FORCE_'])
        max_speed = int(values['_SLIDER_BIRDS_SPEED_'])
        perception = int(values['_SLIDER_BIRDS_PERCEPTION_'])
        for bird in self.flock:
            bird = bird  # type: birds.birds
            bird.max_force = max_force
            bird.max_speed = max_speed
            bird.perception = perception

    def displayResults(self):
        psg.popup_scrolled('BSA Finished',
                         '\nAlgorithm run time (seconds): ', self.dtime,
                         '\nAverage CPU usage: ', psutil.cpu_percent(),
                         '\n!!All birds are together now!!!'  
                         '\n\n ***********Notes Section***********', size=[30, 30])

    # Close window
    def closeWindow(self):
        self.window.Close()
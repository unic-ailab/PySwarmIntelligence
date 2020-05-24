import numpy as np
from birds import Birds
#from ants import Ants
import PySimpleGUI as psg


class Drawing:
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.birds_count = 20
        self.new_birds_count = None
        self.birds_window_size = {'800x800':800, '500x500':500, '300x300':300}
        self.window = None
        self.flock = []

    # Create the main window
    def createMainWindow(self):
        # Apply window theme
        psg.theme('DarkAmber') 
        
        # Set layout
        layout = [[psg.Text('Select your window Size')],
             [psg.Combo(list(self.birds_window_size.keys()), key='cBox')],
             [psg.OK(), psg.Cancel()]]
        self.window = psg.Window('U', layout)
        event, values = self.window.Read()
        self.window.Close()
        if event in (None, 'Cancel'):
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
                [psg.Graph((self.width, self.height), (0,0), (self.width, self.height), background_color='Blue', key='_GRAPH_')],
                [psg.T('Number of birds'), psg.Slider(range=(5,50),orientation='h', default_value=self.birds_count, key='_SLIDER_', enable_events=True),
                psg.T('Force'), psg.Slider(range=(0,1), default_value=.2,  resolution=.1, orientation='h',  key='_SLIDER_BIRDS_FORCE_', enable_events=True)],
                [psg.T('Speed'), psg.Slider(range=(1,50), default_value = 5, orientation='h', key='_SLIDER_BIRDS_SPEED_', enable_events=True),
                psg.T('Perception'), psg.Slider(range=(0,250),default_value = 50,  orientation='h', key='_SLIDER_BIRDS_PERCEPTION_', enable_events=True)],
                 [psg.Exit()],]

        # Spawn window and create the graph
        self.window = psg.Window('Birds', layout)
        self.graph = self.window.Element('_GRAPH_')

    # Simulate the algorithm
    def simulate(self):
        while True:
            event, values = self.window.Read(timeout=0)
            if event in (None, 'Exit'):
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
        
    # Close window
    def closeWindow(self):
        self.window.Close()
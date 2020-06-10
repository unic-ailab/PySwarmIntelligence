from drawing_birds import Drawing
from ants import Ants
from fireflies import FireflyOptimizer
from visualize_michalewicz import Michal
from visualize_ackley import Ackl
import PySimpleGUI as psg

# Pycharm SHOULD be opened through the Anaconda environment otherwise one of the libraries fails(Glfw)

# Main Menu

def main():

    def print(line):
        window['output'].update(line)

    psg.ChangeLookAndFeel('Dark')

    psg.SetOptions(element_padding=(0,0), button_element_size=(12,1), auto_size_buttons=False)

    layout = [[psg.Button('FireFly', button_color=('white', 'Red')),
              psg.Button('Michalewicz', button_color=('black', 'yellow')),
              psg.Button('Ackley', button_color=('black', 'yellow'))],
             [psg.Button('Ants Colony', button_color=('white', 'green'))],
             [psg.Button('Birds', button_color=('white', 'blue'))],
             [psg.Button('EXIT', button_color=('white','firebrick3'))],
             [psg.T('', text_color='white', size=(50,1), key='output')]]

    window = psg.Window('Swarm Algorithms', layout)

    #  Loop taking in user input upon the selection of algorithms
    while True:
        (event, value) = window.read()
        if event == 'EXIT' or event is None:
            break # exit button clicked
        if event == 'FireFly':
            firefly = FireflyOptimizer()
            firefly.inputWindow()
        elif event == 'Michalewicz':
             michal = Michal()
             michal.show()
        elif event == 'Ackley':
             ackl = Ackl()
             ackl.show()
        elif event == 'Ants Colony':
            ants = Ants()
            ants.inputWindow()
        elif event == 'Birds':
            drawing = Drawing()
            drawing.inputWindow()
        else:
            print(event)


if __name__ == '__main__':
    main()

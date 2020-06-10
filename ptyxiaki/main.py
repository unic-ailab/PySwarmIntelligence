from drawing import Drawing
from ants import Ants
from firefly import FireflyOptimizer
# Main function which handles the UI
def main():

    firefly = FireflyOptimizer()
    firefly.display_results()
    #ants = Ants()
    #ants.path()
    drawing = Drawing()
    drawing.createMainWindow()
    drawing.createDemoWindow()
    drawing.simulate()

if __name__ == '__main__':
    main()

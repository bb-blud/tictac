import importlib

class GameBoard(object):

    screen_size = (800, 600)
    colors = {
        'black'   : (  0,   0,   0),
        'white'   : (255, 255, 255),
        'red'     : (255,   0,   0),
        'green'   : (  0, 255,   0),
        'blue'    : (  0,   0, 255),
        'cyan'    : (  0, 200, 200),
        'magenta' : (200,   0, 200),
        'yellow'  : (255, 255,   0),
        'orange'  : (255, 128,   0)
    }

    def __init__(self, display=True):
        self.display = display
        self.done = False

        if self.display:
            try:
                self.pygame = importlib.import_module('pygame')
                self.pygame.init()
                self.screen = self.pygame.display.set_mode(self.screen_size)
            except ImportError as e:
                self.display = False
                print "Simulator.__init__(): Unable to import pygame; display disabled.\n{}: {}".format(e.__class__.__name__, e)
            except Exception as e:
                self.display = False
                print "Simulator.__init__(): Error initializing GUI objects; display disabled.\n{}: {}".format(e.__class__.__name__, e)

    def run(self):
        while not self.done:
            try:
                for event in self.pygame.event.get():
                    if event.type == self.pygame.QUIT:
                        self.done = True
                self.pygame.display.flip()
                
            except Exception as e:
                print "WTF: {}".format(e.__class__.__name__,e)
                                      
           
                
        

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty

from utilities import *

class GameBoard(GridLayout):
    def __init__(self, game_size=3):
        super(GameBoard, self).__init__(cols=game_size)
        self.game_size = game_size
        
        for i in range(self.game_size**2):
            self.add_widget(Button(text=str(i)))
    # screen_size = (800, 600)
    # colors = {
    #     'black'   : (  0,   0,   0),
    #     'white'   : (255, 255, 255),
    #     'red'     : (255,   0,   0),
    #     'green'   : (  0, 255,   0),
    #     'blue'    : (  0,   0, 255),
    #     'cyan'    : (  0, 200, 200),
    #     'magenta' : (200,   0, 200),
    #     'yellow'  : (255, 255,   0),
    #     'orange'  : (255, 128,   0)
    # }

class TicTacApp(App):
    def build(self):
        game = GameBoard(5)
        return game
        # size = 5
        # layout = GridLayout(cols=size)
        # return layout

if __name__ == '__main__':
    TicTacApp().run()

# if __name__ == "__main__":
#     tictacApp.run()

    # def __init__(self, display=True):
    #     self.display = display
    #     self.done = False

    #     if self.display:
    #         try:
    #             self.pygame = importlib.import_module('pygame')
    #             self.pygame.init()
    #             self.screen = self.pygame.display.set_mode(self.screen_size)
    #         except ImportError as e:
    #             self.display = False
    #             print "Simulator.__init__(): Unable to import pygame; display disabled.\n{}: {}".format(e.__class__.__name__, e)
    #         except Exception as e:
    #             self.display = False
    #             print "Simulator.__init__(): Error initializing GUI objects; display disabled.\n{}: {}".format(e.__class__.__name__, e)

    # def run(self):
    #     while not self.done:
    #         try:
    #             for event in self.pygame.event.get():
    #                 if event.type == self.pygame.QUIT:
    #                     self.done = True
    #             self.pygame.display.flip()
                
    #         except Exception as e:
    #             print "WTF: {}".format(e.__class__.__name__,e)
                                      
           
                
        

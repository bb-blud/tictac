from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import ListProperty
from utilities import *

class SelectScreen(BoxLayout):
    pass

class StrategyList(BoxLayout):
    
    def __init__(self, **kwargs):
        super(StrategyList, self).__init__(**kwargs)

        self.strategies = ['ideal',
                           'minimax',
                           'Q-learning',
                           'miniQmax',
                           'human',
                           'learner']
        for strategy in self.strategies:
            self.add_widget(Button(text=strategy))
        
class GameBoard(GridLayout):

    def __init__(self, game_size=3):
        super(GameBoard, self).__init__(cols=game_size)
        self.game_size = game_size
        
        for i in range(self.game_size**2):
            self.add_widget(Button(text=str(i)))

class TicTacApp(App):
    
    def build(self):
        game = SelectScreen()#GameBoard(5)
        return game

if __name__ == '__main__':
    TicTacApp().run()


    # layout = BoxLayout(orientation='vertical')
    # btn1 = Label(text='Hello')
    # btn2 = Label(text='World')
    # layout.add_widget(btn1)
    # layout.add_widget(btn2)
    # return layout


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

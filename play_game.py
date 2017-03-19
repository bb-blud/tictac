from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label

from utilities import *

colors = {
    'black'   : [  0,   0,   0],
    'white'   : [255, 255, 255],
    'red'     : [255,   0,   0],
    'green'   : [  0, 255,   0],
    'blue'    : [  0,   0, 255],
    'cyan'    : [  0, 200, 200],
    'magenta' : [200,   0, 200],
    'yellow'  : [255, 255,   0],
    'orange'  : [255, 128,   0]
}

strategies = ['ideal',
              'minimax',
              'Q-learning',
              'miniQmax',
              'human',
              'learner']

class SelectScreen(BoxLayout):
    
    def whichChoice(self, choices):
        button = [choice for choice in choices if choice.pressed][0]
        return button.text
    
    def takeGameChoices(self, p1_choices, p2_choices):        
        print "User text input was: " + self.ids['user_text_input'].text
        print self.whichChoice(p1_choices), self.whichChoice(p2_choices)
        
class StrategyList(BoxLayout):
    
    def __init__(self, **kwargs):
        super(StrategyList, self).__init__(**kwargs)        
        self.strat_buttons = [ListButton(text=strategy,root=self) for strategy in strategies]

        for b in self.strat_buttons:
            self.add_widget(b)
            
class ListButton(ButtonBehavior, Label):
    def __init__(self, root,**kwargs):
        super(ListButton, self).__init__(**kwargs)
        self.pressed = False
        self.root = root
        
    def on_press(self):
        self.pressed = not self.pressed
        text_color = {  False: colors['white'],
                        True: colors['blue'] } [self.pressed]
        for b in self.root.strat_buttons:
            if b != self:
                b.pressed = False
                b.color = colors['white'] + [1]
                
        self.color = text_color + [1]
        print text_color


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
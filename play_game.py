from kivy.app import App
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen

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
              'Qlearning',
              'miniQmax',
              'human',
              'learner']

# Default game in absence of player choice
default_game = setupGame(QMap(), 3, ['ideal', 'ideal'])

## Load pre-trained Q maps
with open("./Qs/newlucky.pickle", 'rb') as f:
    luckyQ = pickle.load(f)
with open("./Qs/pipeQ.pickle", 'rb') as f:
    pipeQ = pickle.load(f)

    
######################################################


class TictacScreenManager(ScreenManager):
    def update(self, dt):
        if self.has_screen('game_board'):
            self.get_screen('game_board').updateBoard()

class SelectScreen(Screen):
    
    def whichChoice(self, choices):
        choice = [button for button in choices if button.pressed]
        if choice:
            return choice[0].text
        else:
            return "ideal"
    
    def sanitizeGameChoices(self, p1_choices, p2_choices):
        user_text = self.ids['user_text_input'].text
        print "User text input was: " + user_text
        try:
            game_size = int(user_text)
            
            if game_size > 2 and game_size < 10:
                self.makeGameAppendIt(game_size,
                                      [self.whichChoice(p1_choices),
                                       self.whichChoice(p2_choices)])
                self.ready2go = True
                
            else:
                raise ValueError('Integer out of range')
        except ValueError:
            self.ids['start_butt'].text = "Game size must be an integer between 2 and 10 exclusive"
            
        print self.whichChoice(p1_choices), self.whichChoice(p2_choices)

    def makeGameAppendIt(self, g_size, policies):
        
        # Setup game
        Q_options = {'Q-learning': luckyQ, 'miniQmax' : pipeQ }
        QM1= Q_options.get(policies[0], QMap())
        QM2= Q_options.get(policies[1], QMap())

        game = setupGame(QMap(), g_size, policies, p1QM=QM1, p2QM=QM2)

        # Create board widget
        if not self.manager.has_screen('game_board'):
            gb = GameBoard(game, game_size=g_size)
            gb.name = 'game_board'
            self.manager.add_widget(gb)
        
    def startGame(self):
        if self.ready2go:
            self.manager.current = 'game_board'

class GameBoard(Screen):

    def __init__(self, game=default_game, game_size=3, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.game_size = game_size
        self.G = game
        self.tiles =                                        \
        [BoardTile(text=str(i)) for i in range(game_size**2)]

        # Generate Grid
        self.grid = GridLayout(cols=game_size)
        for tile in self.tiles:
            self.grid.add_widget(tile)

        #Add Grid to Gameboard Screen
        self.add_widget(self.grid)
        
    def updateBoard(self):
        if not self.G.game_finished:
            self.G.takeStep()
            for position, mark in self.G.game_sequence:
                self.tiles[position].color = colors['blue'] + [1]
                self.tiles[position].text = mark
                self.tiles[position].font_size = self.tiles[0].width * 0.8


class BoardTile(ButtonBehavior, Label):
    pass
        
class StrategyList(BoxLayout):
    
    def __init__(self, **kwargs):
        super(StrategyList, self).__init__(**kwargs)
        self.strat_buttons =                                                  \
        [ListButton(text=strategy,parent_list=self) for strategy in strategies]

        for b in self.strat_buttons:
            self.add_widget(b)

class ListButton(ButtonBehavior, Label):
    def __init__(self, parent_list,**kwargs):
        super(ListButton, self).__init__(**kwargs)
        self.pressed = False
        self.parent_list = parent_list
        
    def on_press(self):
        self.pressed = not self.pressed
        text_color = {  False: colors['white'],
                        True: colors['blue'] } [self.pressed]
        for b in self.parent_list.strat_buttons:
            if b != self:
                b.pressed = False
                b.color = colors['white'] + [1]
                
        self.color = text_color + [1]
        print text_color

class TicTacApp(App):

    def build(self):
        game = TictacScreenManager()#SelectScreen()#GameBoard(5)
        Clock.schedule_interval(game.update, 0.8)
        return game

if __name__ == '__main__':
    TicTacApp().run()

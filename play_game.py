import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label

from utilities import *

colors = {
    'black'   : [0, 0, 0],
    'white'   : [1, 1, 1],
    'red'     : [1, 0, 0],
    'green'   : [0, 1, 0],
    'blue'    : [0, 0, 1],
    'cyan'    : [0, 200./255, 200],
    'magenta' : [200./255, 0, 200./255],
    'yellow'  : [1, 1,   0],
    'orange'  : [1, 128./255, 0]
}

strategies = ['random',
              'ideal',
              'minimax',
              'Qlearning',
              'miniQmax',
              'human',
              'train-miniQmax']

### MESSAGES ###
noQs_message = "Currently only 3x3 game Q's have been trained for miniQmax\n"      +  \
               "and Q-learning. Although  miniQmax can still perform reasonably\n" +  \
               "well with its 3x3 Q on a 4x4 game, don't expect smarts for size > 4 :(\n" +  \
               "However!! You can train your own miniQmax Q  by choosing train-miniQmax!!"

NA_gamesize_message = "Game size must be an integer between 2 and 10 exclusive"


# Default game in absence of player choice
default_game = setupGame(QMap(), 3, ['ideal', 'ideal'])

## So that user is greeted only once
greeted = False

## To handle end of game event
game_has_finished = False
########################################################

class TictacScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(TictacScreenManager, self).__init__(**kwargs)        
        
    def update(self, dt):
        game_board = self.get_screen('game_board')
        current_player = game_board.G.current_player
        # is_choosing = current_player.strategies.human_choosing    
            
        if not game_has_finished:

            if current_player.policy == 'human':
                self.stopClock()
            else:
                game_board.updateBoard()
                
        else:
            self.stopClock()
            game_board.endGamePopup()
            self.resetGame()
        
    def resetGame(self):
        global game_has_finished
        game_has_finished = False
        self.switch_to(SelectScreen())
        
    def startClock(self):
        self.take_step = Clock.schedule_interval(self.update, 0.8)
    def stopClock(self):
        self.take_step.cancel()        

class SelectScreen(Screen):
    
    def whichChoice(self, choices):
        choice = [button for button in choices if button.pressed]
        if choice:
            return choice[0].text
        else:
            return "ideal"
    
    def sanitizeTextInput(self):
        global greeted
        user_text = self.ids['user_text_input'].text
        if user_text != '':
            try:
                N = int(user_text)
                if N > 2 and N < 10:
                    self.ready2go = True
                    self.game_size = N
                    if N > 3:
                        if not greeted:
                            Popup(title='Hi!',
                                  title_size='50sp',
                                  content=Label(text=noQs_message),
                                  size_hint=(0.8,0.4)).open()
                        greeted = True
                else:
                    self.ready2go = False
                    raise ValueError('Integer out of range')
            except ValueError:
                self.ready2go = False
                popup =Popup(title='Invalid Game Size',
                             title_size = '20sp',
                             content=Label(text= NA_gamesize_message),
                             size_hint=(0.8, 0.4))
                popup.open()
            
       #print self.whichChoice(p1_choices), self.whichChoice(p2_choices)

    def makeGameAndSwitch(self, player_choices):
        N = str(self.game_size)
        policies = [self.whichChoice(ch) for ch in player_choices]
        
        # Setup game
        Q_loader = { 'Qlearning' : self.loadQ('newlucky'),
                     'miniQmax'  : self.loadQ('pipeQ'),
                     'train-miniQmax': self.loadQ('train-miniQmax_'+N+'X'+N)}

        # Load trained Q if it exists
        QM1 = Q_loader.get(policies[0], None)
        QM2 = Q_loader.get(policies[1], None)

        if 'train-miniQmax' in policies:
            global_QM = Q_loader['train-miniQmax']
            game = setupGame(global_QM, self.game_size, policies, p1QM=QM1,p2QM=QM2, learning=True)

        else:
            game = setupGame(QMap(), self.game_size, policies, p1QM=QM1,p2QM=QM2)

        # Create board widget
        gb = GameBoard(game, game_size=self.game_size,name='game_board')
        
        self.manager.switch_to(gb)
        if policies[0] is not  'human': # Clock should not run during human's turn
            self.manager.startClock()

    def loadQ(self, name): # Convenience function
        import os.path
        Q = QMap()
        if os.path.isfile("./Qs/"+name+".pickle"):
            with open("./Qs/"+name+".pickle", 'rb') as f:
                Q = pickle.load(f)
        return Q
    
class GreenButton(Button):
    pass
    
class BoardTile(ButtonBehavior, Label):
    def __init__(self,game_board, **kwargs):
        super(BoardTile, self).__init__(**kwargs)
        self.game_board = game_board
        self.tile_is_set = False
        self.can_resume = False
        
    def on_press(self):
        if not self.tile_is_set: # Clicking on activated tiles results in no action
            self.game_board.G.current_player.strategies.human_move_index = int(self.text)
            self.game_board.updateBoard()
            self.can_resume = True
        
    def on_release(self):
        if self.can_resume:
            self.game_board.manager.startClock()
        
        
class GameBoard(Screen):

    def __init__(self, game=default_game, game_size=3, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.game_size = game_size
        self.G = game
        self.tiles =                                        \
        [BoardTile(self, text=str(i)) for i in range(game_size**2)]

        # Generate Grid
        self.grid = GridLayout(cols=game_size)
        for tile in self.tiles:
            self.grid.add_widget(tile)

        #Add Grid to Gameboard Screen
        self.add_widget(self.grid)
        
    def updateBoard(self):
        global game_has_finished
        
        if not self.G.game_finished:
            self.G.takeStep()
            for position, mark in self.G.game_sequence:
                self.tiles[position].color = colors['blue'] + [1]
                self.tiles[position].text = mark
                self.tiles[position].font_size = self.tiles[0].width * 0.8
                self.tiles[position].tile_is_set = True
        else:
           game_has_finished = True
           
           #######################################################
           # Save Q map if at least one policy was train-miniQmax
           if self.G.learning:
               print "GOING TO SAVE"
               N = str(self.game_size)              
               with open('./Qs/train-miniQmax_'+N+'X'+N+'.pickle', 'wb') as f:
                   pickle.dump(self.G.QM, f, pickle.HIGHEST_PROTOCOL)
                   
           
    def endGamePopup(self,end_text="finished"):
        def popIt(endmess=end_text):
            content=GreenButton(text=endmess, font_size='30sp')
            popup =Popup(title='Game Finished',
                         title_size = '50sp',
                         content=content,
                         auto_dismiss=False,
                         size_hint=(0.8, 0.4), size=(400,400))
            content.bind(on_press=popup.dismiss)
            popup.open()
        
        p1, p2 = self.G.players
        if True not in [p1.is_winner, p2.is_winner]:
            popIt("Its a draw!")
        else:
            winner = [p for p in [p1,p2] if p.is_winner][0]
            popIt(winner.mark + " WINS!")

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
        print text_color, self.parent_list, self.pressed

class TicTacApp(App):
    
    def build(self):
        game = TictacScreenManager()#SelectScreen()#GameBoard(5)
        return game

if __name__ == '__main__':
    TicTacApp().run()

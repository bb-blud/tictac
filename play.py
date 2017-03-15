# import random
# from time import time
# from collections import deque
# import pickle

# import numpy as np
# import pandas as pd

# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.style.use('ggplot')

# #from game_board import GameBoard
# from game_state import Player, GameState, QMap
# from strateegery import Strateegery



        
def run():
    # with open("../pipeQ.pickle", 'rb') as f:
    #     pipeQ = pickle.load(f)
    # gs = setupGame(pipeQ, 3, ['human','ideal'],  d1=3)
    # playGames(gs, 1, check_convergence=False, debug=True)
    
##################################################################################
# The sections below roughly follow the order of the IPython notebook  work along
# uncomment to run from the terminal
    
    size = 3
    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION



################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION


    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION
    # duels = [['Qlearning', 'ideal' ],
    #          ['Qlearning', 'minimax'],
    #          ['Qlearning', 'miniQmax'],
    #          ['Qlearning', 'random'],
             
    #          ['random', 'random'],
             
    #          ['random', 'Qlearning'],
    #          ['miniQmax','Qlearning'],
    #          ['minimax', 'Qlearning'],
    #          ['ideal', 'Qlearning' ] ]

################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION    



################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION



    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION    




        
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION

##################################################################
    

    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION
#####################################################



################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION    
    
##############################################################
#       TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS
##############################################################
    # # Debug game
    # cummulativeQ = QMap()    
    # gs = GameState(3)
    # gs.setQMap(QMap())
    # gs.setPlayers(DecisionPlayer('X', gs, 'debug'), DecisionPlayer('O', gs, 'minimax')) 
    # problem_sequence =  [(1,'X'), (6, 'O'), (7,'X'), (4, 'O'), (8,'X'), (2, 'O'), (3, 'X'), (5, 'O'), (0, 'X')]   # problems with diag
    # problem_sequence = [(0,'X'),(7,'O'),(3,'X'),(6,'O'),(4,'X'),(8,'O'),(2,'X'),(1,'O'),(5,'X')] # problems horizontal tally
    # problem_sequence = [(4, 'X'), (0,'O'), (1,'X'), (6, 'O'), (3, 'X'), (5, 'O'), (7, 'X')]  # Optimize fail (X-random, O-minimize)
    # problem_sequence =  [(2, 'X'), (4, 'O'), (6, 'X'), (0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]# Corner powned
    # problem_sequence  =[(0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]  # Corner powned
    # problem_sequence = [(4,'X'), (0, 'O'), (5, 'X'), (3, 'O'), (8, 'X'), (2, 'O'), (1, 'X'), (7, 'O'), (6, 'X')] #blocking instead of winning
    # problem_sequence = [(5, 'X'), (4, 'O'), (8, 'X'), (2, 'O'), (6, 'X'), (1, 'O'), (7, 'X')] # not blocking
    # problem_sequence = [(4, 'X'), (0, 'O'), (8, 'X')] # Division by 0 error in indexInLine, diagonal fork
    # problem_sequence = [(0, 'X'), (1, 'O'), (7, 'X'), (3, 'O'), (5, 'X')] # Division by 0 error belongsToLine    
    # problem_sequence = [(1, 'X'), (4, 'O'), (8, 'X'), (5, 'O'), (3, 'X'), (2, 'O'), (6, 'X'), (0, 'O'), (7, 'X')] # fork logic fail
    # problem_sequence = [(7, 'X'), (4, 'O'), (3, 'X'), (2, 'O'), (6, 'X'), (0, 'O'), (8, 'X')] # fork fail
    # problem_sequence = [(0, 'X'), (4, 'O'), (5, 'X'), (6, 'O'), (2, 'X'), (1, 'O'), (8, 'X')] # minimax fail to see fork
    # gs.players[0].setDebug(problem_sequence)

    # while not gs.game_finished:
    #     gs.takeStep()
    #     gs.printGame()
    # gs.printGame()
    ################

    
    # problem_sequence = [(4, 'X'), (0, 'O'), (8, 'X')] # Division by 0 error in indexInLine, diagonal fork
    # gs.players[0].setDebug(problem_sequence)
    # gs.setGameSequence(problem_sequence)
    # gs.setCurrentPlayer(gs.players[1])

    # problem_sequence = [(0, 'X'), (1, 'O'), (7, 'X'), (3, 'O'), (5, 'X')] # Division by 0 error belongsToLine
    # gs.players[0].setDebug(problem_sequence)    
    # gs.setGameSequence([(7, 'X'), (4, 'O')]) #list index out of range
    # gs.setCurrentPlayer(gs.players[0])
    # gs.players[0].setDebug([(8, 'X')])


    # gs.players[0].setDebug(problem_sequence)    
    
    #gs.setGameSequence([(2, 'X')])
    #gs.setCurrentPlayer(gs.players[1])

#    gs.players[0].setDebug(problem_sequence)
#    gs.players[1].setDebug(problem_sequence)

    # while not gs.game_finished:
    #     gs.takeStep()
    #     gs.printGame()
    # ################
    
    # # Find lines
    # s = GameState(5)
    # s.test_lines()
    
    #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform()


from kivy.app import App
from kivy.uix.widget import Widget

class GameBoard(Widget):
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
    pass
    


class TicTacApp(App):
    def build(self):
        game = GameBoard()
        return game

if __name__ == '__main__':
    # run()
    TicTacApp().run()

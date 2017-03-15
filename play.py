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

#####################################################
# "lucky" Q-learning  vs Ideal and minimax TAble Stats

    # size = 3
    # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)      
        
    
    # ratios = fightDuels([QM, QM, QM, QM, QM, QMap()],
    #                     [ ['ideal', 'Qlearning'  ],
    #                       ['Qlearning', 'ideal'  ],
    #                       ['minimax', 'Qlearning'],
    #                       ['Qlearning', 'minimax'],
    #                       ['Qlearning', 'Qlearning'],
    #                       ['random', 'random'    ]], size, n_games = 100 )
 
    
    # cols = ["P1 win",  "draw", "P1 loss"]
    
    # rows = ('ideal vs lucky_Q', 'lucky_Q vs ideal',
    #         'minimax vs lucky_Q', 'lucky_Q vs minimax',
    #         'lucky_Q vs lucky_Q','random vs random')
    
    # table = pd.DataFrame(ratios, columns = cols, index = rows)
    # print table
    # table.to_csv("../lucky_table.csv")
    # print
    
    # ######
    # # lucky v Random
    # randos = fightDuels([QM, QM, QM, QMap()], [ ['random', 'Qlearning'],
    #                                             ['Qlearning', 'random'],
    #                                             ['Qlearning', 'Qlearning'],
    #                                             ['random', 'random' ]  ], size, n_games = 1000, p1ds = [2,3,3,2], p2ds = [3,2,3,2] )
    # cols = ["P1 win",  "draw", "P1 loss"]
    # rows = ('random vs lucky_Q',
    #         'lucky_Q vs random',
    #         'lucky_Q vs lucky_Q',            
    #         'random vs random')
    # table = pd.DataFrame(randos, columns = cols, index = rows)
    # print table
    # table.to_csv("../lucky_random_table.csv")
    
    # # # dd = pd.DataFrame(np.random.randn(10, 10)).applymap(abs)
    # # # dd = dd.cumsum()
    # # # print dd
    # # # #plt.figure()
    # # # dd.plot.bar(colormap='Greens')
    # # # parallel_coordinates(data, 'Name', colormap='gist_rainbow')

################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION


###############################################################
# Reproduce Lucky_Q, get lucky again
    # size = 3
    # ts = [70, 1000, 1000, 1000] 
    
    # QM = QMap(gamma=0.1, alpha=0.1) #Initialize QM with parameters found in faux gridsearch
    # # with open("../newlucky.pickle", 'rb') as f:
    # #     QM=pickle.load(f)
    
    # start = time() 
    # QM, tally, conv = playGames(setupGame(QMap(), size, ['random', 'random'],  learning=True), ts[0])   
    # # # player 2 learning against a random player 1
    # # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])   
    # # # Now player 1 learning against a random player 2
    # # QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])    
    # # # Have two agents learn against each other
    # # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])
    # print "Training time: " , time() - start 

    # duels = [ ['ideal', 'Qlearning'  ],
    #           ['Qlearning', 'ideal'  ],
    #           ['minimax', 'Qlearning'],
    #           ['Qlearning', 'minimax'],
    #           ['Qlearning', 'Qlearning'],
    #           ['random', 'Qlearning'],
    #           ['Qlearning', 'random'], 
    #           ['random','random'] ]
    
    # ##TEST IT
    # ratios = fightDuels([QM, QM, QM, QM, QM,QM, QM, QMap()], duels, size, n_games = 100 )
 
    # cols = ["P1 win",  "draw", "P1 loss"]
    
    # rows = ('ideal vs lucky_Q', 'lucky_Q vs ideal',
    #         'minimax vs lucky_Q', 'lucky_Q vs minimax',
    #         'lucky_Q vs lucky_Q',
    #         'random vs lucky_Q',
    #         'lucky_Q vs random',
    #         'random vs random')
    
    # table = pd.DataFrame(ratios, columns = cols, index = rows)
    # print table
    # table.plot.barh(colormap="Greens", stacked=True)
    # plt.show()
    # print
    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION    


    #########################################################################################################
    # Q-Learning Training  Q-Learning Training  Q-Learning Training  Q-Learning Training Q-Learning Training
    #########################################################################################################
    
    # #Seed Q with initial random games
    # size = 3    
    # #ts = [70, 1000, 1000, 2000]
    # ts = [70, 200, 200, 300]
    # start = time()    
    # # QM, tally, conv = playGames(setupGame(QMap(), size, ['random', 'miniQmax'],  learning=True, d1=3,d2=3), ts[0])
    # # QM, tally, conv = playGames(setupGame(QMap(), size, ['miniQmax', 'random'],  learning=True, d1=3,d2=3), ts[0])
    # # # player 2 learning against a random player 1
    # # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])
    
    # # # Now player 1 learning against a random player 2
    # # QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])
    
    # # # Have two agents learn against  each other
    # # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])

    # # print "Training time: " , time() - start  
    # # exploreQ(QM,1)
    
    # ###
    # #Using Multiprocess

    # # Seed Q with initial random games
    # start = time()
    # QM = multiTrain(setupGame(QMap(), size, ['random', 'random'], learning=True), runs=7, batch_size=10)

    # # player 2 learning against a random player 1
    # QM = multiTrain(setupGame(QM, size, ['random', 'Qlearning'], learning=True),  runs=20, batch_size=100)

    # # Now player 1 learning against a random player 2
    # QM = multiTrain(setupGame(QM, size, ['Qlearning', 'random'], learning=True), runs=20, batch_size=100)

    # # Have two agents learn against  each other
    # QM = multiTrain(setupGame(QM, size, ['Qlearning', 'Qlearning'], learning=True),runs=20, batch_size=200)
    # print "Training time: " , time() - start

    
    # # display "quality" table
    # tallies = []
    # lbls = [ ('P1 win', (True, False) ), ('P1 loss', (False, True) ), ('draw', (False, False) )]
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'ideal']), 10, check_convergence = False)
    # tallies.append([tally[l[1]] for l in lbls])
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'minimax']), 10, check_convergence = False)
    # tallies.append([tally[l[1]] for l in lbls])
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning']), 10, check_convergence = False)
    # tallies.append([tally[l[1]] for l in lbls])

    # quality_table = pd.DataFrame(tallies, columns=[l[0] for l in lbls],
    #                              index = ['Qlearning v ideal', 'Qlearning v minimax', 'Qlearning v Qlearning'])
    # print quality_table
    # print

    # with open("../newlucky.pickle", 'wb') as f:
    #     pickle.dump(QM, f, pickle.HIGHEST_PROTOCOL)
        
    # #######################
    # # MiniQmax stats table
    # with open("../newlucky.pickle", 'rb') as f:
    #     QM = pickle.load(f)
        
    # ratios = fightDuels([QM, QM], [ ['random', 'Qlearning'],
    #                                 ['Qlearning', 'random'] ], size, n_games = 100, p1ds = [2,3], p2ds = [3,2] )
    
    # ratios += fightDuels([QM, QM], [ ['random', 'miniQmax'],
    #                                 ['miniQmax', 'random'] ], size, n_games = 100, p1ds = [2,3], p2ds = [3,2] )    
    
    # ratios += fightDuels([QM, QM], [ ['Qlearning', 'miniQmax'],
    #                                  ['miniQmax', 'Qlearning'] ], size, n_games = 100, p1ds = [2,3], p2ds = [3,2] )

    # ratios += fightDuels([QM, QM], [ ['Qlearning', 'Qlearning'],
    #                                  ['random', 'random'] ], size, n_games = 100 )

    # ratios += fightDuels([QM, QM], [ ['Qlearning', 'minimax' ],
    #                                  ['minimax', 'Qlearning' ] ], size, n_games = 40,  p1ds = [2,3], p2ds = [3,2] )

    # ratios += fightDuels([QM, QM], [ ['miniQmax', 'minimax' ],
    #                                  ['minimax', 'miniQmax' ] ], size, n_games = 40,  p1ds = [2,3], p2ds = [3,2] )

    # # ratios += fightDuels([QM, QM], [ ['miniQmax', 'ideal'],
    # #                                  ['ideal', 'miniQmax'] ], size, n_games = 40, p1ds = [2,3], p2ds = [3,2] )
    
    # cols = ["P1 win",  "draw", "P1 loss"]
    # rows = ('random vs Qlearning',
    #         'Qlearning vs random',
            
    #         'random vs miniQmax',
    #         'miniQmax vs random',            
            
    #         'Qlearning vs miniQmax',
    #         'miniQmax vs Qlearn',
            
    #         'Qlearning vs Qlearning',
    #         'random vs random',
            
    #         'Qlearning vs minimax',
    #         'minimax vs Qlearning',
            
    #         'miniQmax vs minimax',
    #         'minimax vs miniQmax')
            
    #         # 'miniQmax vs ideal',
    #         # 'ideal vs miniQmax')

    # exploreQ(QM,2)

    # table = pd.DataFrame(ratios, columns = cols, index = rows)
    # print table
    # #table.plot.barh(stacked=True,colormap='Greens')
    # #plt.show()
    # print "total time: " , time() - start
    # table.to_csv("../justQs_lucky.csv")

    # ## Comparison with random
    # columns = ('Random vs miniQmax', 'miniQmax vs random', 'random vs Qlearning', 'Qlearning vs random')
    # ratios  = fightDuels([QM, QM, QM, QM],
    #                      [ ['random', 'miniQmax' ],
    #                        ['miniQmax', 'random' ],
    #                        ['random', 'Qlearning'],
    #                        ['Qlearning', 'random' ]], size, n_games = 80 , p1ds = [2,3,2,3], p2ds = [3,2,3,2] )
    # ratios = np.transpose(ratios)
    # graphStats(columns, ratios, 'MiniQmax vs Random {}x{}'.format(size,size))

    #####
    #save QM
    # with open("../mulit3x3_600.pickle", 'wb') as f:
    #     QM = pickle.dump(QM, f,  pickle.HIGHEST_PROTOCOL)

        
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION

##################################################################

    ###################################
    # Faux grid search for alpha gamma
    ###################################
    
    #Seed Q with initial random games
    # params = np.linspace(0.1, 0.9, 6)
    # #ts = [70, 200, 200, 300]
    # ts = [70, 1000, 1000, 1000]
    # start = time()
    # for alp in params:
    #     for gam in params:
    #         QM = QMap(gamma = gam, alpha=alp)

    #         QM, tally, conv = playGames(setupGame(QM, size, ['random', 'random'],  learning=True), ts[0])

    #         # player 2 learning against a random player 1
    #         QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])

    #         # Now player 1 learning against a random player 2
    #         QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])

    #         # Have two agents learn against  each other
    #         QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])

    #         ratios = fightDuels([QM, QM, QM, QM], [ ['Qlearning', 'Qlearning'],
    #                                                 ['Qlearning', 'random' ],
    #                                                 ['random', 'Qlearning' ],
    #                                                 ['random', 'random'    ] ], size, 100)
    #         cols = ["P1 win", "draw", "P1 loss"]
    #         table = pd.DataFrame(ratios,
    #                              index = ['Qlearning v Qlearning',
    #                                       'Qlearning v random',
    #                                       'random v Qlearning',
    #                                       'random v random'],  columns=cols,)
    #         print "ALPHA: ", alp, "GAMMA: ", gam
    #         print table

    #         tallies = []
    #         lbls = [ ('P1 win', (True, False) ), ('P1 loss', (False, True) ), ('draw', (False, False) )]
    #         QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'ideal']), 30)#, check_convergence = False)
    #         tallies.append([tally[l[1]] for l in lbls])
            
    #         QM, tally, conv = playGames(setupGame(QM, size, ['ideal','Qlearning']), 30)#, check_convergence = False)
    #         tallies.append([tally[l[1]] for l in lbls])

    #         QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'minimax']), 30)#, check_convergence = False)
    #         tallies.append([tally[l[1]] for l in lbls])

    #         QM, tally, conv = playGames(setupGame(QM, size, ['minimax', 'Qlearning']), 30)#, check_convergence = False)
    #         tallies.append([tally[l[1]] for l in lbls])

    #         QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning']), 30)#, check_convergence = False)
    #         tallies.append([tally[l[1]] for l in lbls])

    #         quality_table = pd.DataFrame(tallies, columns=[l[0] for l in lbls],
    #                                      index = ['Qlearning v ideal',
    #                                               'ideal v Qlearning',
    #                                               'Qlearning v minimax',
    #                                               'minimax v Qlearning',
    #                                               'Qlearning v Qlearning'])
                                      
    #         print "ALPHA: ", alp, "GAMMA: ", gam
    #         print quality_table
    #         print
            
    # print "Training time: " , time() - start
                
    # # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    # #     QM = pickle.load(f)

    # ##### Explore Q #####
    # exploreQ(QM,2)

        
    # with open("../mQm_3x3.pickle", 'wb') as f:
    #     pickle.dump([ts, QM], f,  pickle.HIGHEST_PROTOCOL)

    # # with open("../mQm_3x3.pickle", 'rb') as f:
    # #     #lucky_Q = pickle.load(f)
    # #     QM = pickle.load(f)
    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION

    ##################
    # Breed experiment
    size = 3 
    # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)

        
    # lucky2 = breed(QM, QMap(), size, 1000)

    
    ##### Explore Q #####
    # Q = QM.Q
    # M = max(len(seq) for seq in Q.keys())
    # for k in range(1,M):
    #     print "Explored Moves at step", k
    #     explored = (moves for moves in Q if len(moves) == k)
    #     for seq in explored:
    #         print seq, Q[seq]
    #     print


    # offspring = lucky2
    # QM = None
    # rwin = 0
    # gs = setupGame(offspring, size, ['Qlearning', 'random'])
    # bar = min( getRatios(gs,100)[2] for k in range(3) )

    # for gen in range(3):
    #     while rwin <=  bar:
    #         QM = breed(offspring, QMap(), size, 1000)
    #         gs = setupGame(QM, size, ['Qlearning', 'random'])
    #         rwin = getRatios(gs,100)[2]

    #     offspring = QM

    # gs = setupGame(offspring, size, ['Qlearning', 'random'])
    # print getRatios(gs,100)
    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION
#####################################################

# "lucky" Q-learning  vs Ideal and minimax GRaphs

    # #####################
    # size = 3
    # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)
        
    # #QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning','minimax']), 1)
        
    # #############################
    # # Q-learning vs Ideal stats 
    # columns  = ('Ideal vs lucky_Q', 'lucky_Q vs Ideal', 'random vs Ideal', 'Ideal vs random')
    
    # ratios = fightDuels([QM, QM, QMap(), QMap()], [ ['ideal', 'Qlearning'],
    #                                                 ['Qlearning', 'ideal'],
    #                                                 ['random', 'ideal'   ],
    #                                                 ['ideal', 'random' ] ], size, n_games = 100, p1ds = [2,3,2,2], p2ds = [3,2,2,2] )
    
    # ratios = np.transpose(ratios)

    # graphStats(columns, ratios, 'lucky-Q vs Ideal {}x{}'.format(size,size))

    # ################################
    # # Q-learnin vs Minimax stats 
    # columns  = ('Minimax vs lucky_Q', 'lucky_Q vs Minimax', 'random vs Minimax', 'Minimax vs random')
    
    # ratios = fightDuels([QM, QM, QMap(), QMap()],[ ['minimax', 'Qlearning'],
    #                                                ['Qlearning', 'minimax'],
    #                                                ['random', 'minimax'],
    #                                                ['minimax', 'random']  ], size, n_games = 20, p1ds = [2,3,2,2], p2ds = [3,2,2,2] )
    # ratios = np.transpose(ratios)

    # graphStats(columns, ratios, 'lucky-Q vs Minimax {}x{}'.format(size,size))

    # ################################
    # # Q-learn vs Random stats 
    # columns  = ('Random vs Qlearning',  'Qlearning vs Random', 'Random vs Random', '"Perfect" random')
    
    # duels = fightDuels([QM, QMap(), QMap()], [ ['random', 'Qlearning'],
    #                                            ['Qlearning', 'random'],
    #                                            ['random', 'random' ]  ], size, n_games = 100, p1ds = [2,3,2], p2ds = [3,2,2] )
    # duels.append([91.0/138, 3.0/138, 44.0/138 ])
    # ratios = np.transpose(duels)
    
    # graphStats(columns, ratios, 'lucky-Q/Random Comparison {}x{}'.format(size,size))

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

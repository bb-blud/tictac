from time import time
from collections import deque
import pickle

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

from game_board import GameBoard
from game_state import Player, GameState, QMap
from strateegery import Strateegery


class LearningPlayer(Player):
    def __init__(self, mark, game_state, policy, depth=2):
        super(LearningPlayer, self).__init__(mark, game_state)
        self.policy = policy
        self.strategies  = Strateegery(self.game_state)
        self.depth = depth
        ##
        self.inner_Q = QMap()
        self.use_inner_Q = False
        
    def makeMove(self):
        move = {
            'random'   : self.strategies.randomMove,
            'ideal'    : self.strategies.ideal,
            'minimax'  : self.strategies.minimaxMove,                        
            'Qlearning': self.strategies.Qlearning,
            'miniQmax' : self.strategies.minimaxMove,
            
            'debug'    : self.debug}[self.policy]
        
        if self.policy in ['minimax', 'miniQmax']:
            return move(self, self.depth)

        return move(self)
    
    def setInnerQ(self, QM):
        self.use_inner_Q = True
        self.inner_Q = QM

    
    ########## Player for debugging ##########
    def setDebug(self, sequence):
        from collections import deque
        self.inDebug = True
        self.problem_sequence = sequence
        self.Xmoves = deque([move for move in self.problem_sequence if move[1] == 'X'])
        self.Omoves = deque([move for move in self.problem_sequence if move[1] == 'O'])
        
    def debug(self, player):
        self.strategies.ideal(self)
        if self.inDebug:
            if self.mark == 'X':
                return self.Xmoves.popleft()
            if self.mark == 'O':
                return self.Omoves.popleft()
        return
#########################################################################################

def setupGame(globalQM, game_size, policies, learning=False, marks=['X','O'], p1QM=None, p2QM=None, d1=2, d2=2):
    gs = GameState(game_size,  learning)
    gs.setQMap(globalQM)

    player1 = LearningPlayer(marks[0], gs, policies[0], d1)
    if p1QM is not None:
        player1.setInnerQ(p1QM)
        
    player2 = LearningPlayer(marks[1], gs, policies[1], d2)
    if p2QM is not None:
        player2.setInnerQ(p2QM)

    gs.setPlayers(player1, player2)

    return gs
def getRatios(game_state, n_games):
    QM, tally, conv = playGames(game_state, n_games)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    return [ts[0]/s, ts[2]/s, ts[1]/s]

def fightDuels(QMs, duels, size, n_games, **kwargs):
    ratios = []

    p1depths = kwargs.get('p1ds', [2 for _ in range(len(duels))])
    p2depths = kwargs.get('p2ds', [2 for _ in range(len(duels))])
        
    for i, duel in enumerate(duels):
        ratios.append(getRatios(setupGame(QMs[i], size, duel, d1 = p1depths[i], d2 = p2depths[i] ),  n_games) )
        
    return ratios

def playGames(game_state, n_games, check_convergence=True,  debug=False):
    ####### Tally ########
    tally = { (True, False) : 0, (False, True) : 0, (False, False) : 0 }
    is_converging = False

    ##### Initialize #####
    gs = game_state

    #### Crude convergence test ####
    repeats = deque()
    for game in range(8):

        while not gs.game_finished:
            gs.takeStep()
            if debug:
                gs.printGame()
        repeats.append(gs.game_sequence)
        gs.resetGame()

    ######### Play Games #########
    bads = set() # debug
    
    current = []
    for game in range(n_games):

        while not gs.game_finished:
            gs.takeStep()
            if debug:
                gs.printGame()
        if debug:
            gs.printGame()
            print

        tally[ (gs.players[0].is_winner, gs.players[1].is_winner) ] += 1

        if debug:
            for p in gs.players:
                print p.mark, "is winner: ", p.is_winner
            print tally

        ## Exit if converging ##
        current = gs.game_sequence
        repeats.append(current)
        repeats.popleft()

        if debug:
            for r in repeats:
                print r
                print "**"
            print

        if False not in (current == g for g in repeats) and check_convergence:
            print "CONVERGENCE ON GAME NUMBER: ", game, [p.policy for p in gs.players]
            is_converging = True
            break
        ## ##  ## ##

        # if debug:
        #     if gs.players[0].is_winner:
        #         bads.add(tuple(gs.game_sequence))

        gs.resetGame()
        
        # for b in bads:
        #     print b
    
    return gs.QM, tally, is_converging

def trainQ(game_state, runs, batch_size):
    
    ## Support function plays batch_size amount of games ##
    def playBatch(ns, game_state, batch_size):
        gs = game_state
        for game in range(batch_size):
            gs.setQMap(ns.QM)
            while not gs.game_finished:
                gs.takeStep()
            ns.QM = gs.QM
            gs.resetGame()     
    ##   ##   ##   ##    ##   ##   ##   ##  
   
    import multiprocessing
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.QM = game_state.QM
    
    jobs = []
    for _ in range(runs):
        p = multiprocessing.Process(target=playBatch, args=(ns, game_state, batch_size) )
        jobs.append(p)
        p.start()
        
    for p in jobs:
        p.join()

    return ns.QM

def graphStats(columns, data, strategy): #Based on http://matplotlib.org/examples/pylab_examples/table_demo.html
    rows = ['win', 'draw', 'loss']
    values = np.arange(0, 1, .1)
    value_increment = 2

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))[::-1]
    n_rows = len(data)

    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.array([0.0] * len(columns))

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data[row]
        cell_text.append(['%.4f' % x for x in data[row]])

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom')

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    plt.ylabel("win/draw/loss fraction".format(value_increment))
    plt.yticks(values * value_increment, ['%.2f' % (val*value_increment) for val in values])
    plt.xticks([])
    plt.title('Ratio Comparison ' + strategy)

    plt.show()

def printTally(game_state, n_games):
    
    QM, tally, conv = playGames(game_state, n_games)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    print "{} : {} : {}".format(ts[1]/s, ts[2]/s, ts[0]/s)


def breed(QM1, QM2, size, n_cycles):
    game_state = setupGame(QMap(), size, ['Qlearning', 'Qlearning'], learning=True, p1QM=QM1)    
    QM, tally, conv = playGames(game_state, n_cycles)

    game_state = setupGame(QM, size, ['Qlearning', 'Qlearning'], learning=True, p2QM=QM2)
    QM, tally, conv = playGames(game_state, n_cycles)

    return QM

def exploreQ(QM,d):
    Q = QM.Q
    M = max(len(seq) for seq in Q.keys())
    for k in range(1,M/d):
        print "Explored Moves at step", k
        explored = sorted( [(seq , Q[seq]) for seq in Q if len(seq) == k], key=lambda t:t[1] )
        
        for seq, val  in explored:
            print seq, val
        print

        
def run():
    size = 3
    ###############################################################
    # Approximate baseline win/draw/loss ratios using random policy
    # size = 3
    # columns  = ('"Perfect" Random', 'random vs random')
    
    # # TicTacToe X-O win/loss/draw ratio: 91:44:3 or 0.6594 : 0.31884 : 0.0217, source wikipedia
    # ratios = [[91.0/138, 3.0/138, 44.0/138 ]]
    # ratios += fightDuels([QMap()], [['random', 'random']], size, n_games = 10000)

    # ratios = np.transpose(ratios)
    # graphStats(columns, ratios, 'random 3x3')

    # ##
    # size = 4
    # columns = ('Trial 1', 'Trial 2')
    # ratios = np.transpose(fightDuels([QMap(), QMap()], [ ['random','random'], ['random','random'] ], size, 10000))

    # graphStats(columns, ratios, 'Approximate baseline win/draw/loss ratios 4x4')

    # ## 
    # size = 5
    # columns = ('Trial 1', 'Trial 2')
    # ratios = np.transpose(fightDuels([QMap(), QMap()], [ ['random','random'], ['random','random'] ], size, 10000))

    # graphStats(columns, ratios, 'Approximate baseline win/draw/loss ratios 5x5')

    # ##
    # size = 6
    # columns = ('Trial 1', 'Trial 2')
    # ratios = np.transpose(fightDuels([QMap(), QMap()], [ ['random','random'], ['random','random'] ], size, 10000))

    # graphStats(columns, ratios, 'Approximate baseline win/draw/loss ratios 6x6')
    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION


    # # #########################
    # Ideal policy stats 3x3
    # columns  = ('P1 actual counts', 'Ideal as player1', 'P2 actual counts', 'Ideal as player 2')
    # start = time()
    # # Perfect X player 3x3 win/draw/loss ratio 91:3:0 or 0.9681 : 0.0319 : 0  
    # ratios = [[ 91./94, 3.0/94, 0/94]]
    # ratios += fightDuels([QMap()], [['ideal', 'random']], size, n_games = 1000)

    # # Perfect O player 3x3 win/draw/loss ratio 0:3:44 or 0.9363 :0.0638 : 0
    # ratios.append([ 44./47, 3.0/47, 0.0/47 ])
    
    # # This guy needs to be reversed because we are interested in player2 wins
    # ratios.append(fightDuels([QMap()], [['random', 'ideal']], size, n_games = 1000)[0][::-1] )

    # start = time()
    # ratios = np.transpose(ratios)
    # graphStats(columns, ratios, 'Ideal policy against random 3x3') 
    
    ###########################
    # Minimax policy stats 3x3
    # columns  = ('P1 actual counts', 'Minimax as player 1', 'P2 actual counts', 'Minimax as player 2')
    # start = time()
    # # Perfect X player 3x3 win/draw/loss ratio 91:3:0 or 0.9681 : 0.0319 : 0  
    # ratios  = [[ 91./94, 3.0/94, 0./94]]
    # ratios += fightDuels([QMap()], [['minimax', 'random']], size, n_games = 500)
         
    # # Perfect O player 3x3 win/draw/loss ratio 0:3:44 or 0.9363 :0.0638 : 0
    # ratios.append([ 44./47, 3.0/47, 0/47 ])

    # # This guy needs to be reversed because we are interested in player2 wins
    # ratios.append(fightDuels([QMap()], [['random', 'minimax']], size, n_games = 500)[0][::-1])
    
    # print time() - start        
    # ratios = np.transpose(ratios)
    # graphStats(columns, ratios, 'Minimax policy against random 3x3')
    
    # ###########################
    # Minimax vs Ideal
    # print "Start minimax vs ideal"
    # size = 3
    # columns  = ('Minimax vs Ideal', 'Ideal vs Minimax')
    # start = time()
    # ratios = fightDuels([QMap(), QMap()], [['minimax', 'ideal'],
    #                                        ['ideal', 'minimax'] ], size, n_games = 3, p1qds = [5 , 2], p2ds = [2, 5])
    
    # print time() - start        
    # ratios = np.transpose(ratios)
    # graphStats(columns, ratios, 'Minimax vs Ideal comparison 3x3')

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
    size = 3
    ######################
    # Q-Learning Training
    #Seed Q with initial random games

    #ts = [70, 1000, 1000, 2000]
    # ts = [70, 200, 200, 300]
    # start = time()    
    # QM, tally, conv = playGames(setupGame(QMap(), size, ['random', 'random'],  learning=True), ts[0])
    
    # # player 2 learning against a random player 1
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])
    
    # # Now player 1 learning against a random player 2
    # QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])
    
    # # Have two agents learn against  each other
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])
    # print "Training time: " , time() - start 

    #####################
    # Using Multiprocess

    # Seed Q with initial random games
    # start = time()
    # QM = trainQ(setupGame(QMap(), size, ['random', 'random'], learning=True), runs=7, batch_size=10)

    # # player 2 learning against a random player 1
    # QM = trainQ(setupGame(QM, size, ['random', 'Qlearning'], learning=True),  runs=20, batch_size=100)

    # # Now player 1 learning against a random player 2
    # QM = trainQ(setupGame(QM, size, ['Qlearning', 'random'], learning=True), runs=20, batch_size=100)

    # # Have two agents learn against  each other
    # QM = trainQ(setupGame(QM, size, ['Qlearning', 'Qlearning'], learning=True),runs=20, batch_size=200)
    # print "Training time: " , time() - start

    ########################
    # display "quality" table
    tallies = []
    lbls = [ ('P1 win', (True, False) ), ('P1 loss', (False, True) ), ('draw', (False, False) )]
    QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'ideal']), 10, check_convergence = False)
    tallies.append([tally[l[1]] for l in lbls])

    QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'minimax']), 10, check_convergence = False)
    tallies.append([tally[l[1]] for l in lbls])

    QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning']), 10, check_convergence = False)
    tallies.append([tally[l[1]] for l in lbls])

    quality_table = pd.DataFrame(tallies, columns=[l[0] for l in lbls],
                                 index = ['Qlearning v ideal', 'Qlearning v minimax', 'Qlearning v Qlearning'])
    print quality_table
    print

    #######################
    # MiniQmax stats table

    # ratios = fightDuels([QM, QM], [ ['random', 'miniQmax'],
    #                                  ['miniQmax', 'random'] ], size, n_games = 100, p1ds = [2,3], p2ds = [3,2] )
    
    # ratios += fightDuels([QM, QM], [ ['Qlearning', 'miniQmax'],
    #                                  ['miniQmax', 'Qlearning'] ], size, n_games = 100, p1ds = [2,3], p2ds = [3,2] )

    # ratios += fightDuels([QM, QM], [ ['Qlearning', 'Qlearning'],
    #                                  ['random', 'random'] ], size, n_games = 500 )

    # ratios += fightDuels([QM, QM], [ ['miniQmax', 'minimax' ],
    #                                  ['minimax', 'miniQmax' ] ], size, n_games = 40,  p1ds = [2,3], p2ds = [3,2] )

    # # ratios += fightDuels([QM, QM], [ ['miniQmax', 'ideal'],
    # #                                  ['ideal', 'miniQmax'] ], size, n_games = 40, p1ds = [2,3], p2ds = [3,2] )
    
    # cols = ["P1 win",  "draw", "P1 loss"]
    # rows = ('random vs miniQmax',
    #         'miniQmax vs random',
            
    #         'Qlearning vs miniQmax',
    #         'miniQmax vs Qlearn',
            
    #         'Qlearning vs Qlearning',
    #         'random vs random',
            
    #         'miniQmax vs minimax',
    #         'minimax vs miniQmax',)
            
    #         # 'miniQmax vs ideal',
    #         # 'ideal vs miniQmax')

    # exploreQ(QM,2)

    # table = pd.DataFrame(ratios, columns = cols, index = rows)
    # print table
    # table.plot.barh(stacked=True,colormap='Greens')
    # plt.show()
    # print "total time: " , time() - start

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

  
##################### ##################### ##################### #####################
# Revenge of Lucky_Q Revenge of Lucky_Q Revenge of Lucky_Q Revenge of Lucky_Q 

    # # print "Revenge of Lucky"
    # size = 3
    # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)

    # ratios  = fightDuels([QM, QM], [ ['Qlearning', 'miniQmax' ],
    #                                  ['miniQmax', 'Qlearning'] ], size, n_games = 10, p1ds = [2,3], p2ds = [3,2] )[::-1]

    # ratios += fightDuels([QM, QM], [ ['minimax', 'miniQmax' ],
    #                                  ['miniQmax', 'minimax' ] ], size, n_games = 10,  p1ds = [2,3], p2ds = [3,2] )[::-1]

    # rows  = ('Qlearning vs miniQmax', 'miniQmax vs Qlearn', 'minimax vs miniQmax', 'miniQmax vs minimax')
    # cols = ["P1 win", "draw","P1 loss"]
    # table = pd.DataFrame(ratios,columns = cols, index = rows)
    # print table 

    # ## Comparison with random
    # columns = ('Random vs miniQmax', 'miniQmax vs random')
    # ratios  = fightDuels([QM, QM], [ ['random', 'miniQmax' ],
    #                                  ['miniQmax', 'random' ] ], size, n_games = 100 , p1ds = [2,3], p2ds = [3,2] )
    # ratios = np.transpose(ratios)
    # graphStats(columns, ratios, 'MiniQmax vs Random {}x{}'.format(size,size))

    
################################################################################## ###########################################
# END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION END SECTION

    ###################################
    # Faux grid search for alpha gamma
    #Seed Q with initial random games
    params = np.linspace(0.1, 0.9, 6)
    ts = [70, 200, 200, 300]
    start = time()
    for alp in params:
        for gam in params:
            QM = QMap(gamma = gam, alpha=alp)

            QM, tally, conv = playGames(setupGame(QM, size, ['random', 'random'],  learning=True), ts[0])

            # player 2 learning against a random player 1
            QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])

            # Now player 1 learning against a random player 2
            QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])

            # Have two agents learn against  each other
            QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])


            tallies = []
            lbls = [ ('P1 win', (True, False) ), ('P1 loss', (False, True) ), ('draw', (False, False) )]
            QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'ideal']), 30)#, check_convergence = False)
            tallies.append([tally[l[1]] for l in lbls])
            
            QM, tally, conv = playGames(setupGame(QM, size, ['ideal','Qlearning']), 30)#, check_convergence = False)
            tallies.append([tally[l[1]] for l in lbls])

            QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'minimax']), 30)#, check_convergence = False)
            tallies.append([tally[l[1]] for l in lbls])

            QM, tally, conv = playGames(setupGame(QM, size, ['minimax', 'Qlearning']), 30)#, check_convergence = False)
            tallies.append([tally[l[1]] for l in lbls])

            QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning']), 30)#, check_convergence = False)
            tallies.append([tally[l[1]] for l in lbls])

            quality_table = pd.DataFrame(tallies, columns=[l[0] for l in lbls],
                                         index = ['Qlearning v ideal',
                                                  'ideal v Qlearning',
                                                  'Qlearning v minimax',
                                                  'minimax v Qlearning',
                                                  'Qlearning v Qlearning'])
                                      
            print "ALPHA: ", alp, "GAMMA: ", gam
            print quality_table
            print
            
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
        




    




    ##################
    # Breed experiment
    size = 3 
    # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)

        
    # lucky2 = breed(QM, QMap(), size, 1000)

    # columns = ('lucky2 vs random', 'random vs random')
    # ratios = np.transpose(fightDuels([lucky2, QMap()], [ ['Qlearning', 'random'],
    #                                              ['random', 'random'] ], size, 100 ) )
    # graphStats( columns , ratios, 'lucky2 vs random')
    # gs = setupGame(lucky2, size, ['Qlearning', 'random'])
    # ratios = np.transpose([getRatios(gs, 1000)])
    # graphStats( , ratios, 'lucky2 vs random')
    
    # columns  = ('Random vs Qlearning',  'Qlearning vs Random', 'Random vs Random', '"Perfect" random')
    
    # ratios = fightDuels([lucky_Q, QMap(), QMap()], [ ['random', 'Qlearning'],
    #                                            ['Qlearning', 'random'],
    #                                            ['random', 'random' ]  ], size, n_games = 100)
    
    # ratios.append([44.0/138, 3.0/138, 91.0/138 ])
    # ratios = np.transpose(ratios)

    # graphStats(columns, ratios, 'Lucky 3x3 Q  vs Random {}x{}'.format(size,size))
    
    # columns  = ('Random vs Qlearning',  'Qlearning vs Random', 'Random vs Random', '"Perfect" random')
    
    # ratios = fightDuels([lucky2, QMap(), QMap()], [ ['random', 'Qlearning'],
    #                                            ['Qlearning', 'random'],
    #                                            ['random', 'random' ]  ], size, n_games = 100)
    
    # ratios.append([44.0/138, 3.0/138, 91.0/138 ])
    # ratios = np.transpose(ratios)

    # graphStats(columns, ratios, 'Lucky2 3x3 Q  vs Random {}x{}'.format(size,size))
    
    ##### Explore Q #####
    # Q = QM.Q
    # M = max(len(seq) for seq in Q.keys())
    # for k in range(1,M):
    #     print "Explored Moves at step", k
    #     explored = (moves for moves in Q if len(moves) == k)
    #     for seq in explored:
    #         print seq, Q[seq]
    #     print

    ####### Store/Load QMap #########
    # with open(, 'wb') as f:
    #     pickle.dump(QM, f, pickle.HIGHEST_PROTOCOL)
    # with open(, 'rb') as f:
    #     QM = pickle.load(f)

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


    
##############################################################
#       TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS
##############################################################
    # # Debug game
    # cummulativeQ = QMap()    
    # gs = GameState(3)
    # gs.setQMap(QMap())
    # gs.setPlayers(LearningPlayer('X', gs, 'debug'), LearningPlayer('O', gs, 'minimax')) 
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
    
    # #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform()
    
if __name__ == '__main__':
    run()

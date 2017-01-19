from time import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import pickle

from game_board import GameBoard
from game_state import Player, GameState, QMap
from strateegery import Strateegery


class LearningPlayer(Player):
    def __init__(self, mark, game_state, policy):
        super(LearningPlayer, self).__init__(mark, game_state)
        self.policy = policy
        self.strategies  = Strateegery(self.game_state)
        ##
        self.inner_Q = QMap()
        self.use_inner_Q = False
        
    def makeMove(self):
        move = {
            'random'   : self.strategies.randomMove,
            'minimax'  : self.strategies.minimaxMove,
            'ideal'    : self.strategies.ideal,
            'Qlearning': self.strategies.Qlearning,
            'debug'    : self.debug}[self.policy](self)
        return move
    
    def setInnerQ(QM):
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

def setupGame(globalQM, game_size, policies, learning=False, marks=['X','O'], p1QM=None, p2QM=None):
    gs = GameState(game_size,  learning)
    gs.setQMap(globalQM)
    
    player1 = LearningPlayer(marks[0], gs, policies[0])
    if p1QM is not None:
        player1.setInnerQ(p1QM)
        
    player2 = LearningPlayer(marks[1], gs, policies[1])
    if p2QM is not None:
        player2.setInnerQ(p2QM)

    gs.setPlayers(player1, player2)

    return gs

def playGames(game_state, n_games, check_convergence=True,  debug=False):
    ####### Tally ########
    tally = { (True, False) : 0, (False, True) : 0, (False, False) : 0 }
    is_converging = False
    
    ##### Initialize #####
    gs = game_state

    #### Crude convergence test ####
    repeats = deque()
    for game in range(5):

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
            print "CONVERGENCE ON GAME NUMBER: ", game
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

def printTally(game_state, n_games):
    
    QM, tally = playGames(game_state, n_games)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    print "{} : {} : {}".format(ts[0]/s, ts[2]/s, ts[1]/s)


def graphStats(columns, data, strategy): #Based on http://matplotlib.org/examples/pylab_examples/table_demo.html
    rows = ['win', 'draw', 'loss']
    values = np.arange(0, 1, .1)
    value_increment = 2

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
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

    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]
    cell_text.reverse()

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


def getRatios(game_state, n_games):
    QM, tally, conv = playGames(game_state, n_games)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    return [ts[1]/s, ts[2]/s, ts[0]/s]

def fightDuels(QMs, duels, size, n_games):
    ratios = []
    for i, duel in enumerate(duels):
        ratios.append(getRatios(setupGame(QMs[i], size, duel), n_games))
    return ratios

    
def run():
    size = 3

    ###########################
    # Minimax policy stats 3x3
    # duels  = ('P1 actual counts', 'Minimax as player 1', 'P2 actual counts', 'Minimax as player 2')
    # start = time()
    # ratios = np.array(
    #     # Perfect X player 3x3 win/draw/loss ratio 91:3:0 or 0.9681 : 0.0319 : 0  
    #     [[ 0/94, 3.0/94, 91.0/94],
              
    #      getRatios(setupGame(QMap(), size, ['minimax', 'random']), n_games = 500),
         
    #     # Perfect O player 3x3 win/draw/loss ratio 0:3:44 or 0.9363 :0.0638 : 0
    #      [ 0/47, 3.0/47, 44.0/47 ],

    #     # This guy needs to be reversed because we are interested in player2 wins
    #      getRatios(setupGame(QMap(), size, ['random', 'minimax']), n_games = 500)[::-1] ])
    
    # ratios = np.transpose(ratios)
    
    # print time() - start    
    # graphStats(duels, ratios, 'Minimax policy against random 3x3')

    
    # # #########################
    # Ideal policy stats 3x3
    # duels  = ('P1 actual counts', 'Ideal as player1', 'P2 actual counts', 'Ideal as player 2')
    
    # ratios = np.array(
    #     # Perfect X player 3x3 win/draw/loss ratio 91:3:0 or 0.9681 : 0.0319 : 0  
    #     [[ 0/94, 3.0/94, 91.0/94],
              
    #      getRatios(setupGame(QMap(), size, ['ideal', 'random']), n_games = 1000),
         
    #      # Perfect O player 3x3 win/draw/loss ratio 0:3:44 or 0.9363 :0.0638 : 0
    #      [ 0/47, 3.0/47, 44.0/47 ],

    #      # This guy needs to be reversed because we are interested in player2 wins
    #      getRatios(setupGame(QMap(), size, ['random', 'ideal']), n_games = 1000)[::-1] ])
         
    
    # ratios = np.transpose(ratios)

    # graphStats(duels, ratios, 'Ideal policy against random 3x3')
    
    ###############################################################
    # Approximate baseline win/draw/loss ratios using random policy
    # size = 3
    # columns  = ('"Perfect" Random', 'random vs random')

    # ratios = np.array(
    #     # TicTacToe X-O win/loss/draw ratio: 91:44:3 or 0.6594 : 0.31884 : 0.0217, source wikipedia
    #     [[44.0/138, 3.0/138, 91.0/138 ],
              
    #      getRatios(setupGame(QMap(), size, ['random', 'random']), n_games = 10000)
    #     ]) 
    # ratios = np.transpose(ratios)

    # graphStats(duels, ratios, 'random 3x3')

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
    

    
    #################################################################################################

    
    ######################
    # Q-Learning Training
    # Seed Q with initial random games
    # QM, tally, conv = playGames(setupGame(QMap(), size, ['random', 'random'],  learning=True), 70)
    
    # # player 2 learning against a random player 1
    # QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],    learning=True), 1000)
    
    # # Now player 1 learning against a random player 2
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True),  1000)
    
    # # Have two agents learn against  each other
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), 1000)
    
    

    # Using Multiprocess
    # Seed Q with initial random games
    # start = time()
    # QM = trainQ(setupGame(QMap(), size, ['random', 'random'], learning=True), runs=7, batch_size=100)
    
    # # player 2 learning against a random player 1
    # QM = trainQ(setupGame(QM, size, ['random', 'Qlearning'], learning=True),  runs=10, batch_size=100)
    
    # # Now player 1 learning against a random player 2
    # QM = trainQ(setupGame(QM, size, ['Qlearning', 'random'], learning=True), runs=10, batch_size=100)
    
    # # Have two agents learn against each other
    # QM = trainQ(setupGame(QM, size, ['Qlearning', 'Qlearning'], learning=True), runs=10, batch_size=300)
    # print time() - start

    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'ideal']), 30, check_convergence = False)
    # print tally

    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'minimax']), 30, check_convergence = False)
    # print tally

    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning']), 30, check_convergence = False)
    # print tally


    #####################
    # size = 4
    # with open("../anti_minimax_4x4_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)
        
    # QM, tally, conv = playGames(QM, size, ['Qlearning','minimax'], 1, debug=True)
        
    # #############################
    # # Q-learning vs Ideal stats 
    # columns  = ('Ideal vs Qlearning', 'Ideal vs random', 'random vs Ideal', 'Qlearning vs Ideal')
    
    # ratios = np.transpose(fightDuels([QM, QMap(), QMap(), QM], [ ['ideal', 'Qlearning'],
    #                                                              ['ideal', 'random'   ],
    #                                                              ['random', 'ideal'   ],
    #                                                              ['Qlearning', 'ideal'] ], size, n_games = 100) )
    
    # ratios = np.transpose(ratios)

    # graphStats(columns, ratios, 'Q-learning vs Ideal {}x{}'.format(size,size))


    # # ################################
    # # # Q-learnin vs Minimax stats 
    # columns  = ('Minimax vs Qlearning', 'Minimax vs random', 'random vs Minimax', 'Qlearning vs Minimax')
    
    # ratios = np.transpose(fightDuels([QM, QMap(), QMap(), QM],[ ['minimax', 'Qlearning'],
    #                                                             ['minimax', 'random'],
    #                                                             ['random', 'minimax'],
    #                                                             ['Qlearning', 'minimax'] ], size, n_games = 20) )
    
    # ratios = np.transpose(ratios)

    # graphStats(duels, ratios, 'Q-learning vs Minimax {}x{}'.format(size,size))

    # ################################
    # # Q-learn vs Random stats 
    # columns  = ('Random vs Qlearning',  'Qlearning vs Random', 'Random vs Random', '"Perfect" random')
    
    # duels = fightDuels([QM, QMap(), QMap()], [ ['random', 'Qlearning'],
    #                                            ['Qlearning', 'random'],
    #                                            ['random', 'random' ]  ], size, n_games = 100)
    # duels.append([44.0/138, 3.0/138, 91.0/138 ])
    # ratios = np.transpose(duels)
    

    ###########
    # Lucky QM

    with open("../lucky_3x3_Q.pickle", 'rb') as f:
        QM = pickle.load(f)
    
    columns  = ('Random vs Qlearning',  'Qlearning vs Random', 'Random vs Random', '"Perfect" random')
    
    duels = fightDuels([QM, QMap(), QMap()], [ ['random', 'Qlearning'],
                                               ['Qlearning', 'random'],
                                               ['random', 'random' ]  ], size, n_games = 100)
    duels.append([44.0/138, 3.0/138, 91.0/138 ])
    ratios = np.transpose(duels)

    graphStats(columns, ratios, 'Lucky 3x3 Q  vs Random {}x{}'.format(size,size))
    
    ##### Explore Q #####
    # Q = QM.getQ()
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

import sys
sys.path.append("../")

from time import time
import pandas as pd
from utilities import *

def run():
    
    ###################################
    # Faux grid search for alpha gamma
    ###################################

    size = 3
    
    #Seed Q with initial random games
    params = np.linspace(0.1, 0.9, 6)
    #ts = [70, 200, 200, 300]
    ts = [70, 1000, 1000, 1000]
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

            ratios = fightDuels([QM, QM, QM, QM], [ ['Qlearning', 'Qlearning'],
                                                    ['Qlearning', 'random' ],
                                                    ['random', 'Qlearning' ],
                                                    ['random', 'random'    ] ], size, 100)
            cols = ["P1 win", "draw", "P1 loss"]
            table = pd.DataFrame(ratios,
                                 index = ['Qlearning v Qlearning',
                                          'Qlearning v random',
                                          'random v Qlearning',
                                          'random v random'],  columns=cols,)
            print "ALPHA: ", alp, "GAMMA: ", gam
            print table

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
            
    print "Training time: " , time() - start
                
    # with open("../lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)

    # ##### Explore Q #####
    # exploreQ(QM,2)

        
    # with open("../mQm_3x3.pickle", 'wb') as f:
    #     pickle.dump([ts, QM], f,  pickle.HIGHEST_PROTOCOL)

    # # with open("../mQm_3x3.pickle", 'rb') as f:
    # #     #lucky_Q = pickle.load(f)
    # #     QM = pickle.load(f)

if __name__ == "__main__":
    run()

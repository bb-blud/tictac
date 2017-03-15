import sys
sys.path.append("../")

from time import time
import pandas as pd
from utilities import *

def run():
    
    #################################################################################
    #               Miscellaneous Q-Learning Training  
    ##################################################################################
    
    #Seed Q with initial random games
    size = 3    
    #ts = [70, 1000, 1000, 2000]
    ts = [70, 200, 200, 300]
    start = time()    
    # QM, tally, conv = playGames(setupGame(QMap(), size, ['random', 'miniQmax'],  learning=True, d1=3,d2=3), ts[0])
    # QM, tally, conv = playGames(setupGame(QMap(), size, ['miniQmax', 'random'],  learning=True, d1=3,d2=3), ts[0])
    # # player 2 learning against a random player 1
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])
    
    # # Now player 1 learning against a random player 2
    # QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])
    
    # # Have two agents learn against  each other
    # QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])

    # print "Training time: " , time() - start  
    # exploreQ(QM,1)
    
    #####################
    # Using Multiprocess

    # Seed Q with initial random games
    start = time()
    QM = multiTrain(setupGame(QMap(), size, ['random', 'random'], learning=True), runs=7, batch_size=10)

    # player 2 learning against a random player 1
    QM = multiTrain(setupGame(QM, size, ['random', 'Qlearning'], learning=True),  runs=20, batch_size=100)

    # Now player 1 learning against a random player 2
    QM = multiTrain(setupGame(QM, size, ['Qlearning', 'random'], learning=True), runs=20, batch_size=100)

    # Have two agents learn against  each other
    QM = multiTrain(setupGame(QM, size, ['Qlearning', 'Qlearning'], learning=True),runs=20, batch_size=200)
    print "Training time: " , time() - start

    
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

    # Qname =
    # with open("../Qs/"+Qname+".pickle", 'wb') as f:
    #     pickle.dump(QM, f, pickle.HIGHEST_PROTOCOL)
 

    #####
    #save QM
    # with open("../mulit3x3_600.pickle", 'wb') as f:
    #     QM = pickle.dump(QM, f,  pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    run()




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

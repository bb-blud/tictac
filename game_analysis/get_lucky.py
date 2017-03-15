import sys
sys.path.append("../")

from time import time
import pandas as pd
from utilities import *

def run():

    ###############################################################
    # Reproduce Lucky_Q, get lucky again

    size = 3
    ts = [70, 1000, 1000, 1000] 
    
    QM = QMap(gamma=0.1, alpha=0.1) #Initialize QM with parameters found in faux gridsearch
    
    start = time() 
    QM, tally, conv = playGames(setupGame(QMap(), size, ['random', 'random'],  learning=True), ts[0])   
    # player 2 learning against a random player 1
    QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'random'],   learning=True), ts[1])   
    # Now player 1 learning against a random player 2
    QM, tally, conv = playGames(setupGame(QM, size, ['random', 'Qlearning'],   learning=True), ts[2])    
    # Have two agents learn against each other
    QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning', 'Qlearning'],learning=True), ts[3])
    print "Training time: " , time() - start 
    
    ##TEST IT
    ratios = fightDuels([QM, QM, QM, QM, QM,QM, QM, QMap()],
                        [ ['ideal', 'Qlearning'  ],
                          ['Qlearning', 'ideal'  ],
                          ['minimax', 'Qlearning'],
                          ['Qlearning', 'minimax'],
                          ['Qlearning', 'Qlearning'],
                          ['random', 'Qlearning'],
                          ['Qlearning', 'random'], 
                          ['random','random'] ], size, n_games = 100 )
 
    
    cols = ["P1 win",  "draw", "P1 loss"]
    
    rows = ('ideal vs lucky_Q', 'lucky_Q vs ideal',
            'minimax vs lucky_Q', 'lucky_Q vs minimax',
            'lucky_Q vs lucky_Q',
            'random vs lucky_Q',
            'lucky_Q vs random',
            'random vs random')
    
    table = pd.DataFrame(ratios, columns = cols, index = rows)
    print table
    print
    
    table.plot.barh(colormap="Greens", stacked=True)
    plt.show()
    print

if __name__ == "__main__":
    run()

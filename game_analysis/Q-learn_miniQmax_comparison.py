import sys
sys.path.append("../")

import pickle
from time import time
import pandas as pd
from utilities import *

############################################################
# Compare Qlearning (lucky) with miniQmax different Qs

# NOTES: The following section reproduces the table results in the miniQmax luckyQ
# comparison of the "refinement" section of the report.

def run():

    with open("../Qs/newlucky.pickle", 'rb') as f:
        luckyQ=pickle.load(f)
    size = 3
    ts = [70]
    start = time()
    
    ##########
    #Training
    #Initialize a QMap with just 70 random games played ("Lazy" Q from the report)
    ranQ, tally, conv = playGames(setupGame(QMap(), size, ['random', 'random'],  learning=True), ts[0]) 
    print "Training time: " , time() - start 

    status = 'good'
    print [status for k in range(5)]
    print

    ##########
    #MiniQmax vs Qlearn 
    ratios = [getRatios(setupGame(QMap(), size, ['Qlearning', 'miniQmax'], p1QM=luckyQ, p2QM=luckyQ, d2=3), 100)]
    ratios.append(getRatios(setupGame(QMap(), size, ['miniQmax', 'Qlearning'], p1QM=luckyQ, p2QM=luckyQ, d1=3), 100))
    ratios.append(getRatios(setupGame(QMap(), size, ['Qlearning', 'miniQmax'], p1QM=luckyQ, p2QM=ranQ, d2=3), 100))
    ratios.append(getRatios(setupGame(QMap(), size, ['miniQmax', 'Qlearning'], p1QM=ranQ, p2QM=luckyQ, d1=3), 100))
    
    cols = ('P1 win', 'draw', 'P1 loss')
    
    rows = ['lucky_Qlearn v lucky_Qmax',
            
            'lucky_Qmax v lucky_Qlearn',
            
            'luckyQ_learn v miniQmax',
            
            'miniQmax v lucky_Qlearn']

    table = pd.DataFrame(ratios, columns = cols, index=rows)
    print "total time: " , time()-start
    print table
    table.plot.barh(colormap='Greens')
    plt.show()
    

    #table.to_csv('../"lucky_v_mini_'+status+'.csv')
    
    ##########
    #Comparison with random with
    ratios  = fightDuels([luckyQ, luckyQ, ranQ, ranQ],
                         [ ['random', 'miniQmax' ],
                           ['miniQmax', 'random' ],
                           ['random', 'miniQmax'],
                           ['miniQmax', 'random' ]], size, n_games = 100 , p1ds = [2,3,2,3], p3ds = [3,2,3,2] )
    
    rws = ['random v lucky_Qmax' ,
            'lucky_Qmax v random' ,
            'random v miniQmax',
            'miniQmax v random' ]
    
    ranTable = pd.DataFrame(ratios, columns=cols, index=rws)
    print ranTable
    ranTable.plot.barh(colormap='Greens')
    plt.show()
    # ranTable.to_csv('../"random_v_mini_'+status+'.csv')

    ###########
    #Final comparison minQmax uninitialized
    start = time()
    duels = [ ['Qlearning','miniQmax' ],
              ['miniQmax', 'Qlearning'],
              ['random', 'miniQmax'   ],
              ['miniQmax','random'    ] ]
    
    start = time()
    ratios = []
    ratios.append(getRatios(setupGame(QMap(), size,duels[0], p1QM=luckyQ, d2=3), 100))
    ratios.append(getRatios(setupGame(QMap(), size,duels[1], p2QM=luckyQ, d1=3), 100))
    ratios.append(getRatios(setupGame(QMap(), size,duels[2], d2=3), 100))
    ratios.append(getRatios(setupGame(QMap(), size,duels[3], d1=3), 100))
    
    print "total time: ", time() - start

    cols = ["P1 win",  "draw", "P1 loss"]
    rows = [r[0] +' v '+r[1] for r in duels]
    ftable = pd.DataFrame(ratios, columns = cols, index=rows)
    # ftable.to_csv('../"miniQmax_blankQ.csv')
    print ftable

if __name__ == "__main__":
    run()

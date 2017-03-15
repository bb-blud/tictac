import sys
sys.path.append("../")

from time import time
from utilities import * 

def run():
    size = 3
    #########################
    # Ideal policy stats 3x3
    columns  = ('P1 actual counts', 'Ideal as player1', 'P2 actual counts', 'Ideal as player 2')
    start = time()
    # Perfect X player 3x3 win/draw/loss ratio 91:3:0 or 0.9681 : 0.0319 : 0  
    ratios = [[ 91./94, 3.0/94, 0/94]]
    ratios += fightDuels([QMap()], [['ideal', 'random']], size, n_games = 1000)

    # Perfect O player 3x3 win/draw/loss ratio 0:3:44 or 0.9363 :0.0638 : 0
    ratios.append([ 44./47, 3.0/47, 0.0/47 ])
    
    # This guy needs to be reversed because we are interested in player2 wins
    ratios.append(fightDuels([QMap()], [['random', 'ideal']], size, n_games = 1000)[0][::-1] )

    start = time()
    ratios = np.transpose(ratios)
    graphStats(columns, ratios, 'Ideal policy against random 3x3') 
    
    #########################
    # Minimax policy stats 3x3
    columns  = ('P1 actual counts', 'Minimax as player 1', 'P2 actual counts', 'Minimax as player 2')
    start = time()
    # Perfect X player 3x3 win/draw/loss ratio 91:3:0 or 0.9681 : 0.0319 : 0  
    ratios  = [[ 91./94, 3.0/94, 0./94]]
    ratios += fightDuels([QMap()], [['minimax', 'random']], size, n_games = 500)
         
    # Perfect O player 3x3 win/draw/loss ratio 0:3:44 or 0.9363 :0.0638 : 0
    ratios.append([ 44./47, 3.0/47, 0/47 ])

    # This guy needs to be reversed because we are interested in player2 wins
    ratios.append(fightDuels([QMap()], [['random', 'minimax']], size, n_games = 500)[0][::-1])
    
    print time() - start        
    ratios = np.transpose(ratios)
    graphStats(columns, ratios, 'Minimax policy against random 3x3')
    
    ###########################
    # Minimax vs Ideal
    print "Start minimax vs ideal"
    size = 3
    columns  = ('Minimax vs Ideal', 'Ideal vs Minimax')
    start = time()
    ratios = fightDuels([QMap(), QMap()], [['minimax', 'ideal'],
                                           ['ideal', 'minimax'] ], size, n_games = 3, p1qds = [5 , 2], p2ds = [2, 5])
    
    print time() - start        
    ratios = np.transpose(ratios)
    graphStats(columns, ratios, 'Minimax vs Ideal comparison 3x3')

if __name__ == "__main__":
    run()

from random import randint
from game_board import GameBoard
from game_state import Player, GameState

class LearningPlayer(Player):
    def __init__(self, mark, game_state):
        super(LearningPlayer, self).__init__(mark, game_state)

    def makeMove(self):
        size = self.game_state.size
        choosing = True
        move = None
        while choosing:
            move = randint(0, size**2 - 1)
            if move not in (m[0] for m in  self.game_state.game_sequence ):
                choosing = False
        return move, self.mark
            
def run():
    
    gs = GameState(4)
    gs.setPlayers(LearningPlayer('X',gs) ,LearningPlayer('O',gs) )

    while not gs.gameFinished():
        gs.takeStep()
    
    # s = GameState(5)
    # s.test_lines()
    
if __name__ == '__main__':
    run()

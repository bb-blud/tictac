class Strateegery(object):
    
    def __init__(self, game_state):
        self.game_state = game_state
        
    def measureState(self):
        gs = self.game_state
        size = self.game_state.size
        weightX = 0
        weight0 = 0
        gs.lines, "in strateegery"
        for direction in ['Horizontal', 'Vertical', 'Diagonal']:
           print [gs.lines[direction].get(coordinate) for coordinate in range(size) + range(size**2-size, 0, size)]
        
        return weightX, "working on it"

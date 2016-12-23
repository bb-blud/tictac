def class Strateegery(object):

    def __init__(self):

        self.Q = {}

        
    def updateQ(self, move):
        if not self.Q.get(move, False):
            self.Q[move] = 1
        else:
            self.Q[move] += 1

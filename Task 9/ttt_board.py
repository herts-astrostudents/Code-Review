import numpy as np

class TicTacToeBoard:
    def __init__(self, size=3):
        '''
        Class constructor.
        Set up initial values like the array for the board
        '''
        self.size = 3
        self.marker = [' ', 'X', 'O'] # for non, player 1 and player 2

        self.arr = np.zeros(self.size**2).reshape(self.size, self.size)
        self.current_player = 1
        self.numpad = np.rot90(np.arange(1,10).reshape(3,3).T)
        

    def set(self, value, player):
        '''
        Player made a move, add it to the array.
        NOTE: validate it before setting
        '''
        x, y = np.where(self.numpad == value)
        self.arr[x[0], y[0]] = player
    
    def show(self):
        '''
        Show the board in the terminal
        '''
        print '-' * (self.size*4+1), '\n',
        for i in range(self.size):
            print '|',
            for j in range(self.size):
                print self.marker[int(self.arr[i][j])], '|',

            print '\n',
            print '-' * (self.size*4+1), '\n',

    def get_winner(self):
        '''
        Check if anyone won.
        For instance, return 0 for no winner or player number - 1 or 2.
        '''        
        # row full and not zeros
        for i in range(self.size):
            row = self.arr[i:i+1][0]
            if all(x > 0 and x == row[0] for x in row):
                return int(row[0])

        # column full and not zeros
        for i in range(self.size):
            row = self.arr.T[i:i+1][0]
            if all(x > 0 and x == row[0] for x in row):
                return int(row[0])
        
        # forward diagonal full
        diag1 = np.diagonal(self.arr)
        if all(x > 0 and x == diag1[0] for x in diag1):
            return int(diag1[0])

        # backward diagonal full
        diag2 = np.diagonal(np.rot90(self.arr))
        if all(x > 0 and x == diag2[0] for x in diag2):
            return int(diag2[0])
        
        return 0

    def board_filled(self):
        '''
        Are all tiles filled.
        Returns True or False, for instance
        '''
        return np.all(self.arr > 0)
            
    def game_over(self):
        '''
        Are we done yet?
        Returns True or False, for instance
        '''
        return self.get_winner() > 0 or self.board_filled()
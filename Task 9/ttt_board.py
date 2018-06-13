import numpy as np

class TicTacToeBoard:
    def __init__(self, size=3):
        '''
        Class constructor.
        Set up initial values like the array for the board
        '''
        self.size = 3
        self.marker = [' ', 'X', 'O'] # for none, player 1 and player 2
        self.current_player = 1 # start with player 1
        # .........
        
    def set(self, value, player):
        '''
        Player made a move, add it to the array.
        NOTE: validate it before setting
        '''
    
    def show(self):
        '''
        Show the board in the terminal
        '''

    def get_winner(self):
        '''
        Check if anyone won.
        For instance, return 0 for no winner or player number - 1 or 2.
        '''
        
        return 0

    def board_filled(self):
        '''
        Are all tiles filled.
        Returns True or False, for instance
        '''

        return False
            
    def game_over(self):
        '''
        Are we done yet?
        Returns True or False, for instance
        '''

        return False
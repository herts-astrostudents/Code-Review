from ttt_board import TicTacToeBoard

# get a TicTacToeBoard object
board = TicTacToeBoard()

while not board.game_over():
    print('\n')
    board.show()

    # read a number
    tile = input('Player ' + board.marker[board.current_player] + ': ')

    board.set(tile, board.current_player)

    # switch to the next player, hehe
    board.current_player = 3 - board.current_player

print('\n')
board.show()

winner = board.get_winner()
if board.get_winner() > 0:
    print('Yaaaay, Player ' + board.marker[winner] + ' won.')
else:
    print('Everyone lost.')
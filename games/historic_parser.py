from boardgames import *
from checkers import *
import copy

def parse_history(history, gametype):
    boards = []
    for a in range(len(history)):
        if gametype == 'checkers':
            boards.append(Checkers(history=history[:a]).state)
        elif gametype == 'tic_tac_toe':
            boards.append(TicTacToe(history=history[:a]).state)
        
    return boards

from boardgames import *
from checkers import *
import json

def parse_history(history, gametype):
    boards = []
    history = json.loads(history)
    for a in range(len(history)):
        if gametype == 'checkers':
            boards.append(Checkers(history=history[:a]).state)
        elif gametype == 'tic_tac_toe':
            boards.append(TicTacToe(history=history[:a]).state)
        
    return boards

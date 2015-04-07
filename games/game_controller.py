import multiprocessing
import time_ai
import signal
import time as timer
from game import *

class TicTacToe:
    def __init__(self, n=3, s='', history=[]):
        self.state = []
        if s != '':
            s = s.split(',')
        self.n = n
        index = 0
        for i in range(n):
            k = []
            for j in range(n):
                if s != '' and index < len(s):
                    k.append(s[index])
                else:
                    k.append(' ')
                index += 1
            self.state.append(k)
        if len(history) > 0:
            for move in history:
                self.state[move[1]][move[2]] = move[0]
    def __str__(self):
        s = ''
        for i in range(self.n):
            if i != 0 and i != self.n:
                for j in range(self.n):
                    s += '-'
                    if j != self.n - 1:
                        s += '+'
                s += '\n'
            for j in range(self.n):
                s += self.state[i][j]
                if j != self.n - 1:
                    s += '|'
            s += '\n'
        return s
    def get_state_str(self):
        s = ''
        for row in self.state:
            for col in row:
                s += col + ','
        return s[:-1]
    def insert(self, piece, r, c):
        if type(r) is not int or type(c) is not int:
            return False
        if r >= self.n or c >= self.n:
            return False
        if self.state[r][c] != ' ':
            return False
        self.state[r][c] = piece
        return True
    def match(self, line, piece):
        c = piece
        win = [c == cp for cp in line]
        if False in win:
            return False
        return True
    def build_row(self, r):
        return list(self.state[r])
    def build_col(self, c):
        col = []
        for row in self.state:
            col.append(row[c])
        return col
    def build_down_diag(self):
        diag = []
        for r in range(self.n):
            diag.append(self.state[r][r])
        return diag
    def build_up_diag(self):
        diag = []
        for r in range(self.n):
            diag.append(self.state[r][self.n - 1 - r])
        return diag
    def check_win(self, piece):
        for i in range(self.n):
            if self.match(self.build_row(i), piece) or \
                   self.match(self.build_col(i), piece):
                return True
        if self.match(self.build_down_diag(), piece) or \
               self.match(self.build_up_diag(), piece):
            return True
        return False
    def full(self):
        for row in self.state:
            for col in row:
                if col == ' ':
                    return False
        return True

def something(s,move):
    exec(s)
    move[0] = r
    move[1] = c
    return
    
class TimeOutException(Exception): pass
def time_out(signum, frame):
    raise TimeOutException, "Time Out!!"


def play_game(users, ais, hist=[], turns=-1,time=0,p1time=0,p2time=0,
              game_type='tic_tac_toe'):
    ai = [{'user' : users[0], 'ai': ais[0]}, {'user' : users[1], 'ai' : ais[1]}]
    ttc = GameController(history=hist,time=time,p1t=p1time,p2t=p2time)
    if game_type == 'tic_tac_toe':
        game = TicTacToe(history=hist)
        controller = GameController(history=hist,time=time, p1t=p1time,
                                    p2t=p2time)
    elif game_type == 'checkers':
        game = Checkers(history=hist)
        controller = GameController(history=hist, time=time, p1t=p1time,p2t=p2time, player1='b', player2='r')
    while turns is not 0:
        if ttc.manage_turn(game, ai) == 0:
            break
        if ttc.get_winner() != ' ':
            break
        if turns is not -1:
            turns -= 1
    k = str(ttc)
    l = ttc.winner
    p1t = ttc.timers[0]
    p2t = ttc.timers[1]
    return (ttt.state, k, l, p1t, p2t)

if __name__ == "__main__":
    print play_game(['v2_rand', 'v2_rand'], time=1000)

import multiprocessing
import time as timer
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
    
    
    
class TicTacToeController:
    def __init__(self, player1='x', player2='o', history=[], time=0):
        self.player = len(history) % 2
        self.timers = [time, time]
        self.players = [player1, player2]
        self.history = history
        self.winner = ' '
    def __str__(self):
        s = 'Move sequence:\n'
        for i in self.history:
            s += str(i[0]) + ': ' + str(i[1:]) + '\n'
        return s
    def change_turn(self):
        self.player = 1 - self.player
    def get_input(self):
        r = input("Enter row\n")
        c = input("Enter col\n")
        return (r, c)
    def get_winner(self):
        return self.winner
    def win_statement(self):
        if self.winner == '!':
            return "It's a draw!!"
        return 'The winner is %s!' % self.winner
    def manage_turn(self, ttt, ai=['','']):
        if type(ttt) != type(TicTacToe()):
            #throw some error
            return False
        while 1:
            if ai[self.player] == '':
                r, c = self.get_input()
            else:
                try:
                    mvv=[-1,-1]
                    s = "import %s;r, c = %s.get_move('%s')"\
                        % (ai[self.player], ai[self.player], ttt.get_state_str())
                    p = multiprocessing.Process(target=something, name="ai", \
                                                args=(s,mvv))
                    p.start()
                    start = timer.clock()
                    while 1:
                        end = timer.clock()
                        if not p.is_alive:
                            p.join()
                            self.timers[self.player] -= (end-start)
                            r,c = mvv
                            print "Selected move!"
                            return self.timers[self.player]
                        if (end - start) > self.timers[self.player] \
                               and self.timers[self.player] > 0:
                            p.terminate()
                            p.join()
                            print "Ran out of time!!"
                            self.change_turn()
                            self.winner = self.players[self.player]
                            return 0
                except SyntaxError as inst:
                    print inst
                    print "Error in syntax!"
                    self.change_turn()
                    self.winner = self.players[self.player]
                    return 0
            player = self.players[self.player]
            if ttt.insert(player, r, c):
                self.history.append((player, r, c))
                if ttt.check_win(player):
                    self.winner = player
                    print "success"
                    return self.timers[self.player]
                elif ttt.full():
                    self.winner = '!'
                    return self.timers[self.player]
                self.change_turn()
                self.winner = ' '
                return self.timers[self.player]
            else:
                self.change_turn()
                print "picked a spot that cannot be chosen!!"
                self.winner = self.players[self.player]
                return 0
    

def play_game(ai, hist=[], turns=-1,time=0):
    ttc = TicTacToeController(history=hist,time=time)
    ttt = TicTacToe(history=hist)
    while turns is not 0:
        print ttc.players[ttc.player]
        ttc.manage_turn(ttt, ai)
        if ttc.get_winner() != ' ':
            break
        if turns is not -1:
            turns -= 1
        print ttt
    k = str(ttc)
    l = ttc.winner
    print (ttt.state, k, l)
    return (ttt.state, k, l)

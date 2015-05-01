import multiprocessing
import time_ai
import signal
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
            print history
            for move in history:
                self.state[move[1][0]][move[1][1]] = move[0]
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
    def move(self, piece, move):
        if len(move) != 2:
            return False
        r = move[0]
        c = move[1]
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


class GameBoard(object):
    def __init__(self, n, s='', m=None):
        self.state = []
        if s != '':
            s = s.split(',')
        self.n = n
        if m == None:
            self.m = n
            m = n
        else:
            self.m = m
        index = 0
        for i in range(n):
            k = []
            for j in range(m):
                if s != '' and index < len(s):
                    k.append(s[index])
                else:
                    k.append(' ')
                index += 1
            self.state.append(k)
    def insert(self, r, c, piece):
        self.state[r][c] = piece
    def move(self, turn, mvv):#sr, sc, dr, dc):
        for mv in mvv:
            if not isinstance(mv, list):
                return
            try:
                sr = mv[0]
                sc = mv[1]
                dr = mv[2]
                dc = mv[3]
            except:
                return False
            self.insert(dr, dc, self.state[sr][sc])
            self.insert(sr, sc, ' ')
            return True
    def __str__(self):
        s = ''
        for r in self.state:
            for c in r:
              s += str(c) + ','  
        return s[:-1]
    def __getitem__(self, x):
        return self.state[x]

class GameRules(object):
    def __init__(self):
        pass
    def valid_move(self, board, dest_r, dest_c):
        if dest_r >= board.n or dest_c >= board.m:
            return False
        return board[dest_r][dest_c] == ' '
    


class TimeOutException(Exception):
    pass

class GameController:
    def __init__(self, player1='x', player2='o', history=[], time=0, \
                 p1t=0, p2t=0):
        self.player = len(history) % 2
        self.timers = [p1t, p2t]
        self.max_time = time
        self.players = [player1, player2]
        self.history = history
        self.winner = ' '
        
    def __str__(self):
        s = ''
        for i in self.history:
            s += str(i[0]) + ':' + str(i[1]) + ' \n'
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
        #if type(ttt) != type(TicTacToe()):
            #throw some error
            #return False
        
        if ai[self.player]['ai'] == '':
            r, c = self.get_input()
        else:
            try:
                s = "import %s as ai\nr, c = ai.get_move('%s')"\
                    % (ai[self.player], ttt.get_state_str())
                    
                try:
                    mvv, added_time = time_ai.run_ai(ai[self.player], ttt.state, self.max_time - self.timers[self.player], self.players[self.player])
                    if isinstance(mvv, str):
                        self.history.append((self.players[self.player],mvv))
                        self.change_turn()
                        self.winner = self.players[self.player]
                        return 0
                    
                    self.timers[self.player] += added_time
                        
                    if self.timers[self.player] > self.max_time:
                        self.history.append((self.players[self.player], "Took too long!!"))
                        self.change_turn()
                        self.winner = self.players[self.players]
                        return 0
                    #r, c = mvv[0], mvv[1]
                    # print mvv, r, c
                        
                except TimeOutException, msg:
                    self.history.append((self.players[self.player],"Ran out of time!!!"))
                    self.change_turn()
                    self.winner = self.players[self.player]
                    return 0
                    
            except SyntaxError as inst:
                print inst
                self.history.append((self.players[self.player],"Error in syntax!"))
                self.change_turn()
                self.winner = self.players[self.player]
                return 0
            player = self.players[self.player]
        try:
            if ttt.move(player, mvv):
                self.history.append((player, mvv))
                if ttt.check_win(player):
                    self.change_turn()
                    self.winner = self.players[self.player]
                    return self.max_time
                self.change_turn()
                self.winner = ' '
                return self.max_time
            
            else:
                self.history.append((player, mvv))
                if len(mvv) > 1:
                    if mvv[0] == 9999 and mvv[1] == 9999:
                        print "ran out of time!"
                else:
                    self.history.append((self.players[self.player], "Made an invalid move!!"))
                self.change_turn()
                self.winner = self.players[self.player]
                return 0
        except SyntaxError as e:
            self.history.append((self.players[self.player], "Wrong format!!"))
            self.change_turn()
            self.winner = self.players[self.player]
    

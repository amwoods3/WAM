class TicTacToe:
    def __init__(self, n=3, s=''):
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
    def insert(self, piece, r, c):
        if r >= self.n or c >= self.n:
            return False
        if self.state[r][c] != ' ':
            return False
        self.state[r][c] = piece
        return True
    def match(self,line, piece):
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

class TicTacToeController:
    def __init__(self, player1='x', player2='o'):
        self.player = 0
        self.players = [player1, player2]
    def change_turn(self):
        self.player = 1 - self.player
    def get_input(self):
        r = input()
        c = input()
        return (r, c)
    def manage_turn(self, ttt):
        if type(ttt) != type(TicTacToe()):
            #throw some error
            return False
        while 1:
            r, c = self.get_input()
            if ttt.insert(self.players[self.player], r, c):
               self.change_turn()
               return

ttc = TicTacToeController()
ttt = TicTacToe()
print ttt
ttc.manage_turn(ttt)
print ttt

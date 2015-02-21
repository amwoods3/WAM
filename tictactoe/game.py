class GameBoard:
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
    def move(self, sr, sc, dr, dc):
        self.insert(dr, dc, self.state[sr][sc])
        self.insert(sr, sc, ' ')
    def __str__(self):
        s = ''
        for r in self.state:
            for c in r:
              s += str(c) + ','  
        return s[:-1]

class GameRules:
    def __init__(self):
        pass
    def valid_move(self, board, dest_r, dest_c):
        if dest_r >= board.n or dest_c >= board.m:
            return False
        return board[dest_r][dest_c] == ' '


class GameController:
    def __init__(self, player1='x', player2='o', name1='', name2=''):
        self.player = 0
        self.winner = ' '
        self.players = [player1, player2]
        self.history = []
        self.player_names = [name1, name2]
    def change_turn(self):
        self.player = 1 - self.player
    def get_input(self):
        r = input()
        c = input()
        return (r, c)
    def win_statement(self):
        if self.winner == '!':
            return "It's a draw!!"
        return "The winner is %s!!" % self.winner
    def manage_turn(self, game, ai=['','']):
        while 1:
            if ai[player] == '':
                r, c = self.get_input()
            else:
                exec("import %s; r, c = %s.get_move('%s')" % (ai, ai, game.get_state_str()))
            player = self.players[self.player]
            if game.insert(player, r, c):
                self.history.append((player, r, c))
                if game.check_win(player):
                    self.winner = player
                    return True
                elif game.full():
                    self.winner = '!'
                    return True
                self.change_turn()
                self.winner = ' '
                return True
            

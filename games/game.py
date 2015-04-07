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
    def move(self, sr, sc, dr, dc):
        self.insert(dr, dc, self.state[sr][sc])
        self.insert(sr, sc, ' ')
    def __str__(self):
        s = ''
        for r in self.state:
            for c in r:
              s += str(c) + ','  
        return s[:-1]

class GameRules(object):
    def __init__(self):
        pass
    def valid_move(self, board, dest_r, dest_c):
        if dest_r >= board.n or dest_c >= board.m:
            return False
        return board[dest_r][dest_c] == ' '



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
        
        if ai[self.player]['ai'] == '':
            r, c = self.get_input()
        else:
            try:
                s = "import %s as ai\nr, c = ai.get_move('%s')"\
                    % (ai[self.player], ttt.get_state_str())
                    
                try:
                    mvv, added_time = time_ai.run_ai(ai[self.player], ttt.state, self.max_time - self.timers[self.player], self.players[self.player])
                    self.timers[self.player] += added_time
                        
                    if self.timers[self.player] > self.max_time:
                        print "Took too long!!"
                        self.change_turn()
                        self.winner = self.players[self.players]
                        return 0
                    r, c = mvv[0], mvv[1]
                    print mvv, r, c
                        
                except TimeOutException, msg:
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
                return self.max_time
            elif ttt.full():
                self.winner = '!'
                return self.max_time
            self.change_turn()
            self.winner = ' '
            return self.max_time
            
        else:
            self.change_turn()
            if r == 9999 and c == 9999:
                print "ran out of time!"
            else:
                print "picked a spot that cannot be chosen!!"
            self.winner = self.players[self.player]
            return 0
    

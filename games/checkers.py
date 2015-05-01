from boardgames import GameBoard, GameRules#, GameController
import json

BLACK_STARTS = [(1, 0), (0, 1), (2, 1), (1, 2), (0, 3), (2, 3),
                (1, 4), (0, 5), (2, 5), (1, 6), (0, 7), (2, 7)]
RED_STARTS =   [(5, 0), (7, 0), (6, 1), (5, 2), (7, 2), (6, 3),
                (5, 4), (7, 4), (6, 5), (5, 6), (7, 6), (6, 7)]

## class CheckerPiece:
##     def __init__(self, color):
##         self.color = color
##         self.level = 1
##     def king(self):
##         self.level = 2
##     def __str__(self):
##         if self.color == 'Black':
##             if self.level == 2:
##                 return 'B'
##             else:
##                 return 'b'
##         else:
##             if self.level == 2:
##                 return 'R'
##             else:
##                 return 'r'
##     def __repr__(self):
##         return repr(self.__str__())
##     def __eq__(self, b):
##         return self.color == b.color
##     def __ne__(self, b):
##         return self.color != b.color
def CheckerPiece(color):
    if color == "Black":
        return 'b'
    elif color == "Red":
        return 'r'
    
def is_color(p, color):
    if color == "Black":
        return p == 'b' or p == 'B'
    elif color == "Red":
        return p == 'r' or p == 'R'
    return False

class CheckerBoard(GameBoard):
    def __init__(self, state=''):
        super(CheckerBoard, self).__init__(8)
        #GameBoard.__init__(self, 8, state)
        self.black_pos = list(BLACK_STARTS)
        self.red_pos = list(RED_STARTS)
        for pos in BLACK_STARTS:
            self.state[pos[0]][pos[1]] = 'b'#CheckerPiece('Black')
        for pos in RED_STARTS:
            self.state[pos[0]][pos[1]] = 'r'#CheckerPiece('Red')

    def __str__(self):
        s = ' 0 1 2 3 4 5 6 7\n'
        s += '+-+-+-+-+-+-+-+-+\n'
        r = 0
        for row in self.state:
            for square in row:
                s += '|' + str(square)
            s += '|' + str(r) + '\n'
            s += '+-+-+-+-+-+-+-+-+\n'
            r += 1
        return s
    def __repr__(self):
        return repr(self.state)
    def super_string(self):
        return super(CheckerBoard, self).__str__()
    def move(self, p, movv):
        is_jump = False
        kinged = False
        super(CheckerBoard, self).move(p, movv)
        for mvv in movv:
            if not isinstance(mvv, list):
                return
            turn = 'Black' if p == 'b' else 'Red'
            if CheckerRules().is_jump(self.state, mvv[0], mvv[1],
                                      mvv[2], mvv[3], turn):
                is_jump = True
                a = (mvv[0] + mvv[2]) / 2
                b = (mvv[1] + mvv[3]) / 2
                super(CheckerBoard, self).insert(a, b, ' ')
                if turn == 'Black':
                    self.red_pos.remove((a, b))
                else:
                    self.black_pos.remove((a, b))
            if p == 'r':
                self.red_pos.remove((mvv[0], mvv[1]))
                self.red_pos.append((mvv[2], mvv[3]))
            elif p == 'b':
                self.black_pos.remove((mvv[0], mvv[1]))
                self.black_pos.append((mvv[2], mvv[3]))
        for b in range(len(self.state[7])):
            if self.state[7][b] == 'b':
                self.state[7][b] = 'B'
                kinged = True
        for b in range(len(self.state[0])):
            if self.state[0][b] == 'r':
                self.state[0][b] = 'R'
                kinged = True
        return (is_jump, kinged)
            
            
    
class CheckerRules(GameRules):
    def __init__(self):
        self.red_direction = -1
        self.black_direction = 1
        
    def valid_move(self, board, mvv, turn):
        b = None
        if turn in ('b', 'r', 'B', 'R'):
            turn = "Black" if turn == "b" or turn == "B" else "Red"
        for index, mv in enumerate(mvv):
            if b == None:
                b = mv
            else:
                if b[2] != mv[0] or b[3] != mv[1]:
                    return False
                b = mv
            (source_r, source_c, dest_r, dest_c) = (mv[0], mv[1], mv[2], mv[3])
            if index > 0:
                if not self.is_jump(board, source_r, source_c, dest_r, dest_c, turn):
                    return False
            if not super(CheckerRules, self).valid_move(board, dest_r, dest_c):
                return False
        
            source = board[source_r][source_c]
            if not is_color(source, turn) and index == 0:#source != cp:
                return False
            jump_av = self.can_jump(board.red_pos, board.black_pos, turn, board)
            if jump_av:
                if not self.is_jump(board, source_r, source_c, dest_r, dest_c, turn):
                    print "That is not a jump!"
                    return False
            else:
                direction = self.black_direction if turn == 'Black'\
                            else self.red_direction
                if dest_r - source_r != direction:
                    if board[dest_r][dest_c] not in ('B', 'R'):
                        
                        print "You are heading in wrong direction with not a king"
                        return False
                if abs(dest_c - source_c) != 1:
                    return False
        return True
        
    def is_jump(self, board, source_r, source_c, dest_r, dest_c, turn):
        d1 = dest_r - source_r
        d2 = dest_c - source_c
        if abs(d1) == 2 and abs(d2) == 2:
            r = source_r + d1 / 2
            c = source_c + d2 / 2
            
            target = board[r][c]
            enemy = 'Black' if turn == 'Red' else 'Red'
            #enemy = CheckerPiece(enemy)
            
            if is_color(target, enemy):#target == enemy:
                return True
        return False
    
    def valid_directions(self, direction):
        return [(1 * direction, -1), (1 * direction, 1)]
    
    def jump_to_space(self, board, a, d1, d2):
        r = a[0] + d1 * 2
        c = a[1] + d2 * 2
        if r >= 8 or r < 0: return False
        if c >= 8 or c < 0: return False
        return (board[a[0] + d1 * 2][a[1] + d2 * 2] == ' ')
    
    def can_jump(self, red_pos, black_pos, turn, board):
        (attack,defend) = (red_pos,black_pos) if turn == 'Red' else (black_pos,red_pos)
        direction = self.black_direction if turn == 'Black' else self.red_direction
        for a in attack:
            for b in defend:
                checking = board[a[0]][a[1]]
                if self.a_can_attack_b(a, b, direction) \
                    and self.jump_to_space(board, a, direction, b[1] - a[1]):
                    return True
                if (checking == 'B' or checking == 'R') \
                    and self.a_can_attack_b(a, b, -direction) \
                    and self.jump_to_space(board, a, -direction, b[1] - a[1]):
                    return True
        return False
    def a_can_attack_b(self, a, b, direction):
        r = b[0] - a[0]
        c = b[1] - a[1]
        if b[0] + 1 >= 8 or b[0] - 1 < 0:
            return False
        if b[1] + 1 >= 8 or b[1] - 1 < 0:
            return False
        return r == direction and c in (1, -1)
    def a_can_jump(self, a, board):
        piece = board[a[0]][a[1]]
        if piece == 'r':
            defend = board.black_pos
            direction = self.red_direction
        elif piece == 'b':
            defend = board.red_pos
            direction = self.black_direction
        for b in defend:
            checking = board[a[0]][a[1]]
            if self.a_can_attack_b(a, b, direction) \
                   and self.jump_to_space(board, a, direction, b[1] - a[1]):
                return True
            if (checking == 'B' or checking == 'R') \
                   and self.a_can_attack_b(a, b, -direction) \
                   and self.jump_to_space(board, a, -direction, b[1] - a[1]):
                return True
    def possible_moves(self, a, board):
        d = (a[0] + 1, a[0] - 1)
        f = (a[1] + 1, a[1] - 1)
        pm = []
        for r in d:
            for c in f:
                if r >= 8 or r < 0 or c >= 8 or c < 0:
                    break
                if board[r][c] == ' ':
                    pm.append((r, c))
                elif self.a_can_attack_b(a, (r, c), r - a[0]):
                    r1 = r + (r - a[0])
                    c1 = c + (c - a[1])
                    if c1 >= 8 or c1 < 0 or r1 >= 8 or r1 < 0:
                        break
                    pm.append((r1, c1))
        return pm
    def a_can_move(self, a, board):
        s = board[a[0]][a[1]]
        c = (a[1] + 1, a[1] - 1)
        if s == 'R' or s == 'B':
            direction = 0
        else:
            direction = 1 if s == 'b' else -1
        pm = self.possible_moves(a, board)
        if not pm:
            return False
        if direction != 0:
            for move in pm:
                if a[0] + direction == move[0]:
                    return True
            return False
        return True
        

class Checkers:
    def __init__(self, n=3, s='', history=[]):
        self.board = CheckerBoard(s)
        self.state = self.board.state
        if len(history) > 0:
            for move in history:
                self.board.move(move[0], move[1])
    def __str__(self):
        s = ''
        n = self.board.n
        for i in range(n):
            if i != 0 and i != n:
                for j in range(n):
                    s += '-'
                    if j != n - 1:
                        s += '+'
                s += '\n'
            for j in range(n):
                s += str(self.state[i][j])
                if j != n - 1:
                    s += '|'
            s += '\n'
        return s
    def move(self, piece, mvv):
        cr = CheckerRules()
        try:
            if not cr.valid_move(self.board, mvv, piece):
                self.board.move(piece, mvv)
                return False
        except:
            self.board.move(piece, mvv)
            return False
        jumped, kinged = self.board.move(piece, mvv)
        last_m = len(mvv) - 1
        
        a = (mvv[last_m][2], mvv[last_m][3])
        print a
        if jumped:
            if not kinged:
                if cr.a_can_jump(a, self.board):
                    print "You can make another jump!!"
                    return False
        return True
    
    def check_win(self, piece):
        cr = CheckerRules()
        if piece == 'r':
            for r in self.board.red_pos:
                if cr.a_can_move(r, self.board):
                    return False
            return True
        if piece == 'b':
            for b in self.board.black_pos:
                if cr.a_can_move(b, self.board):
                    return False
            print "game over"
            return True
    def get_state_str(self):
        return self.board.super_string()
    
    

## if __name__ == "__main__":
##     board = CheckerBoard()
##     print board
##     a = input()
##     b = input()
##     c = input()
##     d = input()
##     rules = CheckerRules()
##     t = 'Black'
##     while rules.valid_move(board, [[a,b,c,d]], t):
##         board.move('b' if t == 'Black' else 'r', [[a,b,c,d]])
##         t = 'Red' if t == 'Black' else 'Black'
##         try:
##             a = input()
##             b = input()
##             c = input()
##             d = input()
##         except EOFError:
##             break
##     print board
#x = Checkers()
#print x

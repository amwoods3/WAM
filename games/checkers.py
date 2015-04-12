from boardgames import GameBoard, GameRules, GameController

BLACK_STARTS = [(1, 0), (0, 1), (2, 1), (1, 2), (0, 3), (2, 3),
                (1, 4), (0, 5), (2, 5), (1, 6), (0, 7), (2, 7)]
RED_STARTS =   [(5, 0), (7, 0), (6, 1), (5, 2), (7, 2), (6, 3),
                (5, 4), (7, 4), (6, 5), (5, 6), (7, 6), (6, 7)]

class CheckerPiece:
    def __init__(self, color):
        self.color = color
        self.level = 1
    def king(self):
        self.level = 2
    def __str__(self):
        if self.color == 'Black':
            if self.level == 2:
                return 'B'
            else:
                return 'b'
        else:
            if self.level == 2:
                return 'R'
            else:
                return 'r'
    def __eq__(self, b):
        return self.color == b.color
    
class CheckerBoard(GameBoard):
    def __init__(self, state=''):
        super(CheckerBoard, self).__init__(8)
        #GameBoard.__init__(self, 8, state)
        black_pos = list(BLACK_STARTS)
        red_pos = list(RED_STARTS)
        for pos in BLACK_STARTS:
            self.state[pos[0]][pos[1]] = CheckerPiece('Black')
        for pos in RED_STARTS:
            self.state[pos[0]][pos[1]] = CheckerPiece('Red')

    def __str__(self):
        s = '+-+-+-+-+-+-+-+-+\n'
        for row in self.state:
            for square in row:
                s += '|' + str(square)
            s += '|\n'
            s += '+-+-+-+-+-+-+-+-+\n'
        return s
    def super_string(self):
        return super.__str__(self)
    
class CheckerRules(GameRules):
    def __init__(self):
        self.red_direction = -1
        self.black_direction = 1
    def valid_move(self, board, source_r, source_c, dest_r, dest_c, turn):
        if not super.valid_move(board, dest_r, dest_c):
            return False
        jump_av = self.can_jump(board.red_pos, board.black_pos, turn, board)
        if jump_av:
            if not is_jump(board, source_r, source_c, dest_r, dest_c, turn):
                return False
    
    def is_jump(self, board, source_r, source_c, dest_r, dest_c, turn):
        d1 = dest_r - source_r
        d2 = dest_c - source_c
        if abs(d1) == 2 and abs(d2) == 2:
            r = source_r + d1 / 2
            c = source_c + d2 / 2
            if board[r][c] not in (CheckerPiece(turn), ' '):
                return True
        return False
    
    def valid_directions(self, direction):
        return [(1 * direction, -1), (1 * direction, 1)]
    
    def jump_to_space(self, board, a, d1, d2):
        return (board[a[0] + d1 * 2][a[1] + d2 * 2] == ' ')
    
    def can_jump(self, red_pos, black_pos, turn, board):
        attack,defend = red_pos,black_pos if turn == 'Red' else black_pos,red_pos
        direction = 1 if turn == 'Black' else -1
        for a in attack:
            for b in defend:
                if self.a_can_attack_b(a, b, direction) \
                   and self.jump_to_space(board, a, direction, b[1] - a[1]):
                    return True
        return False
    def a_can_attack_b(self, a, b, direction):
        r = a[0] - b[0]
        c = a[1] - b[1]
        return r == direction and c in (1, -1)
board = CheckerBoard()
print board

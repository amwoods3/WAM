from game import *
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
                return '#'
            else:
                return '@'
        else:
            if self.level == 2:
                return 'O'
            else:
                return 'o'
    
class CheckerBoard(GameBoard):
    def __init__(self, state):
        #super(CheckerBoard, self).__init__(8)
        GameBoard.__init__(self, 8)
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
        
class CheckerRules(GameRules):
    def __init__(self):
        self.red_direction = -1
        self.black_direction = 1
    def valid_move(self, board, source_r, source_c, dest_r, dest_c, turn):
        pass

board = CheckerBoard()
print board

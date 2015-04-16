
def get_move(state, time_limit, turn):
    import random, json
    state = json
    pos = []
    # get position of all player pieces
    for row in range(len(state)):
        for col in range(row):
            s = state[row][col]
            if s == turn or s == turn.lower():
                pos.append((row, col))
    direction = 1 if turn == 'b' else -1
    enemy = ('r', 'R') if turn == 'b' else ('b', 'B')
    # check for possible jumps
    for p in pos:
        r = p[0], c = p[1]
        r += direction
        r1 = r + direction
        c1 = c + 1
        c2 = c - 1
        if state[r][c1] in enemy:
            c2 = c1 + 1
            if state[r1][c1] == ' ':
                pass
            

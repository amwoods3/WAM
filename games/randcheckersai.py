def get_move(state, time_limit, turn):
    import random, json
    state = json.loads(state)
    pos = []
    # get position of all player pieces
    for row in range(len(state)):
        for col in range(len(state)):
            s = state[row][col].lower()
            if s == turn:
                pos.append((row, col))
    direction = 1 if turn == 'b' else -1
    enemy = ('r', 'R') if turn == 'b' else ('b', 'B')
    # check for possible jumps
    jumps = []
    for p in pos:
        r = p[0]
        c = p[1]
        r += direction
        r1 = r + direction
        c1 = c + 1
        c2 = c - 1
        if r < 8 and r >= 0:
            if c1 < 8:
                if state[r][c1] in enemy:
                    c3 = c1 + 1
                    if r1 < 8 and c3 < 8 and r1 >= 0:
                        if state[r1][c3] == ' ':
                            jumps.append(((p[0], p[1]), (r1, c3)))
            if c2 >= 0:
                if state[r][c2] in enemy:
                    c3 = c2 - 1
                    if r1 < 8 and c3 >= 0 and r1 >= 0:
                        if state[r1][c3] == ' ':
                            jumps.append(((p[0], p[1]), (r1, c3)))
    if len(jumps) > 0:
        return json.dumps(random.choice(jumps))
    moves = []
    for p in pos:
        r = p[0]
        c = p[1]
        r += direction
        c1 = c + 1
        c2 = c - 1
        if r < 8 and r >= 0:
            if c1 >= 0 and c1 < 8:
                if state[r][c1] == ' ':
                    moves.append(((p[0], p[1]), (r, c1)))
            if c2 >= 0 and c2 < 8:
                if state[r][c2] == ' ':
                    moves.append(((p[0], p[1]), (r, c2)))
    chosen = json.dumps(random.choice(moves))
    return chosen

import json
def get_move(state, time_limit, turn):
    import random
    state = json.JSONDecoder().decode(state)
    choices = [(i,j) for i in range(len(state)) for j in range(len(state[i])) if state[i][j] == ' ']
    for i in range(1000000):
        a = 1
        b = [a, 2]
        c = [b, a, 3]
        d = [c, b, a, 4]
        e = list(c) + list(b) + [a] + list(d) + c
    row, col = random.choice(choices)
    return json.JSONEncoder().encode((row, col))


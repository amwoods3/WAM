import json
def get_move(state, time_limit, turn):
    import random
    state = json.JSONDecoder().decode(state)
    choices = [(i,j) for i in range(len(state)) for j in range(len(state[i])) if state[i][j] == ' ']
    row, col = random.choice(choices)
    return json.JSONEncoder().encode([(row, col)])


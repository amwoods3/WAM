def get_move(state):
    import random
    state = state.split(',')
    choices = [i for i in range(len(state)) if state[i] == ' ']
    choose = random.choice(choices)
    row = choose / 3
    col = choose % 3
    return (row, col)


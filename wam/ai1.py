def get_move(state):
    state = state.split(',')
    choices = [i for i in range(len(state)) if state[i] == ' ']
    choose = choices[0]
    row = choose / 3
    col = choose % 3
    return (row, col)

def get_move(state):
    import random
    state = state.split(',')
    choices = [i for i in range(len(state)) if state[i] == ' ']
    choose = random.choice(choices)
    row = choose / 3
    col = choose % 3
    for i in range(899000):
        a = [1,2,3,4,5,6,7]
        a += [8]
        b = a + [9,0]
        if b[1] == a[1]:
            b = []
            a = [1]
        b.append(i)
        a.append(b)
    return (row, col)


from boardgames import *


def something(s,move):
    exec(s)
    move[0] = r
    move[1] = c
    return
    
#class TimeOutException(Exception): pass
#def time_out(signum, frame):
#    raise TimeOutException, "Time Out!!"


def play_game(users, ais, hist=[], turns=-1,time=0,p1time=0,p2time=0,
              game_type='tic_tac_toe'):
    ai = [{'user' : users[0], 'ai': ais[0]}, {'user' : users[1], 'ai' : ais[1]}]
    #ttc = GameController(history=hist,time=time,p1t=p1time,p2t=p2time)
    if game_type == 'tic_tac_toe':
        game = TicTacToe(history=hist)
        controller = GameController(history=hist,time=time, p1t=p1time,
                                    p2t=p2time)
    elif game_type == 'checkers':
        game = Checkers(history=hist)
        controller = GameController(history=hist, time=time, p1t=p1time,p2t=p2time, player1='b', player2='r')
    while turns is not 0:
        if controller.manage_turn(game, ai) == 0:
            break
        if controller.get_winner() != ' ':
            break
        if turns is not -1:
            turns -= 1
    k = str(ttc)
    l = ttc.winner
    p1t = controller.timers[0]
    p2t = controller.timers[1]
    return (ttt.state, k, l, p1t, p2t)

if __name__ == "__main__":
    print play_game(['v2_rand', 'v2_rand'], time=1000)

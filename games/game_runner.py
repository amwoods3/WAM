from boardgames import *
from checkers import *
from games.models import ActiveGame
import json
def something(s,move):
    exec(s)
    move[0] = r
    move[1] = c
    return
    
#class TimeOutException(Exception): pass
#def time_out(signum, frame):
#    raise TimeOutException, "Time Out!!"


def play_game(users, ais, hist=None, turns=-1,time=0,p1time=0,p2time=0,
              game_type='tic_tac_toe', p1id=1, p2id=2):
    if hist is None:
        hist = []
    ai = [{'user' : users[0], 'ai': ais[0]}, {'user' : users[1], 'ai' : ais[1]}]
    #ttc = GameController(history=hist,time=time,p1t=p1time,p2t=p2time)
    if game_type == 'tic_tac_toe':
        game = TicTacToe(history=hist)
        controller = GameController(history=hist,time=time, p1t=p1time,
                                    p2t=p2time)
    elif game_type == 'checkers':
        game = Checkers(history=hist)
        controller = GameController(history=hist, time=time, p1t=p1time,p2t=p2time, player1='b', player2='r')

        # create a point in database for this game.
    cur_game = ActiveGame(game_state=json.dumps(game.state), last_move= '', player1_id=p1id, player2_id=p2id, player1_timer=0, player2_timer=0, is_player1_turn = True, player1_ai=ais[0], player2_ai=ais[1])
    cur_game.save()

    
    while turns is not 0:
        if controller.manage_turn(game, ai) == 0:
            break
        else:
            cur_game.game_state = json.dumps(game.state)
            cur_game.last_move = json.dumps(controller.history[-1])
            cur_game.player1_timer=controller.timers[0]
            cur_game.player2_timer=controller.timers[1]
            cur_game.is_player1_turn = controller.player == 0
            cur_game.save()
        if controller.get_winner() != ' ':
            break
        if turns is not -1:
            turns -= 1
    k = str(controller)
    l = controller.winner
    p1t = controller.timers[0]
    p2t = controller.timers[1]
    return (game.state, k, l, p1t, p2t, controller.history)

if __name__ == "__main__":
    print play_game(['v2_rand', 'v2_rand'], time=1000, game_type='checkers')

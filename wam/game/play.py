import veiws

def play(request):
    import sys
    sys.path.insert(0, 'ais')
    sys.path.insert(0, '../tictactoe/')
    import tictactoe
    from html_change import *
    s = tictactoe.play_game(ai=['ai1', 'randai'])
    return HttpResponse(change(s))
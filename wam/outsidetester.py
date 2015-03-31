import sys
from config import AI_PATH, TEST_PATH
sys.path.insert(0, '%sgames/' % (TEST_PATH))
import tictactoe as ttt

ttt.play_game(['testuser', 'testuser'], ['v2_rand', 'v2_rand'], time=1000)

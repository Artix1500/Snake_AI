ENABLE_KEYBOARD = False

BLOCK_SIZE = 50

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
KEY = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3, "YES": 4, "NO": 5, "EXIT": 6}
REWARD = {"DEATH" : 0, "EAT" : 0, "LIVE" : 1}

def check_collision(pos1, pos2):
    if(pos1.x == pos2.x and pos1.y == pos2.y):
        return True
    return False 
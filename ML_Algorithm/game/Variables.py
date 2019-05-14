ENABLE_KEYBOARD = False

BLOCK_SIZE = 50

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4, "YES": 5, "NO": 6, "EXIT": 7}

REWARD = {"DEATH" : -10, "EAT" : 20, "LIVE" : 5}

def check_collision(pos1, pos2):
    if pos1.x * BLOCK_SIZE < (pos2.x + 1) * BLOCK_SIZE and (
            pos1.x + 1) * BLOCK_SIZE > pos2.x * BLOCK_SIZE and pos1.y * BLOCK_SIZE < (pos2.y + 1) * BLOCK_SIZE and (
            pos1.y + 1) * BLOCK_SIZE > pos2.y * BLOCK_SIZE:
        return True
    return False
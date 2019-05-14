from game.Variables import BLOCK_SIZE

class Apple:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.exists = state

    def draw(self, screen, apple_image):
        screen.blit(apple_image, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE))
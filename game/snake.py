from pygame.locals import *
from random import randint
import pygame
import time


def do_collide(x1, y1, x2, y2):
    if x2 <= x1 <= x2 + Game.block_size - 5:
        if y2 <= y1 <= y2 + Game.block_size - 5:
            return True
    return False


class Apple:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x * Game.block_size
        self.y = y * Game.block_size

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Snake:

    def __init__(self, length):
        self.length = length
        self.direction = 0
        self.refresh_counter = 0
        self.x = [2 * Game.block_size, 1 * Game.block_size, 0]
        self.y = [0]

        # initial positions, no collision.
        self.y.append(0)
        self.y.append(0)

    def update(self):
        # move tail
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # move head
        if self.direction == 0:
            self.x[0] = self.x[0] + Game.block_size
        if self.direction == 1:
            self.x[0] = self.x[0] - Game.block_size
        if self.direction == 2:
            self.y[0] = self.y[0] - Game.block_size
        if self.direction == 3:
            self.y[0] = self.y[0] + Game.block_size

    def move_right(self):
        if self.direction != 1:
            self.direction = 0

    def move_left(self):
        if self.direction != 0:
            self.direction = 1

    def move_up(self):
        if self.direction != 3:
            self.direction = 2

    def move_down(self):
        if self.direction != 2:
            self.direction = 3

    def draw(self, surface, block):
        if len(self.x) < self.length:
            self.x.append(self.x[len(self.x) - 1])
            self.y.append(self.y[len(self.y) - 1])
        for i in range(0, self.length):
            surface.blit(block, (self.x[i], self.y[i]))

    def log(self):
        print("===================")
        for i in range(0, self.length):
            print("x[" + str(i) + "] (" + str(self.x[i]) + "," + str(self.y[i]) + ")")


class Game:
    window_width = 800
    window_height = 600
    block_size = 50
    delay = 100.0 / 1000.0

    def __init__(self):
        self.running = True
        self.background_image = None
        self.snake_image = None
        self.apple_image = None
        self.snake = Snake(3)
        self.apple = Apple(7, 7)

    def get_width_bound(self):
        return Game.window_width // Game.block_size

    def get_height_bound(self):
        return Game.window_height // Game.block_size

    def on_init(self):
        pygame.init()
        self.background_image = pygame.display.set_mode((Game.window_width, Game.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Snake')
        self.running = True
        self.snake_image = pygame.image.load("snake_box.jpg").convert()
        self.snake_image = pygame.transform.scale(self.snake_image, (Game.block_size, Game.block_size))
        self.apple_image = pygame.image.load("apple.png").convert()
        self.apple_image = pygame.transform.scale(self.apple_image, (Game.block_size, Game.block_size))

    def on_loop(self):
        self.snake.update()
        # self.snake.log()

        # self collision
        for i in range(2, self.snake.length):
            if do_collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                print("COLLISION: x[0] (" + str(self.snake.x[0]) + "," + str(self.snake.y[0]) + ") with x[" + str(i) + "] (" + str(self.snake.x[i]) + "," + str(self.snake.y[i]) + ")")
                exit(0)

        # apple collision
        for i in range(0, self.snake.length - 1):
            if do_collide(self.apple.x, self.apple.y, self.snake.x[i], self.snake.y[i]):
                self.apple.x = randint(0, self.get_width_bound() - 1) * Game.block_size
                self.apple.y = randint(0, self.get_height_bound() - 1) * Game.block_size
                self.snake.length = self.snake.length + 1

        # wall collision todo...

        pass

    def on_cleanup(self):
        pygame.quit()

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False

    def on_render(self):
        self.background_image.fill((0, 0, 0))
        self.snake.draw(self.background_image, self.snake_image)
        self.apple.draw(self.background_image, self.apple_image)
        pygame.display.flip()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.snake.move_right()
            if keys[K_LEFT]:
                self.snake.move_left()
            if keys[K_UP]:
                self.snake.move_up()
            if keys[K_DOWN]:
                self.snake.move_down()
            if keys[K_ESCAPE]:
                self.running = False

            self.on_loop()
            self.on_render()
            time.sleep(Game.delay)

        self.on_cleanup()


if __name__ == "__main__":
    game_instance = Game()
    game_instance.on_execute()

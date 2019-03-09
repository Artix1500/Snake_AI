from pygame.locals import *
import pygame
import time


class Apple:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x * Game.block_size
        self.y = y * Game.block_size

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Snake:
    refresh_max = 2

    def __init__(self, length):
        self.length = length
        self.direction = 0
        self.refresh_counter = 0
        self.x = []
        self.y = []
        for i in range(0, length):
            self.x.append(0)
            self.y.append(0)

    def update(self):
        self.refresh_counter = self.refresh_counter + 1
        if self.refresh_counter > Snake.refresh_max:
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

            self.refresh_counter = 0

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface, block):
        for i in range(0, self.length):
            surface.blit(block, (self.x[i], self.y[i]))


class Game:
    window_width = 800
    window_height = 600
    block_size = 50
    delay = 20.0 / 1000.0

    def __init__(self):
        self.running = True
        self.background_image = None
        self.snake_image = None
        self.apple_image = None
        self.snake = Snake(5)
        self.apple = Apple(5, 5)

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

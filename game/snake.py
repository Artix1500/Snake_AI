from pygame.locals import *
import pygame


class Snake:
    x = 0
    y = 0
    speed = 1
 
    def move_right(self):
        self.x = self.x + self.speed
 
    def move_left(self):
        self.x = self.x - self.speed
 
    def move_up(self):
        self.y = self.y - self.speed
 
    def move_down(self):
        self.y = self.y + self.speed


class Game:
    windowWidth = 800
    windowHeight = 600
    snake = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.snake = Snake()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Snake')
        self._running = True
        self._image_surf = pygame.image.load("snake_box.jpg").convert()
        self._image_surf = pygame.transform.scale(self._image_surf, (80, 80))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(self._image_surf, (self.snake.x, self.snake.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
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
                self._running = False

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    game_instance = Game()
    game_instance.on_execute()

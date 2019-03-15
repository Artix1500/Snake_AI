import pygame
import random
import sys

FPS = 15
BLOCK_SIZE = 50
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
BOARD_HEIGHT = SCREEN_HEIGHT / BLOCK_SIZE
BOARD_WIDTH = SCREEN_WIDTH / BLOCK_SIZE
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}


def check_collision(pos1, pos2):
    if pos1.x < pos2.x + BLOCK_SIZE and pos1.x + BLOCK_SIZE > pos2.x and pos1.y < pos2.y + BLOCK_SIZE and pos1.y + BLOCK_SIZE > pos2.y:
        return True
    return False


class Apple:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.exists = state

    def draw(self, screen):
        screen.blit(apple_image, (self.x, self.y))


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["DOWN"]

        self.elements = []
        head = Segment(self.x, self.y)
        head.direction = KEY["DOWN"]
        self.elements.append(head)

        self.move()
        self.grow()
        self.move()

    def move(self):
        last_element = len(self.elements) - 1
        while last_element != 0:
            self.elements[last_element].direction = self.elements[last_element - 1].direction
            self.elements[last_element].x = self.elements[last_element - 1].x
            self.elements[last_element].y = self.elements[last_element - 1].y
            last_element -= 1

        if len(self.elements) < 2:
            last_segment = self
        else:
            last_segment = self.elements.pop(last_element)

        last_segment.direction = self.elements[0].direction

        if self.elements[0].direction == KEY["UP"]:
            last_segment.y = self.elements[0].y - BLOCK_SIZE
        elif self.elements[0].direction == KEY["DOWN"]:
            last_segment.y = self.elements[0].y + BLOCK_SIZE
        elif self.elements[0].direction == KEY["LEFT"]:
            last_segment.x = self.elements[0].x - BLOCK_SIZE
        elif self.elements[0].direction == KEY["RIGHT"]:
            last_segment.x = self.elements[0].x + BLOCK_SIZE
        self.elements.insert(0, last_segment)

    def get_head(self):
        return self.elements[0]

    def grow(self):
        last_element = len(self.elements) - 1
        self.elements[last_element].direction = self.elements[last_element].direction

        if self.elements[last_element].direction == KEY["UP"]:
            new_segment = Segment(self.elements[last_element].x, self.elements[last_element].y - BLOCK_SIZE)
        elif self.elements[last_element].direction == KEY["DOWN"]:
            new_segment = Segment(self.elements[last_element].x, self.elements[last_element].y + BLOCK_SIZE)
        elif self.elements[last_element].direction == KEY["LEFT"]:
            new_segment = Segment(self.elements[last_element].x - BLOCK_SIZE, self.elements[last_element].y)
        elif self.elements[last_element].direction == KEY["RIGHT"]:
            new_segment = Segment(self.elements[last_element].x + BLOCK_SIZE, self.elements[last_element].y)

        self.elements.append(new_segment)

    def set_direction(self, direction):
        if (self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or
                self.direction == KEY["LEFT"] and direction == KEY["RIGHT"] or
                self.direction == KEY["UP"] and direction == KEY["DOWN"] or
                self.direction == KEY["DOWN"] and direction == KEY["UP"]):
            pass
        else:
            self.direction = direction

    def check_crash(self):
        if self.elements[0].x < 0 or self.elements[0].y < 0 or self.elements[0].x >= SCREEN_WIDTH or self.elements[0].y >= SCREEN_HEIGHT:
            return True

        counter = 1
        while counter < len(self.elements) - 1:
            if check_collision(self.elements[0], self.elements[counter]):
                return True
            counter += 1
        return False

    def draw(self, screen):
        screen.blit(snake_image, (self.elements[0].x, self.elements[0].y))
        counter = 1
        while counter < len(self.elements):
            screen.blit(snake_image, (self.elements[counter].x, self.elements[counter].y))
            counter += 1


def read_key():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            sys.exit()


def spawn_apple(snake):
    valid_apple = False
    x = 0
    y = 0
    while not valid_apple:
        x = random.randint(0, BOARD_WIDTH - 1) * BLOCK_SIZE
        y = random.randint(0, BOARD_HEIGHT - 1) * BLOCK_SIZE
        valid_apple = not check_collision(snake.get_head(), Segment(x, y))

    return Apple(x, y, True)


def end_game():
    message = game_over_font.render("Game Over", 1, pygame.Color("white"))
    message_play_again = play_again_font.render("Restart? Y / N", 1, pygame.Color("green"))
    main_screen.blit(message, (320, 240))
    main_screen.blit(message_play_again, (320 + 12, 240 + 40))

    pygame.display.flip()
    pygame.display.update()

    my_key = read_key()
    while my_key != "exit":
        if my_key == "yes":
            run_game()
        elif my_key == "no":
            break
        my_key = read_key()
        game_clock.tick(FPS)
    sys.exit()


def draw_score(score):
    score_area = score_area_font.render(str(score), 1, pygame.Color("white"))
    main_screen.blit(score_msg, (SCREEN_WIDTH - score_msg_size[0] - 60, 10))
    main_screen.blit(score_area, (SCREEN_WIDTH - 45, 10))


def draw_game_time(game_time_value):
    game_time = score_font.render("Time:", 1, pygame.Color("white"))
    game_time_area = score_area_font.render(str(game_time_value / 1000), 1, pygame.Color("white"))
    main_screen.blit(game_time, (30, 10))
    main_screen.blit(game_time_area, (105, 10))


def run_game():
    score = 0

    # Snake initialization
    main_snake = Snake(1 * BLOCK_SIZE, 1 * BLOCK_SIZE)

    # Apples
    apple_eaten = False
    apple = spawn_apple(main_snake)

    start_time = pygame.time.get_ticks()
    running = True

    while running:
        game_clock.tick(FPS)

        # Input
        key_pressed = read_key()
        if key_pressed == "exit":
            running = False

        # Collision check
        if main_snake.check_crash():
            end_game()

        if apple.exists:
            if check_collision(main_snake.get_head(), apple):
                main_snake.grow()
                apple.exists = False
                score += 5
                apple_eaten = True

        # Moving snake
        if key_pressed:
            main_snake.set_direction(key_pressed)
        main_snake.move()

        # Spawning apple
        if apple_eaten:
            apple_eaten = False
            apple = spawn_apple(main_snake)

        # Drawing
        main_screen.fill(background_color)
        if apple.exists:
            apple.draw(main_screen)

        main_snake.draw(main_screen)
        draw_score(score)
        game_time = pygame.time.get_ticks() - start_time
        draw_game_time(game_time)

        pygame.display.flip()
        pygame.display.update()


if __name__ == "__main__":
    # Screen setup
    pygame.init()
    pygame.display.set_caption("Snake")
    pygame.font.init()
    random.seed()

    # Global resources
    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)
    score_font = pygame.font.Font(None, 25)
    score_area_font = pygame.font.Font(None, 25)
    game_over_font = pygame.font.Font(None, 45)
    play_again_font = score_area_font
    score_msg = score_font.render("Score:", 1, pygame.Color("white"))
    score_msg_size = score_font.size("Score")
    background_color = pygame.Color(100, 100, 100)
    game_clock = pygame.time.Clock()
    apple_image = pygame.transform.scale(pygame.image.load("apple.png").convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
    snake_image = pygame.transform.scale(pygame.image.load("snake_box.jpg").convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    run_game()

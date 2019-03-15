import pygame
import random
import sys

FPS = 15
BLOCK_SIZE = 50
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}


def check_collision(pos1, pos2):
    if pos1.x * BLOCK_SIZE < (pos2.x + 1) * BLOCK_SIZE and (
            pos1.x + 1) * BLOCK_SIZE > pos2.x * BLOCK_SIZE and pos1.y * BLOCK_SIZE < (pos2.y + 1) * BLOCK_SIZE and (
            pos1.y + 1) * BLOCK_SIZE > pos2.y * BLOCK_SIZE:
        return True
    return False


class Apple:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.exists = state

    def draw(self, screen):
        screen.blit(apple_image, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE))


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
            last_segment.y = self.elements[0].y - 1
        elif self.elements[0].direction == KEY["DOWN"]:
            last_segment.y = self.elements[0].y + 1
        elif self.elements[0].direction == KEY["LEFT"]:
            last_segment.x = self.elements[0].x - 1
        elif self.elements[0].direction == KEY["RIGHT"]:
            last_segment.x = self.elements[0].x + 1
        self.elements.insert(0, last_segment)

    def get_head(self):
        return self.elements[0]

    def grow(self):
        last_element = len(self.elements) - 1
        self.elements[last_element].direction = self.elements[last_element].direction

        if self.elements[last_element].direction == KEY["UP"]:
            new_segment = Segment(self.elements[last_element].x, self.elements[last_element].y - 1)
        elif self.elements[last_element].direction == KEY["DOWN"]:
            new_segment = Segment(self.elements[last_element].x, self.elements[last_element].y + 1)
        elif self.elements[last_element].direction == KEY["LEFT"]:
            new_segment = Segment(self.elements[last_element].x - 1, self.elements[last_element].y)
        elif self.elements[last_element].direction == KEY["RIGHT"]:
            new_segment = Segment(self.elements[last_element].x + 1, self.elements[last_element].y)

        self.elements.append(new_segment)

    def set_direction(self, direction):
        self.direction = direction

    def check_crash(self):
        if self.elements[0].x < 0 or self.elements[0].y < 0 or self.elements[0].x >= BOARD_WIDTH or self.elements[
            0].y >= BOARD_HEIGHT:
            return True

        counter = 1
        while counter < len(self.elements) - 1:
            if check_collision(self.elements[0], self.elements[counter]):
                return True
            counter += 1
        return False

    def draw(self, screen):
        screen.blit(snake_image, (self.elements[0].x * BLOCK_SIZE, self.elements[0].y * BLOCK_SIZE))
        counter = 1
        while counter < len(self.elements):
            screen.blit(snake_image, (self.elements[counter].x * BLOCK_SIZE, self.elements[counter].y * BLOCK_SIZE))
            counter += 1

    def collides_with_body(self, block):
        for segment in self.elements:
            if check_collision(block, segment):
                return True
        return False

    def display_log(self):
        print("Segments: ", end="")
        for segment in self.elements:
            print("({0}, {1}) ".format(segment.x, segment.y), end="")

        closest_right = 1
        closest_left = 1
        closest_up = 1
        closest_down = 1
        head = self.elements[0]

        while closest_right <= BOARD_WIDTH - head.x:
            if self.collides_with_body(Segment(head.x + closest_right, head.y)):
                break
            closest_right += 1

        while closest_left <= head.x + 1:
            if self.collides_with_body(Segment(head.x - closest_left, head.y)):
                break
            closest_left += 1

        while closest_down <= BOARD_HEIGHT - head.y:
            if self.collides_with_body(Segment(head.x, head.y + closest_down)):
                break
            closest_down += 1

        while closest_up <= head.y + 1:
            if self.collides_with_body(Segment(head.x, head.y - closest_up)):
                break
            closest_up += 1

        closest_right = min(closest_right, BOARD_WIDTH - head.x)
        closest_left = min(closest_left, head.x + 1)
        closest_down = min(closest_down, BOARD_HEIGHT - head.y)
        closest_up = min(closest_up, head.y + 1)

        crashes = {
            "right": closest_right,
            "left": closest_left,
            "down": closest_down,
            "up": closest_up
        }

        print("\nRight crash: {0}, left crash: {1}, up crash: {2}, down crash: {3}.".format(
            crashes["right"], crashes["left"], crashes["up"], crashes["down"]))


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


def wait_for_key():
    while True:
        event = pygame.event.wait()
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
        valid_apple = True
        x = random.randint(0, BOARD_WIDTH - 1)
        y = random.randint(0, BOARD_HEIGHT - 1)
        for segment in snake.elements:
            if check_collision(segment, Segment(x, y)):
                valid_apple = False
                break

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
    sys.exit()


def draw_score(score):
    score_area = score_area_font.render(str(score), 1, pygame.Color("white"))
    main_screen.blit(score_msg, (SCREEN_WIDTH - score_msg_size[0] - 60, 10))
    main_screen.blit(score_area, (SCREEN_WIDTH - 45, 10))


def redraw_game(apple, snake, score):
    main_screen.fill(background_color)
    if apple.exists:
        apple.draw(main_screen)
    snake.draw(main_screen)
    draw_score(score)
    pygame.display.flip()
    pygame.display.update()


def run_game():
    score = 0
    main_snake = Snake(1, 1)
    apple_eaten = False
    apple = spawn_apple(main_snake)
    running = True

    while running:

        # Draw game
        redraw_game(apple, main_snake, score)

        # Check collisions (walls and self)
        if main_snake.check_crash():
            end_game()

        # Check apple availability
        grow_snake = False
        if apple.exists:
            if check_collision(main_snake.get_head(), apple):
                grow_snake = True
                apple.exists = False
                score += 5
                apple_eaten = True

        # Spawn apple
        if apple_eaten:
            apple_eaten = False
            apple = spawn_apple(main_snake)
            print("Wow, you've eaten an apple! Next apple: ({0}, {1})".format(apple.x, apple.y))
            redraw_game(apple, main_snake, score)

        # Wait for user input (here goes agent's move)
        main_snake.display_log()
        print("Waiting for input...")
        key_pressed = wait_for_key()
        if key_pressed == "exit":
            running = False

        # Move snake
        if grow_snake:
            main_snake.grow()
        if key_pressed:
            main_snake.set_direction(key_pressed)
        main_snake.move()


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
    apple_image = pygame.transform.scale(pygame.image.load("apple.png").convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
    snake_image = pygame.transform.scale(pygame.image.load("snake_box.jpg").convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

    run_game()

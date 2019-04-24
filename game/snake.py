import sys
import os
import time

import pygame
import random
import sys

ENABLE_KEYBOARD = False
BLOCK_SIZE = 50
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4, "YES": 5, "NO": 6, "EXIT": 7}


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

    def draw(self, screen, apple_image):
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
        if self.elements[0].x < 0 or self.elements[0].y < 0 or self.elements[0].x >= BOARD_WIDTH or \
                self.elements[0].y >= BOARD_HEIGHT:
            return True

        counter = 1
        while counter < len(self.elements) - 1:
            if check_collision(self.elements[0], self.elements[counter]):
                return True
            counter += 1
        return False

    def draw(self, screen, snake_image):
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


class Game:
    def __init__(self):
        self.score = 0
        self.main_snake = Snake(1, 1)
        self.apple_eaten = False
        self.apple = self.spawn_apple()
        self.running = True
        self.last_info = self.get_info()
        self.grow_snake = False

        pygame.init()
        pygame.display.set_caption("Snake")
        pygame.font.init()
        random.seed()
        self.main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)
        self.score_font = pygame.font.Font(None, 25)
        self.score_area_font = pygame.font.Font(None, 25)
        self.game_over_font = pygame.font.Font(None, 45)
        self.play_again_font = self.score_area_font
        self.score_msg = self.score_font.render("Score:", 1, pygame.Color("white"))
        self.score_msg_size = self.score_font.size("Score")
        self.background_color = pygame.Color(100, 100, 100)
        self.apple_image = pygame.transform.scale(pygame.image.load(r"../game/apple.png").convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_image = pygame.transform.scale(pygame.image.load(r"../game/snake_box.jpg").convert_alpha(),
                                             (BLOCK_SIZE, BLOCK_SIZE))

    def get_info(self):
        closest_right = 1
        closest_left = 1
        closest_up = 1
        closest_down = 1
        head = self.main_snake.elements[0]

        while closest_right <= BOARD_WIDTH - head.x:
            if self.main_snake.collides_with_body(Segment(head.x + closest_right, head.y)):
                break
            closest_right += 1

        while closest_left <= head.x + 1:
            if self.main_snake.collides_with_body(Segment(head.x - closest_left, head.y)):
                break
            closest_left += 1

        while closest_down <= BOARD_HEIGHT - head.y:
            if self.main_snake.collides_with_body(Segment(head.x, head.y + closest_down)):
                break
            closest_down += 1

        while closest_up <= head.y + 1:
            if self.main_snake.collides_with_body(Segment(head.x, head.y - closest_up)):
                break
            closest_up += 1

        closest_right = min(closest_right, BOARD_WIDTH - head.x)
        closest_left = min(closest_left, head.x + 1)
        closest_down = min(closest_down, BOARD_HEIGHT - head.y)
        closest_up = min(closest_up, head.y + 1)

        apple_x_dist = abs(self.main_snake.elements[0].x - self.apple.x)
        apple_y_dist = abs(self.main_snake.elements[0].y - self.apple.y)

        info = {
            "right_crash": closest_right,
            "left_crash": closest_left,
            "down_crash": closest_down,
            "up_crash": closest_up,
            "reward": 0,
            "lost_game": False,
            "apple_x": apple_x_dist,
            "apple_y": apple_y_dist
        }

        print("\nRight crash: {0}, left crash: {1}, up crash: {2}, "
              "down crash: {3}. Reward: {4}, lost game: {5}. Apple x: {6}, "
              "apple y: {7}.".format(info["right_crash"], info["left_crash"], info["up_crash"],
                                     info["down_crash"], info["reward"], info["lost_game"],
                                     info["apple_x"], info["apple_y"]))

        return info

    def get_action(self, action):
        # sending state to agent
        if action == KEY["UP"]:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        elif action == KEY["DOWN"]:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        elif action == KEY["LEFT"]:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        elif action == KEY["RIGHT"]:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        # make the move
        pygame.event.post(event)
    def wait_for_action(self):
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
                    return KEY["EXIT"]
                elif event.key == pygame.K_y:
                    return KEY["YES"]
                elif event.key == pygame.K_n:
                    return KEY["NO"]
            if event.type == pygame.QUIT:
                sys.exit()

    def spawn_apple(self):
        valid_apple = False
        x = 0
        y = 0
        while not valid_apple:
            valid_apple = True
            x = random.randint(0, BOARD_WIDTH - 1)
            y = random.randint(0, BOARD_HEIGHT - 1)
            for segment in self.main_snake.elements:
                if check_collision(segment, Segment(x, y)):
                    valid_apple = False
                    break

        return Apple(x, y, True)
    def rerun(self):
        self.__init__()
    def end_game(self):
        self.running = False
        print("fses")
#        message = self.game_over_font.render("Game Over", 1, pygame.Color("white"))
        #message_play_again = self.play_again_font.render("Restart? Y / N", 1, pygame.Color("green"))
        #self.main_screen.blit(message, (320, 240))
        #self.main_screen.blit(message_play_again, (320 + 12, 240 + 40))

        #pygame.display.flip()
        #pygame.display.update()

#        my_key = self.wait_for_action()


#        print("MY KEY GOT IS: {0}".format(my_key))
        # tu trzeba zmienic bo nie chcemy takiego
        #while my_key != KEY["EXIT"]:
#            if my_key == KEY["YES"]:
#                print("RUNNING GAME!!!!!!")
#                self.rerun()
#            elif my_key == KEY["NO"]:
#                break
            #my_key = self.wait_for_action()
        #sys.exit()

    def draw_score(self):
        score_area = self.score_area_font.render(str(self.score), 1, pygame.Color("white"))
        self.main_screen.blit(self.score_msg, (SCREEN_WIDTH - self.score_msg_size[0] - 60, 10))
        self.main_screen.blit(score_area, (SCREEN_WIDTH - 45, 10))

    def redraw_game(self):
        self.main_screen.fill(self.background_color)
        if self.apple.exists:
            self.apple.draw(self.main_screen, self.apple_image)
        self.main_snake.draw(self.main_screen,self.snake_image)
        self.draw_score()
        pygame.display.flip()
        pygame.display.update()

    def action(self, action_key):
        if action_key == KEY["EXIT"]:
            self.running = False

        # Move snake
        if self.grow_snake:
            self.main_snake.grow()
        if action_key:
            self.main_snake.set_direction(action_key)
        self.main_snake.move()
        return self.last_info

    def run(self, action):
        # Draw game
        self.redraw_game()

        # Check collisions (walls and self)
        if self.main_snake.check_crash():
            self.end_game()

        # Check apple availability
        self.grow_snake = False
        if self.apple.exists:
            if check_collision(self.main_snake.get_head(), self.apple):
                self.grow_snake = True
                self.apple.exists = False
                self.score += 5
                self.apple_eaten = True

        # Spawn apple
        if self.apple_eaten:
            self.apple_eaten = False
            self.apple = self.spawn_apple(self.main_snake)
            print("Wow, you've eaten an apple! Next apple: ({0}, {1})".format(self.apple.x, self.apple.y))
            self.redraw_game()

        # Wait for user input (here goes agent's move)
        #self.main_snake.display_log()
        print("Waiting for input...")
        # Here agent is telling what to do
        # get_order(random.randint(1,4),main_snake,apple)
        self.get_action(action)
        # Waits for our eyes
        time.sleep(0.5)
        key_pressed = self.wait_for_action()
        if key_pressed == "exit":
            self.running = False

        # Move snake
        if self.grow_snake:
            self.main_snake.grow()
        if key_pressed:
            self.main_snake.set_direction(key_pressed)
        self.main_snake.move()
        return self.send_state()

    def send_state(self):
        # Should send double square = 18
        # sends actual state in table of ints
        # apple.x,apple.y, snake.direction, all snake.elements(x,y)
        ret = [self.apple.x, self.apple.y, self.main_snake.direction]
        for e in self.main_snake.elements:
            ret.append(e.x)
            ret.append(e.y)
        return ret



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

    # Game initialization
    game = Game()
    game.run_game()




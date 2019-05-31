import pygame
import random
import time
import os
import sys
import math

from game.Apple import Apple
from game.Segment import Segment
from game.snake import Snake
from game.Variables import *

DISPLAY = True


class Game:
    def __init__(self):
        self.iterations_count = 0
        self.score = 0
        #self.main_snake = Snake(4, 4 )
        self.main_snake = Snake(random.randint(4,11), random.randint(3,4) )
        self.apple_eaten = False
        self.apple = self.spawn_apple()
        self.running = True
        # self.last_info = self.get_info()
        self.grow_snake = False

        pygame.init()
        pygame.display.set_caption("Snake")
        pygame.font.init()
        # pygame.display.iconify()
        random.seed()
        self.main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)
        self.score_font = pygame.font.Font(None, 25)
        self.score_area_font = pygame.font.Font(None, 25)
        self.game_over_font = pygame.font.Font(None, 45)
        self.play_again_font = self.score_area_font
        self.score_msg = self.score_font.render("Score:", 1, pygame.Color("white"))
        self.score_msg_size = self.score_font.size("Score")
        self.background_color = pygame.Color(100, 100, 100)

        image_path = os.path.dirname(__file__)

        self.apple_image = pygame.transform.scale(
            pygame.image.load(os.path.join(image_path, "apple.png")).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_image = pygame.transform.scale(
            pygame.image.load(os.path.join(image_path, "snake_box.jpg")).convert_alpha(),
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
            "apple_y": apple_y_dist,
            "score": self.score,
            "iterations_count": self.iterations_count
        }

        print("\nRight crash: {0}, left crash: {1}, up crash: {2}, "
              "down crash: {3}. Reward: {4}, lost game: {5}. Apple x: {6}, "
              "apple y: {7}, score: {8}, number of iterations {9}".format(info["right_crash"], info["left_crash"],
                                                                          info["up_crash"],
                                                                          info["down_crash"], info["reward"],
                                                                          info["lost_game"],
                                                                          info["apple_x"], info["apple_y"],
                                                                          info["score"], info["iterations_count"]))

        return info

    def get_action(self, action):
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
        # self.get_info()
        self.running = False

    def get_snake_size(self):
        return len(self.main_snake.elements)

    def draw_score(self):
        score_area = self.score_area_font.render(str(self.score), 1, pygame.Color("white"))
        self.main_screen.blit(self.score_msg, (SCREEN_WIDTH - self.score_msg_size[0] - 60, 10))
        self.main_screen.blit(score_area, (SCREEN_WIDTH - 45, 10))

    def redraw_game(self):
        self.main_screen.fill(self.background_color)
        if self.apple.exists:
            self.apple.draw(self.main_screen, self.apple_image)
        self.main_snake.draw(self.main_screen, self.snake_image)
        self.draw_score()
        if DISPLAY:
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
        # print(self.send_state(), action)

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
            self.apple = self.spawn_apple()
            print("Wow, you've eaten an apple! Next apple: ({0}, {1})".format(self.apple.x, self.apple.y))
            self.redraw_game()

        # Wait for user input (here goes agent's move)
        # self.main_snake.display_log()
        self.iterations_count += 1
        # Here agent is telling what to do

        # Waits for our eyes
        #time.sleep(0.2)
        self.get_action(action)
        key_pressed = self.wait_for_action()
        if key_pressed == "exit":
            self.running = False

        if (key_pressed != action):
            print("error when getting key presed", key_pressed, action)

        # Move snake
        if self.grow_snake:
            self.main_snake.grow()
        if key_pressed in range(0, 4):
            self.main_snake.set_direction(key_pressed)
        self.main_snake.move()

        # Check collisions (walls and self)
        if self.main_snake.check_crash():
            self.end_game()

        reward = self.send_reward()
        return (self.send_state(), reward)

    def send_reward(self):
        # reward = 0
        # apple_part =0
        # apple_distance = abs(self.apple.x - self.main_snake.get_head().x) + abs(self.apple.y - self.main_snake.get_head().y)
        # if apple_distance==1:
        #     apple_part= REWARD["EAT"]
        # if self.running:
        #     reward= REWARD["LIVE"] + apple_part
        # else:
        #     reward = REWARD["DEATH"]+ apple_part
        # return reward
        apple_part =0
        if(self.running == False):
             return REWARD["DEATH"]
        apple_distance = abs(self.apple.x - self.main_snake.get_head().x) + abs(self.apple.y - self.main_snake.get_head().y)


        # ------DIFFICULT SCENARIO---------
        if apple_distance == 0:
            apple_part = REWARD["EAT"]
        # ---------------------------------

        # # -------EASIER SCENARIO-----------
        # apple_part = (1-(apple_distance/(BOARD_HEIGHT+BOARD_WIDTH))) * REWARD["EAT"]
        # # ---------------------------------

        return REWARD["LIVE"] + apple_part

    # when snake eats an apple => true
    # that is when the head of the snake is on the apple
    def snake_eating(self):
        return self.apple.x == self.main_snake.get_head().x and self.apple.y == self.main_snake.y

    # Sends state to agent
    # List of collisions (U, R, D L) and apple distances (U, R, D, L)
    def send_state(self):
        collisions = self.check_collisions_all_directions()
        apple_distance = self.check_apple_all_directions()
        if len(collisions) != 4 or len(apple_distance) != 4:
            print(collisions)
            print(apple_distance)
        return collisions + apple_distance

    def check_apple_all_directions(self):
        # distance = [0,0,0,0]
        distance = []

        # snake is eating the apple now  => no reward for that
        if self.snake_eating():
            return [0,0,0,0]

        # UP
        distance.append(self.distance_calc(self.apple.x, self.apple.y,self.main_snake.get_head().x,  self.main_snake.get_head().y-1))
        

        # DOWN
        distance.append(self.distance_calc(self.apple.x,self.apple.y, self.main_snake.get_head().x,  self.main_snake.get_head().y+1))

        # LEFT
        distance.append(self.distance_calc(self.apple.x,self.apple.y, self.main_snake.get_head().x-1,  self.main_snake.get_head().y))

        # RIGHT
        distance.append(self.distance_calc(self.apple.x, self.apple.y,self.main_snake.get_head().x+1,  self.main_snake.get_head().y))

        return distance

    def distance_calc(self, applex, appley, snakex, snakey):
        return abs(applex - snakex) + abs(appley - snakey)



    def check_collisions_all_directions(self):
        collision = []

        # UP
        distance = self.main_snake.get_head().y
        new_head = (self.main_snake.get_head().x, self.main_snake.get_head().y - 1)

        snake_elements_without_tail = self.main_snake.elements[:-1]

        for segment in snake_elements_without_tail:
            if segment.x == new_head[0] and segment.y < self.main_snake.get_head().y:
                distance = min(distance, abs(segment.y - new_head[1]))
        collision.append(distance) 
        
        # DOWN
        distance = BOARD_HEIGHT - self.main_snake.get_head().y - 1
        new_head = (self.main_snake.get_head().x, self.main_snake.get_head().y + 1)
        for segment in snake_elements_without_tail:
            if segment.x == new_head[0] and segment.y > self.main_snake.get_head().y:
                distance = min(distance, abs(segment.y - new_head[1]))
        collision.append(distance)

        # LEFT
        distance = self.main_snake.get_head().x
        new_head = (self.main_snake.get_head().x - 1, self.main_snake.get_head().y)
        for segment in snake_elements_without_tail:
            if segment.y == new_head[1] and segment.x < self.main_snake.get_head().x:
                distance = min(distance, abs(new_head[0] - segment.x))
        collision.append(distance)

        # RIGHT
        distance = BOARD_WIDTH - self.main_snake.get_head().x - 1
        new_head = (self.main_snake.get_head().x + 1, self.main_snake.get_head().y)
        for segment in snake_elements_without_tail:
            if segment.y == new_head[1] and segment.x > self.main_snake.get_head().x:
                distance = min(distance, abs(new_head[0] - segment.x))
        collision.append(distance)

        return collision

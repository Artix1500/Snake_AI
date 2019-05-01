from game.Variables import *
from game.Apple import Apple
from game.Segment import Segment 

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
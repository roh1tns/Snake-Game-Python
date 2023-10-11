import pygame
import time
import random
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (243, 240, 255)
OBSTACLES = 0


class Obstacle:
    def __init__(self, parent_screen, count):
        self.count = count
        self.parent_screen = parent_screen
        self.obstacle = pygame.image.load("resources/Obstacle.png").convert()
        self.x = []
        self.y = []
        self.x.append(random.randint(0, 24)*SIZE)
        self.y.append(random.randint(0, 18)*SIZE)

    def draw(self):
        for i in range(0, self.count):
            self.parent_screen.blit(self.obstacle, (self.x[i], self.y[i]))
        pygame.display.flip()

    def new_obstacle(self):
        self.x.append(random.randint(0, 24) * SIZE)
        self.y.append(random.randint(0, 18) * SIZE)
        self.count += 1


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 18)*SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block1.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 760))

        pygame.mixer.init()
        # self.play_background_music()
        self.surface.fill((243, 240, 255))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.obstacle = Obstacle(self.surface, 1)
        self.obstacle.draw()
        self.time_step = 0.2
        self.score = self.snake.length


    def play_background_music(self):
        pygame.mixer.music.load("resources/BGM.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.obstacle.draw()
        pygame.display.flip()

        # Snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.apple.move()
            while True:
                for i in range(0, self.obstacle.count):
                    if self.apple.x == self.obstacle.x[i] and self.apple.y == self.obstacle.y[i]:
                        self.apple.move()
                else:
                    break

            self.score += 1
            self.snake.increase_length()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"

        # Snake hitting boundary
        if self.snake.x[0] > 1000 or self.snake.x[0] < 0 or self.snake.y[0] > 760 or self.snake.y[0] < 0:
            self.play_sound("crash")
            raise "Game over"

        # Snake hitting obstacle
        for i in range(0, self.obstacle.count):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.obstacle.x[i], self.obstacle.y[i]):
                self.play_sound("crash")
                raise "Game over"

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2  and x1 < x2+ SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'SCORE: {self.score - 1}', True, (95, 61, 196))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'GAME OVER!!! SCORE: {self.snake.length - 1}', True, (95, 61, 196))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press ENTER to play again. Press ESC to Exit!", True, (95, 61, 196))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.obstacle = Obstacle(self.surface, 1)
        self.time_step = 0.2
        self.obstacle.x = [self.obstacle.x[0]]
        self.obstacle.y = [self.obstacle.y[0]]
        self.score = 1

    def run(self):

        running = True
        pause = False
        iteration = 0

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            if iteration % 100 == 0 and iteration > 1:
                self.obstacle.new_obstacle()

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            if iteration % 300 == 0 and iteration > 1 and self.time_step > 0.05:
                self.time_step -= 0.05

            time.sleep(self.time_step)
            iteration += 1


if __name__ == "__main__":
    game = Game()
    game.run()


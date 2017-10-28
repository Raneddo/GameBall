import pygame
from random import randint

import sys

size = width, height = 320, 240
bg_color = 33, 33, 33


class Button:
    def __init__(self):
        font = pygame.font.SysFont('Ubuntu', 15)
        self.surface = pygame.Surface((60, 25))
        self.surface.fill((0, 0, 0))
        self.surface.blit(font.render('Pause', 1, (255, 0, 0)), (11, 4))
        self.geometry = (260, 0)

    def get_surface(self):
        return self.surface


class Ball:
    def __init__(self):
        self.speed = [2, 2]
        self.ball = pygame.image.load('basketball.png')
        self.geometry = self.ball.get_rect()

    def shift(self):
        self.geometry = self.geometry.move(self.speed)
        if self.geometry.left <= 0 or self.geometry.right >= width:
            self.speed[0] *= -1
        if self.geometry.top <= 0 or self.geometry.bottom >= height:
            self.speed[1] *= -1

    def set_position(self, pos):
        self.geometry.x = pos[0] - self.geometry.width // 2
        self.geometry.y = pos[1] - self.geometry.height // 2

    def move_key(self, key):
        key = chr(key)
        if key == 'w':
            self.geometry.top -= 10
        elif key == 's':
            self.geometry.top += 10
        if key == 'a':
            self.geometry.left -= 10
        elif key == 'd':
            self.geometry.left += 10


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    b = Ball()
    button = Button()
    w_close = False
    time = pygame.time.get_ticks()
    while not w_close:
        # --- обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                w_close = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                b.set_position(pos)
            if event.type == pygame.KEYDOWN:
                b.move_key(event.key)

        # --- игровая логика ---
        b.shift()

        # --- отрисовка картинки ---
        screen.fill(bg_color)
        font = pygame.font.SysFont('Ubuntu', 15)
        screen.blit(font.render('Time is ' + str(int(pygame.time.get_ticks() - time)//1000), 1, (255, 0, 0)), (15, 15))
        screen.blit(b.ball, b.geometry)
        screen.blit(button.surface, button.geometry)
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


if __name__ == "__main__":
    main()

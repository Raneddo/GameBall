#!/usr/bin/python3

import pygame
from random import randint
from easygui import enterbox, msgbox

import sys

size = width, height = 320, 240
bg_color = 33, 33, 33
game_stop = False

about = \
"""
I'm very sorry for my code. But I can do only 
this because there was no time. I hope, that next
code will be better.

And now about this program.
It's game. You start with one ball and it 'run' on field.
When ball concerns walls it changes self direction.
You can move ball with mouse. The Ball will be where you click.
On playing field are located 3 buttons:
1) "Pause" -- pausing game, but "mousemoving" isn't pausing
2) "Rating" -- show last 10 plays (name : seconds)
3) "Add ball" -- about it next chapter.

When you click to button "Add ball", real game is starting.
You should control new ball with "WASD".
When first ball concerns new, game is finishing.
You shold your name, and you results turn out to be in rating table.
Then you can see rating with pressing button "Rating"
Note, real time starts when do you press "Add ball"
Then you can only close the game and start again.

                    Have fun!
                    
                    
                                    Created by Raneddo
                                    GNU/GPL v3.0
                                    Thanks PyGame and easygui for libs
                                    And thanks informatics.ru
"""


class Button:
    def __init__(self, button_text='', button_size=(60, 25), geometry=(0, 0), text_geometry=(11, 4)):
        font = pygame.font.SysFont('Ubuntu', 15)
        self.surface = pygame.Surface(button_size)
        self.surface.fill((0, 0, 0))
        self.surface.blit(font.render(button_text, 1, (255, 0, 0)), text_geometry)
        self.geometry = geometry
        self.see = True

    def get_surface(self):
        return self.surface


class Ball:
    def __init__(self, img='basketball.png'):
        self.go = True
        self.speed = [2, 2]
        self.ball = pygame.image.load(img)
        self.geometry = self.ball.get_rect()

    def shift(self):
        if not self.go:
            return
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


def mouse_in_square_surface(surface, mouse_pos):
    size_s = surface.surface.get_size()
    if surface.geometry[0] <= mouse_pos[0] and surface.geometry[1] <= mouse_pos[1] and surface.geometry[0] + \
            size_s[0] >= mouse_pos[0] and surface.geometry[1] + size_s[1] >= mouse_pos[1]:
        return True
    else:
        return False


def get_name():
    return enterbox('After writing do you can see the rating\nEnter your name:', title='Enter your name')


def main():
    global game_stop
    new_time = 0
    pygame.init()
    screen = pygame.display.set_mode(size)
    b = Ball()
    active_ball = b
    add_ball = Button('Add ball', (60, 25), (260, 215), (3, 4))
    button = Button('Pause', (60, 25), (260, 0), (11, 4))
    rating = Button('Rating', (60, 25), (0, 215), (8, 4))
    w_close = False
    time = pygame.time.get_ticks()
    while not w_close:
        if game_stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    w_close = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if mouse_in_square_surface(rating, pos):
                        message = '10 last records:\n\n'
                        with open('records.txt', 'r') as f:
                            text = f.readlines()
                            if not len(text):
                                message = 'Rating is empty'
                            else:
                                count = 1
                                for i in text[::-1]:
                                    if count > 10:
                                        break
                                    temp = i.split(';')
                                    message += str(count) + ') ' + temp[0] + ' : ' + temp[1] + '\n'
                                    count += 1
                        msgbox(title='Rating', msg=message, ok_button='Continue')
            pygame.time.wait(100)
            continue

# --- обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                w_close = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if mouse_in_square_surface(button, pos):
                    b.go = not b.go
                elif mouse_in_square_surface(add_ball, pos) and add_ball.see is True:
                    add_ball.see = False
                    nb = Ball('magic_ball.png')
                    active_ball = nb
                    new_time = pygame.time.get_ticks()
                elif mouse_in_square_surface(rating, pos):
                    game_stop = True
                    message = '10 last records:\n\n'
                    with open('records.txt', 'r') as f:
                        text = f.readlines()
                        if not len(text):
                            message = 'Rating is empty'
                        else:
                            count = 1
                            for i in text[::-1]:
                                if count > 10:
                                    break
                                temp = i.split(';')
                                message += str(count) + ') ' + temp[0]+' : ' + temp[1] + '\n'
                                count += 1
                    msgbox(title='Rating', msg=message, ok_button='Continue')
                    game_stop = False
                else:
                    b.set_position(pos)
            if event.type == pygame.KEYDOWN:
                active_ball.move_key(event.key)
        if add_ball.see is False and \
                (((b.geometry.left - nb.geometry.left)**2 + (b.geometry.top - nb.geometry.top)**2)**0.5 < 100):
            """
            if nb.geometry[0] < b.geometry[0]:
                b.speed[0] = 2
            else:
                b.speed[0] = -2
            if nb.geometry[1] < b.geometry[1]:
                b.speed[1] = 2
            else:
                b.speed[1] = -2
            """
            game_stop = True
            name = get_name()
            if name is not None and name != '':
                with open('records.txt', 'a') as f:
                    f.write(name+';'+str((pygame.time.get_ticks()-new_time)//1000)+'\n')

        # --- игровая логика ---
        b.shift()

        # --- отрисовка картинки ---
        screen.fill(bg_color)
        font = pygame.font.SysFont('Ubuntu', 15)
        screen.blit(button.surface, button.geometry)
        screen.blit(rating.surface, rating.geometry)
        if add_ball.see is True:
            screen.blit(add_ball.surface, add_ball.geometry)
        else:
            screen.blit(nb.ball, nb.geometry)
        screen.blit(b.ball, b.geometry)
        screen.blit(font.render('Time is ' + str(int(pygame.time.get_ticks() - time) // 1000), 1, (255, 0, 0)),
                    (15, 15))
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if  sys.argv[1] in ("--about", '-a'):
            print(about)
        else:
            print('For info about prog, enter -a or --about')
    else:
        main()


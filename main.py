import random
import sys
import pygame
from pygame.locals import *


FPS = 30
WINDOWWIDTH = 289
WINDOWHEIGHT = 511
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BASE_Y = WINDOWHEIGHT * 0.8
GAME_IMAGES = {}
GAME_SOUNDS = {}
PLAYER = 'Images/Flappy Bird.png'
BACKGROUND = 'Images/City Skyline.png'
PIPE = 'Images/Super Mario pipe.png'


def welcomeScreen():

    player_x = int(WINDOWWIDTH / 5)
    player_y = int((WINDOWHEIGHT - GAME_IMAGES['player'].get_height()) / 2)
    message_x = int((WINDOWWIDTH - GAME_IMAGES['message'].get_width()) / 2)
    message_y = int(WINDOWHEIGHT * 0.13)
    base_x = 0
    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_IMAGES['background'], (0, 0))
                SCREEN.blit(GAME_IMAGES['player'], (player_x, player_y))
                SCREEN.blit(GAME_IMAGES['message'], (message_x, message_y))
                SCREEN.blit(GAME_IMAGES['base'], (base_x, BASE_Y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    player_x = int(WINDOWWIDTH / 5)
    player_Y = int(WINDOWWIDTH / 2)
    basex = 0


    new_pipe1 = get_pipe()
    new_pipe2 = get_pipe()


    upper_pipes = [
        {'x': WINDOWWIDTH + 200, 'y': new_pipe1[0]['y']},
        {'x': WINDOWWIDTH + 200 + (WINDOWWIDTH / 2), 'y': new_pipe2[0]['y']},
    ]

    lower_pipes = [
        {'x': WINDOWWIDTH + 200, 'y': new_pipe1[1]['y']},
        {'x': WINDOWWIDTH + 200 + (WINDOWWIDTH / 2), 'y': new_pipe2[1]['y']},
    ]

    pipe_vel_x = -4

    player_vel_y = -9
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1

    player_flap_accv = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_Y > 0:
                    player_vel_y = player_flap_accv
                    player_flapped = True


        crash_test = collision(player_x, player_Y, upper_pipes,
                              lower_pipes)
        if crash_test:
            return


        player_mid_pos = player_x + GAME_IMAGES['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + GAME_IMAGES['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score}")


        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        player_height = GAME_IMAGES['player'].get_height()
        player_Y = player_Y + min(player_vel_y, BASE_Y - player_Y - player_height)


        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x


        if 0 < upper_pipes[0]['x'] < 5:
            newpipe = get_pipe()
            upper_pipes.append(newpipe[0])
            lower_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upper_pipes[0]['x'] < -GAME_IMAGES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)


        SCREEN.blit(GAME_IMAGES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_IMAGES['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            SCREEN.blit(GAME_IMAGES['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
        SCREEN.blit(GAME_IMAGES['base'], (basex, BASE_Y))
        SCREEN.blit(GAME_IMAGES['player'], (player_x, player_Y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += GAME_IMAGES['numbers'][digit].get_width()
        xoffset = (WINDOWWIDTH - width) / 2

        for digit in my_digits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit], (xoffset, WINDOWHEIGHT * 0.12))
            xoffset += GAME_IMAGES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def collision(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > BASE_Y - 25 or player_y < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upper_pipes:
        pipe_height = GAME_IMAGES['pipe'][0].get_height()
        if (player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()):

            return True

    for pipe in lower_pipes:
        if (player_y + GAME_IMAGES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < \
                GAME_IMAGES['pipe'][0].get_width():

            return True

    return False


def get_pipe():

    pipe_height = GAME_IMAGES['pipe'][0].get_height()
    offset = WINDOWHEIGHT / 3
    y2 = offset + random.randrange(0, int(WINDOWHEIGHT - GAME_IMAGES['base'].get_height() - 1.2 * offset))
    pipe_x = WINDOWWIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_IMAGES['numbers'] = (
        pygame.image.load('Images/0.png').convert_alpha(),
        pygame.image.load('Images/1.png').convert_alpha(),
        pygame.image.load('Images/2.png').convert_alpha(),
        pygame.image.load('Images/3.png').convert_alpha(),
        pygame.image.load('Images/4.png').convert_alpha(),
        pygame.image.load('Images/5.png').convert_alpha(),
        pygame.image.load('Images/6.png').convert_alpha(),
        pygame.image.load('Images/7.png').convert_alpha(),
        pygame.image.load('Images/8.png').convert_alpha(),
        pygame.image.load('Images/9.png').convert_alpha(),
    )

    GAME_IMAGES['message'] = pygame.image.load('Images/title.png').convert_alpha()
    GAME_IMAGES['base'] = pygame.image.load('Images/Stone Floor.png').convert_alpha()
    GAME_IMAGES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                           pygame.image.load(PIPE).convert_alpha()
                           )



    GAME_IMAGES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeScreen()




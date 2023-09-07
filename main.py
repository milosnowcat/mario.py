# TODO hacer un juego en pygame inspirado en Mario,
# tendra un nivel, conteo de puntos, mecanicas de salto,
# movimiento horizontal y vertical.
# Usará sprites gratuitos de itch.io

import pygame
from pygame.locals import *

pygame.init()

screen_width = 960
screen_height = 540

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mario')

tile_size = 60

bg_img = pygame.image.load('assets/img/background.png')

def draw_grid():
    for line in range(0,17):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

run = True
while run:
    screen.blit(bg_img, (0, 0))

    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()

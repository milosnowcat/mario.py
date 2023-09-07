# TODO hacer un juego en pygame inspirado en Mario,
# tendra un nivel, conteo de puntos, mecanicas de salto,
# movimiento horizontal y vertical.
# Usará sprites gratuitos de itch.io

import pygame
from pygame.locals import *

pygame.init()

screen_width = 650
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mario')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

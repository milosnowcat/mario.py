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

background = pygame.image.load('assets/img/background.png')
bg_img = pygame.transform.scale(background, (screen_width, screen_height))

def draw_grid():
    for line in range(0,17):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player():
    def __init__(self, x, y):
        img = pygame.image.load('assets/img/dino.png')
        self.image = pygame.transform.scale(img, (60, 68))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
    
    def update(self):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 3
        if key[pygame.K_RIGHT]:
            dx += 3

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        # collisions

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect)

class World():
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('assets/img/dirt.png')
        grass_img = pygame.image.load('assets/img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1],
    [1,0,0,0,0,0,0,2,0,2,0,2,2,1,1,1],
    [1,0,0,0,2,2,0,0,0,0,0,1,1,1,1,1],
    [1,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

player = Player(120, screen_height - 120)
world = World(world_data)

run = True
while run:
    screen.blit(bg_img, (0, 0))

    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()

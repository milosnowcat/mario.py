# TODO hacer un juego en pygame inspirado en Mario,
# tendra un nivel, conteo de puntos, mecanicas de salto,
# movimiento horizontal y vertical.
# Usará sprites gratuitos de itch.io

import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 960
screen_height = 540

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mario')

tile_size = 60
game_over = 0

background = pygame.image.load('assets/img/background.png')
bg_img = pygame.transform.scale(background, (screen_width, screen_height))
img_restart = pygame.image.load('assets/img/button_restart.png')

def draw_grid():
    for line in range(0,17):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
        
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)
    
    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 3
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.image_idle_right
                if self.direction == -1:
                    self.image = self.image_idle_left

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10

            dy += self.vel_y
            self.in_air = True

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y > 0:
                        dy = tile[1].top - self.rect.bottom
                        self.in_air = False
                else:
                    if self.vel_y < 0:
                        if self.direction == 1:
                            self.image = self.image_jump_right
                        if self.direction == -1:
                            self.image = self.image_jump_left

            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel_y = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
                dx = 0
            if self.rect.left < 0:
                self.rect.left = 0
                dx = 0
        elif game_over == -1:
            if self.direction == 1:
                self.image = self.image_dead_right
            if self.direction == -1:
                self.image = self.image_dead_left

        screen.blit(self.image, self.rect)

        return game_over
    
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        img_idle_right = pygame.image.load('assets/img/dino.png')
        img_idle_right = pygame.transform.scale(img_idle_right, (60, 68))
        img_idle_left = pygame.transform.flip(img_idle_right, True, False)
        self.image_idle_right = img_idle_right
        self.image_idle_left = img_idle_left

        img_jump_right = pygame.image.load('assets/img/dino_jump.png')
        img_jump_right = pygame.transform.scale(img_jump_right, (60, 68))
        img_jump_left = pygame.transform.flip(img_jump_right, True, False)
        self.image_jump_right = img_jump_right
        self.image_jump_left = img_jump_left

        img_dead_right = pygame.image.load('assets/img/dino_dead.png')
        img_dead_right = pygame.transform.scale(img_dead_right, (60, 68))
        img_dead_left = pygame.transform.flip(img_dead_right, True, False)
        self.image_dead_right = img_dead_right
        self.image_dead_left = img_dead_left

        for num in range(1, 7):
            img_right = pygame.image.load(f'assets/img/dino_walk{num}.png')
            img_right = pygame.transform.scale(img_right, (60, 72))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.image_idle_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

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
                if tile == 3:
                    spike = Spike(col_count * tile_size + (tile_size / 4), row_count * tile_size + 30)
                    spike_group.add(spike)
                if tile == 4:
                    water = Water(col_count * tile_size, row_count * tile_size + (tile_size / 2))
                    water_group.add(water)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/spike.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/water.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,2,0,0,2,2,2],
    [0,0,0,0,0,0,2,2,4,4,4,4,4,1,1,1],
    [0,0,0,3,2,2,1,1,0,0,0,0,0,1,1,1],
    [2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
]

player = Player(0, screen_height - 120)
spike_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
world = World(world_data)
restart_button = Button(screen_width / 2 - 64, screen_height / 2 - 64, img_restart)

run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    world.draw()
    spike_group.draw(screen)
    water_group.draw(screen)
    game_over = player.update(game_over)

    if game_over == -1:
        if restart_button.draw():
            player.reset(0, screen_height - 120)
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()

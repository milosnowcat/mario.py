#                      .                    .                           
#                 :-:--=:-:::.             :=-**##*=:                   
#                  :=----------.         .-%@@@@@@@@@%:                 
#                 :-------------:        :@@@@@@@@@@@@%.                
#                :-=-----------==:       +@@@@@@@@@@@@@#                
#              .------------=------.     =@@@@@@@@@@@@@#                
#               :=-=-------===-=--      .+%@@@@@@@@@@@#=                
#                --=--------==-=-.       -*%@@@@@@@@@*-.                
#                   ::----===+-             .#%@@@@*.                   
#                      -+++=: .               :+##+                     
#                     -+=====.              .=%@@%%%#=                  
#                  :-----------:.        :+#%%%@@@@@%@%+-               
#                -----------------      -%%%%%@@@%@@%%@%%*              
#               .-==----------==--:     #%%%@%@@@@@@@@@@%%.             
#               :-=+----------*=---    =%%%@@%%@@@%%@@@%%%=             
#               ---=----------*----:  .#%%%@@%%@@@%@%@@%%%%             
#              :-===----------+=---=  -#%%%@@%%@%@%@%@@%%%%=            
#                --=----------=#==+.   ==+%@@%%@@@%@%@@*++.             
#                --=-----------*=---  :===#@@%%@@@%@%%%--=              
#                -==-----------++--=  ---:#@%@@@%%%@@@%--=              
#                -=------------=:--=. =-- %@%%%%%%@%%%@=-=              
#               .-+-------------.:---.--: %%%%%%%%@%%@@+==              
#               :-++*++++++*+***. --=+--  *###########**-=              
#               --*+++++++++*+++: :--*-: :------=------*-=              
#               =-*++++++++*+***- .--*-. :-------------+-=              
#              .--*+++=+*++*+***+ :==*=: -------=------===:             
#              :=+++++==+++*++**+ -*++=. -------+-------+=:             
#               -++++=+==**+++***  :-:   -------+-------+.              
#                -+++=++=****+**#        -------+=------=               
#                .++==*=---=*+**+        =------+*------=               
#                 ----=    :---=          ====-.::+====                 
#            :**#==---=:   ----= ..   .:::=--=+*%#*--=+***. .--:..      
#            .=+**#=--==   :=--=%@*:.-=+%%*--=: ::+=--+***+=#@%*-=-::.  
#                :+=--=. :::=--=:.-*#%*--=*---+-+**=--=--=+**+*=**%@%=  
#                  =--= .#%%=--=.  +*#%#= +---#%++#=---.+%@%+  .+++*+-  
#                  ====   .:+===:   -==+= :===*+: -==== .--:.      ..   
#                  =--=     ----:         .----   :=---                 
#                  ----     :---:         .=---   .=---                 
#                  ----     :---:         .=---    =---                 
#                  ---:     :---:         .=---    +---                 
#                  +##%.    =*##-         -%%#:    %%%#                 
#                 :@@@@-    #@@@+         %@@@*   :@@@%:                
#                 .====.    -++=:         =+==-    --==.                

# @milosnowcat

# Tiles from https://bayat.itch.io/platform-game-assets
# Character from https://arks.itch.io/dino-characters
# Sound effects from https://jdwasabi.itch.io/8-bit-16-bit-sound-effects-pack
# Music from https://chippy01302.itch.io/chippy-music-pack

import pygame
from pygame.locals import *
import utils
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 960
screen_height = 540

font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 70)
font_score = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 30)
black = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mario')

tile_size = 60
game_over = 0
main_menu = True
level = 1
score = 0
win = False

background = pygame.image.load('assets/img/background.png')
bg_img = pygame.transform.scale(background, (screen_width, screen_height))
img_restart = pygame.image.load('assets/img/button_restart.png')
img_start = pygame.image.load('assets/img/button_start.png')
img_exit = pygame.image.load('assets/img/button_exit.png')

pygame.mixer.music.load('assets/audio/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('assets/audio/jump.wav')
jump_fx.set_volume(0.5)
dead_fx = pygame.mixer.Sound('assets/audio/dead.wav')
dead_fx.set_volume(0.5)

def draw_text(text, font, color, x, y):
    """
    The function `draw_text` takes in parameters for text, font, color, x and y coordinates, and renders
    the text onto the screen at the specified coordinates.
    
    :param text: The text parameter is a string that represents the text you want to draw on the screen
    :param font: The font parameter is the font object that you want to use for rendering the text. It
    should be a pygame.font.Font object
    :param color: The color parameter is the color of the text that will be drawn on the screen. It can
    be specified using RGB values or by using predefined color names from the pygame library, such as
    pygame.Color('red') or pygame.Color(255, 0, 0)
    :param x: The x parameter represents the x-coordinate of the top-left corner of the text on the
    screen
    :param y: The y parameter in the draw_text function represents the vertical position of where the
    text will be drawn on the screen. It determines the distance from the top of the screen to the
    baseline of the text
    """
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def next_level(level):
    """
    The function "next_level" resets the game environment and player position for the next level.
    
    :param level: The level parameter is an integer that represents the current level of the game
    :return: the game data for the next level.
    """
    spike_group.empty()
    water_group.empty()
    chest_group.empty()
    coin_group.empty()

    game_data = utils.worlds(level)

    player.reset(game_data[1][0], game_data[1][1])

    return game_data

# The Button class represents a clickable button with an image that can be drawn on the screen and
# detects when it is clicked.
class Button():
    def __init__(self, x, y, image):
        """
        The function initializes an object with given coordinates and an image, and sets the initial
        state of the object.
        
        :param x: The x-coordinate of the object's position on the screen
        :param y: The y parameter represents the y-coordinate of the object's position on the screen
        :param image: The "image" parameter is the image that will be displayed for the object. It is
        passed as an argument to the constructor when creating an instance of the class
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        """
        The function checks if the mouse is clicked on a specific object and returns a boolean value
        indicating whether an action should be performed.
        :return: the value of the variable "action".
        """
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

# The Player class represents a player character in a game, with methods for updating its position and
# handling user input.
class Player():
    def __init__(self, x, y):
        """
        The above function is a constructor that initializes the object with the given x and y values.
        
        :param x: The x parameter is used to initialize the x-coordinate of an object
        :param y: The parameter "y" is a variable that represents the y-coordinate of a point
        """
        self.reset(x, y)
    
    def update(self, game_over):
        """
        The `update` function updates the position and behavior of a game character based on user input
        and game conditions.
        
        :param game_over: The parameter "game_over" is a variable that indicates the current state of
        the game. It is used to control the player's movement and actions based on whether the game is
        over or not. If game_over is 0, the player can move and perform actions. If game_over is -1
        :return: The variable `game_over` is being returned.
        """
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
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
                dead_fx.play()

            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1
                dead_fx.play()
            
            if pygame.sprite.spritecollide(self, chest_group, False):
                game_over = 1

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0
                self.in_air = False
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
        """
        The `reset` function initializes the attributes of a Dino object in a game, including loading
        and scaling images, setting the initial position and velocity, and setting flags for jumping and
        direction.
        
        :param x: The x parameter represents the x-coordinate of the position where the object will be
        reset
        :param y: The parameter `y` represents the y-coordinate of the position where the object will be
        reset
        """
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

# The World class is responsible for creating and drawing tiles based on the data provided.
class World():
    def __init__(self, data):
        """
        The function initializes a list of tiles based on the given data, where each tile is represented
        by an image and its corresponding rectangle.
        
        :param data: The "data" parameter is a 2D list that represents the layout of tiles in a game
        level. Each element in the list represents a tile, and its value determines the type of tile
        """
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
                    spike = Spike(col_count * tile_size + (tile_size / 2), row_count * tile_size + tile_size)
                    spike_group.add(spike)
                if tile == 4:
                    water = Water(col_count * tile_size, row_count * tile_size + (tile_size / 2))
                    water_group.add(water)
                if tile == 5:
                    chest = Chest(col_count * tile_size, row_count * tile_size)
                    chest_group.add(chest)
                if tile == 6:
                    coin = Coin(col_count * tile_size + (tile_size / 2), row_count * tile_size + (tile_size / 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        """
        The function iterates through a list of tiles and blits them onto the screen.
        """
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# The Spike class is a subclass of pygame.sprite.Sprite that represents a spike object with an image
# and a position.
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        The function initializes a sprite object with an image and sets its position.
        
        :param x: The x parameter represents the x-coordinate of the center of the sprite
        :param y: The y parameter represents the y-coordinate of the center of the sprite
        """
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/spike.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# The Water class is a sprite that represents a body of water in a game, with a specified position and
# image.
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        This function initializes a sprite object with an image and sets its position.
        
        :param x: The x parameter represents the x-coordinate of the sprite's position on the screen. It
        determines the horizontal position of the sprite
        :param y: The parameter `y` represents the y-coordinate of the sprite's position on the screen
        """
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/water.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# The `Chest` class represents a chest sprite in a game, with a specified position and image.
class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        The function initializes a sprite object with an image and sets its position on the screen.
        
        :param x: The x parameter represents the x-coordinate of the chest's position on the screen
        :param y: The parameter "y" represents the y-coordinate of the chest's position on the screen
        """
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/chest.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# The Coin class represents a coin object in a game and initializes its image and position.
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        The function initializes a sprite object with an image of a coin and sets its position.
        
        :param x: The x parameter represents the x-coordinate of the center of the coin sprite on the
        screen
        :param y: The parameter `y` represents the y-coordinate of the center of the coin sprite
        """
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size / 2, tile_size / 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

game_data = utils.worlds(level)

player = Player(game_data[1][0], game_data[1][1])

spike_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

world = World(game_data[0])

restart_button = Button(screen_width / 2 - 32, screen_height / 2 - 32, img_restart)
start_button = Button(screen_width / 2 - 128, screen_height / 2 - 32, img_start)
exit_button = Button(screen_width / 2 + 64, screen_height / 2 - 32, img_exit)

# The above code is a game loop written in Python using the Pygame library. It sets up a game window,
# handles user input, updates game objects, and renders them on the screen.
run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
        if win:
            draw_text('YOU WIN!', font, black, screen_width / 2 - (screen_width / 4) , screen_height / 2 - (screen_height / 4))
    else:
        world.draw()
        spike_group.draw(screen)
        water_group.draw(screen)
        chest_group.draw(screen)
        coin_group.draw(screen)
        game_over = player.update(game_over)
        draw_text('X' + str(score), font_score, black, tile_size, tile_size / 4)

        if game_over == 0:
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()

        if game_over == -1:
            pygame.mixer.music.stop()

            if restart_button.draw():
                game_data = next_level(level)
                world = World(game_data[0])
                game_over = 0
                score = 0
                pygame.mixer.music.play(-1, 0.0, 5000)

            draw_text('GAME OVER!', font, black, screen_width / 2 - (screen_width / 3) , screen_height / 2 - (screen_height / 4))
        
        if game_over == 1:
            level += 1
            if level <= utils.total():
                game_data = next_level(level)
                world = World(game_data[0])
                game_over = 0
            else:
                level = 1
                game_data = next_level(level)
                world = World(game_data[0])
                game_over = 0
                main_menu = True
                win = True
                score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()

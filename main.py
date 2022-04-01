# imports
from time import time
import pygame
import os
import time
import random

# initialize font
pygame.font.init()

# setup window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat and Mouse")

# load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# load lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
# scale the image to fill the entire window
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)) 

# abstract ship class to share attributes between the two kinds of ships.
class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50), 0)

# main function
def main():
    # variables
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("sans serif", 50)
    player_vel = 5 # velocity for moving character
    
    ship = Ship(350, 375)
    
    clock = pygame.time.Clock()



    def redraw_window():
        # draw image as a surface starting from the top left
        WIN.blit(BG, (0, 0))
        
        # draw labels or text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # add labels to screen
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width()- 10, 10))

        # draw ship
        ship.draw(WIN)
        # refresh the display
        pygame.display.update()

    # loop to run the game.
    while run:
        clock.tick(FPS)
        redraw_window()

        # check if a quit event has occured
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: #move left
            ship.x -= player_vel
        if keys[pygame.K_RIGHT]: #move right
            ship.x += player_vel
        if keys[pygame.K_UP]: #move up
            ship.y -= player_vel
        if keys[pygame.K_DOWN]: #move down
            ship.y += player_vel
main()
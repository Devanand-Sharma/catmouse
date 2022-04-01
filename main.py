# imports
from pickle import TRUE
from time import time
from turtle import width
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
MICE = pygame.image.load(os.path.join("assets", "Mouse.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# player ship
CAT = pygame.image.load(os.path.join("assets", "Cat.png"))

# background
# scale the image to fill the entire window
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)) 


# abstract class to share attributes between cat and mouse.
class Character:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.character_img = None

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.character_img = CAT
        self.mask = pygame.mask.from_surface(self.character_img)

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.character_img = MICE
        self.mask = pygame.mask.from_surface(self.character_img)
    
    def move(self, vel):
        self.y += vel
    
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# main function
def main():
    # variables
    run = True
    FPS = 60
    level = 0
    lives = 20
    main_font = pygame.font.SysFont("sans serif", 50)
    lost_font = pygame.font.SysFont("sans serif", 60)
    player_vel = 20 # velocity for moving character
    enemies = []
    wave_length = 5
    enemy_vel = 4
    player = Player(350, 350)
    
    clock = pygame.time.Clock()

    lost = False

    lost_count = 0



    def redraw_window():
        # draw image as a surface starting from the top left
        WIN.blit(BG, (0, 0))
        
        # draw labels or text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # add labels to screen
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width()- 10, 10))

        # draw the mice
        for enemy in enemies:
            enemy.draw(WIN)

        # draw Cat
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


        # refresh the display
        pygame.display.update()

    # loop to run the game.
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue


        if len(enemies) == 0:
            level += 1
            if enemy_vel < 20:
                enemy_vel += 0.5
            if wave_length < 40:
                wave_length += 1

            for i in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500, -100))
                enemies.append(enemy)
        # check if a quit event has occured
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel + 122 > 0: #move left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_height() - 122 < WIDTH: #move right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel + 122 > 0: #move up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_width() - 122 < HEIGHT: #move down
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if collide(enemy, player):
                enemies.remove(enemy)

            if enemy.y + enemy.get_height() - 35 > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        

def menu():
    menu_font = pygame.font.SysFont("sans serif", 50)
    run = True

    while run:
        WIN.blit(BG, (0, 0))
        menu_label1 = menu_font.render("Mice Gone Mad", 1, (255, 0, 0))
        menu_label2 = menu_font.render("Press the left mouse button to start!", 1, (255, 255, 255))
        menu_label3 = menu_font.render("By: Devanand Sharma", 1, (0, 255, 0))
        WIN.blit(menu_label1, (WIDTH / 2 - menu_label1.get_width()/2, 350 - 45))
        WIN.blit(menu_label2, (WIDTH / 2 - menu_label2.get_width()/2, 350))
        WIN.blit(menu_label3, (WIDTH / 2 - menu_label3.get_width()/2, 350 + 45))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()            
    pygame.quit()


menu()
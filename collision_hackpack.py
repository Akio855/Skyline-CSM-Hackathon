import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('My Game')

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()

        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        self.walls = None

    def change_speed(self, x_diff, y_diff):
        self.change_x = x_diff
        self.change_y = y_diff
    
    def update(self, pressed_keys):
        not_moving = True
        if pressed_keys[K_w]:
            self.change_speed(0, -3)
            not_moving = False
        if pressed_keys[K_a]:
            self.change_speed(-3, 0)
            not_moving = False
        if pressed_keys[K_s]:
            self.change_speed(0, 3)
            not_moving = False
        if pressed_keys[K_d]:
            self.change_speed(3, 0)
            not_moving = False
        if not_moving:
            self.change_speed(0,0)

        self.rect.x += self.change_x
        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in collide_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        self.rect.y += self.change_y
        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in collide_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])

        self.image.fill((50, 50, 255))
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x


clock = pygame.time.Clock()

all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

player = Player(50, 50)
all_sprite_list.add(player)

wall1 = Wall(100, 0, 10, 200)
wall_list.add(wall1)
all_sprite_list.add(wall1)

player.walls = wall_list

running = True
while running == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    pressed_keys = pygame.key.get_pressed()

    all_sprite_list.update(pressed_keys)
    #player.update(pressed_keys)

    screen.fill((255,255,255))
    all_sprite_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
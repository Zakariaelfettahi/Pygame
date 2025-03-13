import pygame
import math
import constants

class Character():
    def __init__(self,x,y, health, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0
        self.running = True
        self.health = health
        self.alive = True
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,constants.TILE_SIZE, constants.TILE_SIZE)
        self.rect.center = (x, y)
        self.coins = 0
    
    def move(self,dx,dy):
        #flip image if going left
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        #normalize the diagonal movement
        if dx !=0 and dy !=0:
            dx = dx/1.414
            dy = dy/1.414
        self.rect.x += dx
        self.rect.y += dy

        # running animation
        self.running = True
        if dx == 0 and dy == 0:
            self.running = False

    def update(self):
        #check if character is alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

        if self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self,area):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            area.blit(flipped_image, (self.rect.x, self.rect.y - constants.OFFSET*constants.SCALER))
        else:
            area.blit(flipped_image, self.rect)
        pygame.draw.rect(area, constants.RED , self.rect, 1)


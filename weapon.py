import pygame
import math

class Weapon():
    def __init__(self, image):
        self.original_image = image
        self.angle =0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()

    def update(self, player):
        self.rect.center = player.rect.center

        position = pygame.mouse.get_pos()

        x_distance = +(position[0] - self.rect.centerx)
        y_distance = -(position[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_distance, x_distance))
        
    def draw(self, area):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        area.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))
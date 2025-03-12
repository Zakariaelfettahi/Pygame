import pygame
import constants

class Character():
    def __init__(self,x,y, image):
        self.image = image
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x, y)
    def move(self,dx,dy):
        if dx !=0 and dy !=0:
            dx = dx/1.414
            dy = dy/1.414
        self.rect.x += dx
        self.rect.y += dy
    def draw(self,area):
        area.blit(self.image, self.rect)
        pygame.draw.rect(area, constants.RED , self.rect, 1)

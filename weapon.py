import pygame
import math
import random
import constants

class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle =0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

        self.arrow_image = arrow_image

    def update(self, player):
        #shoting cooldown
        cooldown = 300

        #create arrow
        arrow = None
        self.rect.center = player.rect.center

        #rotating the bow around the player
        position = pygame.mouse.get_pos()
        x_distance = +(position[0] - self.rect.centerx)
        y_distance = -(position[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_distance, x_distance))

        #getting mouse clicks
        if pygame.mouse.get_pressed()[0] and self.fired == False and pygame.time.get_ticks() - self.last_shot >= cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

            #reset mouseclick
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

        return arrow
        
    #draw function
    def draw(self, area):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        area.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #claculate velocity based on angle
        self.dx = +(math.cos(math.radians(self.angle)) * constants.ARROW_SPEED)
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)
        
    #update function
    def update(self, enemy_list):
        # reset varibales
        damage = 0
        damage_position = (0,0)

        #move arrow
        self.rect.x += self.dx
        self.rect.y += self.dy

        #delete arrow if it leaves the screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        #check for collision with enemy
        for enemy in enemy_list:
            if pygame.sprite.collide_rect(self, enemy) and enemy.alive:
                damage = 15 + random.randint(-5,5)
                damage_position = (enemy.rect.centerx, enemy.rect.y)
                enemy.health -= damage
                self.kill()
                break
        return damage, damage_position


    #draw function
    def draw(self, area):
        area.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))


    
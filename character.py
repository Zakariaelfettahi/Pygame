import pygame
import math
import weapon
import constants

class Character():
    def __init__(self,x,y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0
        self.running = True
        self.health = health
        self.alive = True
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,constants.TILE_SIZE*0.90 * size, constants.TILE_SIZE*size*0.90)
        self.rect.center = (x, y)
        self.coins = 0
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned =  False
    
    def move(self,dx,dy, obstacle_tiles, exit_tile = None):
        #level completion
        level_complete = False

        if self.char_type == 0:
            if exit_tile[1].colliderect(self.rect):
                #ensure player is the right distance
                exit_dist = math.sqrt((self.rect.centerx - exit_tile[1].centerx)**2) + ((self.rect.centery - exit_tile[1].centery)**2)
                if exit_dist < 20: 
                    level_complete = True

        


        #screen scroll
        screen_scroll = [0,0]

        #flip image if going left
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        #normalize the diagonal movement
        if dx !=0 and dy !=0:
            dx = dx/1.414
            dy = dy/1.414
        
        #check for collision
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                #check which side
                if dx > 0:
                    self.rect.right= obstacle[1].left
                if dx < 0:
                    self.rect.left= obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                #check which side
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top= obstacle[1].bottom

        # running animation
        self.running = True
        if dx == 0 and dy == 0:
            self.running = False

        #update player scroll based on player position
        if self.char_type == 0:

            #scroll right
            if self.rect.right > constants.SCREEN_WIDTH - constants.SCROLL_THRESH:
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH

            #scroll left
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH
            
            #scroll down
            if self.rect.bottom > constants.SCREEN_HEIGHT - constants.SCROLL_THRESH:
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH

            #scroll up
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH

        return screen_scroll, level_complete
            
    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image):
        fireball = None
        clipped_line = ()
        stun_cooldown = 200
        ai_dx = 0
        ai_dy = 0
        #reposition mob
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #create a line of sight
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        #check if line of sight intersects an obstacle
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        #check distance
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2))

        if not clipped_line and dist >= constants.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = +constants.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = +constants.ENEMY_SPEED
        
        if self.alive:
            if not self.stunned:
                #chase player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                #attack player
                if dist < constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                    #boss eenemy fireball
                    boss_cooldown = 750
                    if self.boss:
                        if dist < 500:
                            if pygame.time.get_ticks() - self.last_attack >= boss_cooldown:
                                fireball = weapon.Fireball(fireball_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                                self.last_attack = pygame.time.get_ticks()
            
            #reset hit
            if self.hit == True:
                self.hit = False
                self.last_hit= pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0)
            
            #if cooldown passed
            if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False
            
        return fireball

    def update(self):
        #check if character is alive
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        #timer to reset player vunerability
        hit_cooldown = 1000
        if self.char_type == 0:
            if self.hit == True:
                if (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                    self.hit = False


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


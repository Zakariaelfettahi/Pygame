import pygame

class Items(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin

    def update(self, screen_scroll, player, coin_fx, heal_fx):
        #dummy coin
        if not self.dummy_coin:
            #update rect
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        #check collision with player
        if pygame.sprite.collide_rect(self, player):
            #check item type
            if self.item_type == 0:
                player.coins += 1
                coin_fx.play()
            elif self.item_type == 1:
                player.health += 20
                heal_fx.play()
                if player.health >= 100:
                    player.health = 100
            self.kill()

        animation_cooldown = 150
        #update image
        self.image = self.animation_list[self.frame_index]
        #check time passed
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #reset animation
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        
    def draw(self, area):
        area.blit(self.image, self.rect)

   
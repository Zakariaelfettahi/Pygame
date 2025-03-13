import pygame
import constants
from character import Character
from weapon import Weapon
from items import Items

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

#create a clock
clock = pygame.time.Clock()

#define movement variables
move_left = False
move_right = False
move_up = False
move_down = False

#scale image helper function
def scale_image(image, scaler):
    return pygame.transform.scale(image, (image.get_width()*scaler, image.get_height()*scaler))

#coin images
coin_images = []
for i in range(4):
    coin_image = scale_image(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(), constants.ITEM_SCALER)
    coin_images.append(coin_image)

#potion image
potion_image = scale_image(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALER)


#heart images
empty_heart_image = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALER)
half_heart_image = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALER)
full_heart_image = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALER)

#weapon images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALER)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALER)


#MOB images
mob_animations = []
mob_types = ['elf', 'imp', 'goblin', 'skeleton', 'muddy', "tiny_zombie", "big_demon"]

#player image
animation_types = ['idle', 'run']

for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            player_image = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            player_image = scale_image(player_image, constants.SCALER)
            temp_list.append(player_image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#Write on screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))
#draw info function
def draw_info():
    #draw pannel
    pygame.draw.rect(screen, constants.TOP_PANNEL, (0,0,constants.SCREEN_WIDTH, 40))
    pygame.draw.line(screen, constants.WHITE, (0,40), (constants.SCREEN_WIDTH, 40), 1)
    #draw health
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i+1)*20):
            screen.blit(full_heart_image, (10+i*50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(half_heart_image, (10+i*50, 0))
            half_heart_drawn = True
        else:
            screen.blit(empty_heart_image, (10+i*50, 0))

    #draw coins
    draw_text(f"Shmoney: {player.coins}", font, constants.WHITE, 600, 10)

#Damage text class
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


# create a player
player = Character(100, 100, 100, mob_animations,0)

#create an enemy
enemy = Character(200, 200, 100, mob_animations, 1)

#create player's weapon
bow = Weapon(bow_image, arrow_image)

#create sprite group
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

#create top pannel coin
score_coin = Items(590, 19, 0, coin_images)
item_group.add(score_coin)

#create coin
coin = Items(300, 300, 0, coin_images)
item_group.add(coin)

#create potion
potion = Items(100, 200, 1, [potion_image])
item_group.add(potion)


#create enemy list
enemy_list = []
enemy_list.append(enemy)


#main game loop
running = True
while running:

    #control speed of the game
    clock.tick(constants.FPS)

    screen.fill(constants.BG)

    #calculate movement
    dx=0
    dy=0

    if move_down:
        dy = +constants.SPEED
    if move_up:
        dy = -constants.SPEED
    if move_left:
        dx = -constants.SPEED
    if move_right:
        dx = +constants.SPEED

    #move player
    player.move(dx,dy)

    #update player 
    player.update()

    #update enemy
    for enemy in enemy_list:
        enemy.update()

    #update weapon
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    
    # Update arrow
    for arrow in arrow_group:
        damage, damage_position = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_position[0], damage_position[1], str(damage), pygame.Color("red"))
            damage_text_group.add(damage_text)

    # Update and draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)  

    #draw and update itmes 
    item_group.draw(screen)
    item_group.update(player)

    #draw info
    draw_info()

    #draw score_coin 
    score_coin.draw(screen)

    #draw player
    player.draw(screen)

    #draw enemy
    for enemy in enemy_list:
        enemy.draw(screen)

    #draw weapon
    bow.draw(screen)

    #draw arrow
    for arrow in arrow_group:
        arrow.draw(screen)


    #event handler (pressing keys, quiting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True
        # check if button is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s:
                move_down = False
    pygame.display.update()
pygame.quit()

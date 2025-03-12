import pygame
import constants
from character import Character
from weapon import Weapon

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


# create a player
player = Character(100, 100, 100, mob_animations,0)

#create an enemy
enemy = Character(200, 200, 100, mob_animations, 1)

#create player's weapon
bow = Weapon(bow_image, arrow_image)

#create sprite group
arrow_group = pygame.sprite.Group()

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
    
    #update arrow
    for arrow in arrow_group:
        arrow.update(enemy_list)

    
    #verifying if arrow gets deleted when it leaves the screen
    print(arrow_group)


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

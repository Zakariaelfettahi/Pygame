import pygame
import constants

class World():
    def __init__(self):
        self.map_tiles = []
    
    def process_data(self, data, tile_list):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x*constants.TILE_SIZE
                image_y = y*constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = (image, image_rect, image_x, image_y)

                #add image
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update (self, screen_scroll):
        for tile in self.map_tiles:
            tile[1][0] += screen_scroll[0]
            tile[1][1] += screen_scroll[1]
            
            

    def draw(self, area):
        for tile in self.map_tiles:
            area.blit(tile[0], tile[1])




    
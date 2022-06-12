import pygame
from Settings import *
from Noise import PerlinNoise
from Item import Item
from Object import Object

class Ground:
    def __init__(self,map,Tile_map):
        self.map = map
        self.Tile_map = Tile_map
        self.image = pygame.Surface((tile_size,tile_size))
        
    def ground_logic(self,mouse_pos,ground,perlin):
        mouse_offset = mouse_pos//tile_size
        if ground[mouse_offset[1]][mouse_offset[0]]['ground'] == 'plowed_ground':
            self.restore_ground(mouse_offset,ground,perlin)
        else:
            biome = perlin[mouse_offset[1]][mouse_offset[0]]
            if biome != 'water':
                self.image.fill('black')
                self.draw(mouse_offset)
                ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'plowed_ground'

    def seeding_logic(self,mouse_pos,ground,seed,ui):
        mouse_offset = mouse_pos//tile_size
        if ground[mouse_offset[1]][mouse_offset[0]]['ground'] == 'plowed_ground':
            if ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] == False:
                ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] = True
                ground[mouse_offset[1]][mouse_offset[0]]['seed'] = seed
                ground[mouse_offset[1]][mouse_offset[0]]['growth_time'] = growth_times[seed]
                self.image.fill('yellow')
                self.draw(mouse_offset)
            elif ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] and ground[mouse_offset[1]][mouse_offset[0]]['growth_time'] == 0:
                ui.add_item(Item(Object((0,0),None,ground[mouse_offset[1]][mouse_offset[0]]['seed']),(0,0),None),1)
                ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] = False
                ground[mouse_offset[1]][mouse_offset[0]]['seed'] = None
                ground[mouse_offset[1]][mouse_offset[0]]['growth_time'] = None
                self.image.fill('black')
                self.draw(mouse_offset)
            else:
                ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] = False
                ground[mouse_offset[1]][mouse_offset[0]]['seed'] = None
                ground[mouse_offset[1]][mouse_offset[0]]['growth_time'] = None
                self.image.fill('black')
                self.draw(mouse_offset)
                
    def check_growth(self,ground,y,x):
        if ground[y][x]['seeded_ground']:
            if ground[y][x]['growth_time'] != None:
                if ground[y][x]['growth_time'] >= 1:
                    ground[y][x]['growth_time'] -= 1
                else:
                    ground[y][x]['growth_time'] = 0 # 0 cuz we check if its 0 and then if it is we know the tree grew up and return this to None
                    self.image.fill('red')
                    self.draw(pygame.math.Vector2(x,y))
            
    def restore_ground(self,mouse_offset,ground,perlin):
        if perlin[mouse_offset[1]][mouse_offset[0]] == 'beach':
            self.map.blit(self.Tile_map[22*1+1],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'beach'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'forest':
            self.map.blit(self.Tile_map[22*11+3],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'forest'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'rainforest':
            self.map.blit(self.Tile_map[22*12+2],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'rainforest'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'savanna':
            self.map.blit(self.Tile_map[22*5+3],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'savanna'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'desert':
            self.map.blit(self.Tile_map[22*5],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'desert'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'plains':
            self.map.blit(self.Tile_map[22*12+3],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'plains'
            
    def draw(self,mouse_offset):
        self.map.blit(self.image,mouse_offset*tile_size)
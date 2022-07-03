import re
from numpy import tile
import pygame
from Settings import *
class Object(pygame.sprite.Sprite):
    def __init__(self,pos,groups,name,key):
        if groups != None:
            super().__init__(groups)
        self.type = 'block'
        self.name = name
        self.key = key
        self.image = pygame.image.load(f'../graphics/objects/{self.name}.png')
        self.seed_image = pygame.image.load(f'../graphics/seeds/seed.png')
        self.pos = pygame.math.Vector2(pos) - object_offset[self.name]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.inv_image = self.image.subsurface(pygame.Rect((0,0),(tile_size,tile_size)))
        
    def subtract_recursion(self,pos):
        real_pos = pygame.math.Vector2(pos[0],pos[1])
        if pos[1] - tile_size > 0:
            real_pos[1] = pos[1] - tile_size
            if pos[1] - tile_size > 0:
                self.subtract_recursion(real_pos)
        return real_pos
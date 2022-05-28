import pygame
from Settings import *
class Object(pygame.sprite.Sprite):
    def __init__(self,pos,groups,key):
        if groups != None:
            super().__init__(groups)
        self.name = key
        self.type = 'block'
        self.image = pygame.image.load(f'../graphics/objects/{self.name}.png')
        self.inv_image = self.image.subsurface(pygame.Rect((0,0),(tile_size,tile_size)))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-10)
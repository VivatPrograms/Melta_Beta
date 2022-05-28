import pygame
from Settings import *
class Item(pygame.sprite.Sprite):
    def __init__(self,sprite,pos,groups):
        if groups != None:
            super().__init__(groups)
        self.type = 'item_drop'
        self.name = sprite.name
        self.pos = pos
        self.inv_image = sprite.inv_image
        self.image = self.inv_image
        self.rect = self.image.get_rect(topleft=self.pos)
        if sprite.type == 'item_drop':
            self.type_before = sprite.type_before
        else:
            self.type_before = sprite.type
        pygame.draw.rect(self.image, 'white', pygame.Rect((0, 0), (tile_size, tile_size)), 2)
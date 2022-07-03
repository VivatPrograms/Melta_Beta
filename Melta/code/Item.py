import pygame
from Settings import *
class Item(pygame.sprite.Sprite):
    def __init__(self,sprite,pos,groups,seed):
        if groups != None:
            super().__init__(groups)
        self.name = sprite.name
        self.key = sprite.key
        self.pos = pos
        self.seed = seed
        self.image = pygame.image.load(f'../graphics/objects/{self.name}.png')
        self.seed_image = pygame.image.load(f'../graphics/seeds/seed.png')
        self.determine_type(seed,sprite)
        self.determine_type_before(sprite)
        pygame.draw.rect(self.image, 'white', pygame.Rect((0, 0), (tile_size, tile_size)), 2)
        
    def determine_type(self,seed,sprite):
        if seed:
            self.type = 'seed'
            self.inv_image = sprite.seed_image
        else:
            self.type = 'item_drop'
            self.inv_image = sprite.inv_image
        self.image = self.inv_image
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def determine_type_before(self,sprite):
        if sprite.type == 'item_drop':
            self.type_before = sprite.type_before
        elif sprite.type == 'seed':
            self.type_before = sprite.type_before
        else:
            self.type_before = sprite.type
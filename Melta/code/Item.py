import copy
from Settings import *
class Item(pygame.sprite.Sprite):
    def __init__(self,sprite,pos,groups,seed,amount):
        if groups != None:
            super().__init__(groups)
        else:
            super().__init__()
        font = pygame.font.Font(None, 32)
        text = font.render(str(amount), True, 'white')
        self.name = sprite.name
        self.amount = amount
        self.pos = pos
        self.seed = seed
        self.image = pygame.image.load(f'../graphics/objects/{self.name}.png')
        self.seed_image = pygame.image.load(f'../graphics/seeds/seed.png')
        self.determine_type(seed,sprite)
        self.determine_type_before(sprite)
        self.image.blit(text, (font_offset,font_offset))
        pygame.draw.rect(self.image, 'aqua', pygame.Rect((0, 0), (tile_size, tile_size)), 2)
        
    def determine_type(self,seed,sprite):
        if seed: 
            self.type = 'seed'
            self.inv_image = sprite.seed_image
        else:
            self.type = 'item_drop'
            self.inv_image = sprite.inv_image
        self.image = copy.copy(self.inv_image)
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def determine_type_before(self,sprite):
        if sprite.type == 'item_drop':
            self.type_before = sprite.type_before
        elif sprite.type == 'seed':
            self.type_before = sprite.type_before
        else:
            self.type_before = sprite.type
import copy
from Settings import *
class Item(pygame.sprite.Sprite):
    def __init__(self,sprite,pos,groups,seed,amount):
        if groups != None:
            super().__init__(groups)
        else:
            super().__init__()
        self.seed = seed
        self.name = sprite.name
        self.amount = amount
        self.pos = pos
        self.folder = self.get_folder_and_image()
        self.determine_type(seed,sprite)
        self.determine_type_before(sprite)
        slot = pygame.image.load('../graphics/items/unplaceables/other/slot.png')
        self.image.blit(pygame.transform.scale(slot,(slot.get_width()*reshape_game.x,slot.get_height()*reshape_game.y)),(0, 0))

    def get_folder_and_image(self):
        try:
            folder = 'unplaceables'
            if not self.seed:
                self.image = pygame.transform.scale(pygame.image.load(f'{paths[self.name]}/{self.name}.png'),
                (tile_size*reshape_game.x,tile_size*reshape_game.y))
            else:
                self.image = pygame.transform.scale(pygame.image.load('../graphics/items/placeables/seeds/seed.png'),
                (tile_size*reshape_game.x,tile_size*reshape_game.y))
        except KeyError:
            folder = 'placeables'
            self.image = pygame.image.load(f'../graphics/items/placeables/objects/{self.name}.png')
        return folder
        
    def determine_type(self,seed,sprite):
        if seed: 
            self.type = 'seed'
            self.inv_image = self.image
        else:
            self.type = 'item_drop'
            self.inv_image = sprite.inv_image
            self.image_before = sprite.image
        self.image = copy.copy(self.inv_image)
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def determine_type_before(self,sprite):
        if sprite.type == 'item_drop':
            self.type_before = sprite.type_before
        elif sprite.type == 'seed':
            self.type_before = sprite.type_before
        else:
            self.type_before = sprite.type
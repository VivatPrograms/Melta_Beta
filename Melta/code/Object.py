from Settings import *
import copy
class Object(pygame.sprite.Sprite):
    def __init__(self,pos,groups,name):
        if groups != None:
            super().__init__(groups)
        self.type = 'block'
        self.name = name
        self.being_damaged = False
        self.damage_received = 0
        self.damage_bar = pygame.Surface((86*reshape_game.x,22*reshape_game.y))
        self.folder = self.get_folder_and_image()
        self.seed_image = pygame.image.load(f'../graphics/items/placeables/seeds/seed.png')
        self.pos = pos if self.image.get_rect().width == round(tile_size*reshape_game.x) else self.object_offset(pos)  
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(0,-20*reshape_game.y)
        self.create_inv_image()
        self.open_chest = False
        self.chest_inventory = copy.deepcopy(chest_inventory)
    def create_inv_image(self):
        for name in ['sword','lance']:
            if not name in self.name:
                self.inv_image = pygame.transform.scale(self.image,(tile_size*reshape_game.x,tile_size*reshape_game.y))
            else:
                img = pygame.image.load(f'{paths[self.name]}/{self.name}.png')
                self.inv_image = pygame.transform.scale(img,(img.get_width()*reshape_game.x,img.get_height()*reshape_game.y))

    def object_offset(self,pos): 
        offset = (self.image.get_width()//4,self.image.get_height() - tile_size*reshape_game.y)
        return pygame.math.Vector2(pos) - offset

    def get_folder_and_image(self):
        try:
            folder = 'unplaceables'
            self.image = pygame.transform.scale(pygame.image.load(f'{paths[self.name]}/{self.name}.png'),
            (tile_size*reshape_game.x,tile_size*reshape_game.y))
        except KeyError:
            folder = 'placeables'
            img = pygame.image.load(f'../graphics/items/placeables/objects/{self.name}.png')
            self.image = pygame.transform.scale(img,(img.get_width()*reshape_game.x,img.get_height()*reshape_game.y))
        return folder
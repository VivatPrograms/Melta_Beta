from Settings import *
class Object(pygame.sprite.Sprite):
    def __init__(self,pos,groups,name):
        if groups != None:
            super().__init__(groups)
        self.type = 'block'
        self.name = name
        self.being_damaged = False
        self.damage_received = 0
        self.damage_bar = pygame.Surface((86,22))
        self.folder = self.get_folder_and_image()
        self.seed_image = pygame.image.load(f'../graphics/items/placeables/seeds/seed.png')
        self.pos = pos if self.image.get_rect().width == tile_size else self.object_offset(pos)  
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.inv_image = pygame.transform.scale(self.image,(tile_size,tile_size))

    def object_offset(self,pos): 
        offset = (self.image.get_width()//4,self.image.get_height() - tile_size)
        return pygame.math.Vector2(pos) - offset

    def get_folder_and_image(self):
        try:
            folder = 'unplaceables'
            self.image = pygame.transform.scale(pygame.image.load(f'{paths[self.name]}/{self.name}.png'),
            (tile_size,tile_size))
        except KeyError:
            folder = 'placeables'
            self.image = pygame.image.load(f'../graphics/items/placeables/objects/{self.name}.png')
        return folder
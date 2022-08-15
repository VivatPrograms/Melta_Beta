from Settings import *
class Object(pygame.sprite.Sprite):
    def __init__(self,pos,groups,name):
        if groups != None:
            super().__init__(groups)
        self.type = 'block'
        self.name = name
        self.image = pygame.image.load(f'../graphics/objects/{self.name}.png')
        self.seed_image = pygame.image.load(f'../graphics/seeds/seed.png')
        self.pos = pos if self.image.get_rect().width == tile_size else self.object_offset(pos)  
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.inv_image = self.image.subsurface(pygame.Rect((0,0),(tile_size,tile_size)))

    def object_offset(self,pos): 
        offset = (self.image.get_width()//4,self.image.get_height() - tile_size)
        return pygame.math.Vector2(pos) - offset
        
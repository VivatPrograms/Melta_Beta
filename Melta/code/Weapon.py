from Settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.name = 'weapon'
        self.type = self.name
        direction = player.status.split('_')[0]
        #graphic
        fullpath = f'../graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(fullpath).convert_alpha()
        #placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(0,16))
        if direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(0,16))
        if direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop+pygame.math.Vector2(-10,0))
        if direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(-10,0))
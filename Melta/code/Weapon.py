from Settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.name = 'weapon'
        self.type = self.name
        direction = player.status.split('_')[0]
        #graphic
        fullpath = f'../graphics/weapons/{player.weapon}/SpriteInHand.png'
        self.image = pygame.image.load(fullpath).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*3,self.image.get_height()*3))
        #placement
        if direction == 'Right':
            self.image = pygame.transform.rotate(self.image,90)
            self.rect = self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(0,16))
        if direction == 'Left':
            self.image = pygame.transform.rotate(self.image,270)
            self.rect = self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(0,16))
        if direction == 'Up':
            self.image = pygame.transform.rotate(self.image,180)
            self.rect = self.image.get_rect(midbottom=player.rect.midtop+pygame.math.Vector2(-10,0))
        if direction == 'Down':
            self.image = pygame.transform.rotate(self.image,0)
            self.rect = self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(-10,0))
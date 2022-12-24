import pygame, copy
from Settings import *

class ObjectDisplay:
    def __init__(self,pos,slot):
        self.block = False
        if self.block_check(slot):
            self.name = slot.name
            img = pygame.image.load(f'../graphics/items/placeables/objects/{self.name}.png')
            self.image = pygame.transform.scale(img,(img.get_width()*reshape_game.x,img.get_height()*reshape_game.y))
            self.pos = pos if self.image.get_width() == round(tile_size*reshape_game.x) else self.object_offset(pos)  
            self.rect = self.image.get_rect(topleft=self.pos)
            self.block = True
    def block_check(self,slot):
        if slot != None and slot.type != 'seed':
            if slot.type_before == 'block' and slot.folder == 'placeables':
                return True
        return False
    def object_offset(self,pos):
        offset = (self.image.get_width()//4,self.image.get_height() - tile_size*reshape_game.y)
        return pygame.math.Vector2(pos) - offset
    def convert_object(self,color):
        mask = pygame.mask.from_surface(self.image)
        self.image = mask.to_surface(setcolor=color, unsetcolor=None)
    def draw_display(self):
        pygame.display.get_surface().blit(self.image,self.rect)
    def draw(self,color):
        self.convert_object(color)
        self.draw_display()
from Settings import *
class Button(pygame.sprite.Sprite):
    def __init__(self,name,pos,button_to,img_name,button_from,font,key_explanation):
        self.name = name
        self.pos = pos
        self.button_to = button_to
        self.button_from = button_from
        self.font = font
        self.explanation = key_explanation
        self.draw_image(img_name)
    def draw_image(self,img):
        self.image = pygame.image.load(f'../graphics/items/unplaceables/other/{img}.png')
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*reshape_game.y,self.image.get_height()*reshape_game.y))
        self.rect = self.image.get_rect(center=self.pos) 
        txt = self.font.render(self.name.upper(),False,'#3a3a50')
        self.image.blit(txt,txt.get_rect(center=(self.rect.width/2,self.rect.height/2)))
    def key_explanation(self):
        txt = self.font.render(self.explanation,False,'#fbeee4')
        pygame.display.get_surface().blit(txt,(self.pos[0]+(round(tile_size*reshape_game.x)),self.pos[1]-(round(tile_size*reshape_game.y))//5))
    def draw(self,i):
        pygame.display.get_surface().blit(self.image,(self.rect.x,self.rect.y+self.offset))
        if self.button_from[i] == 'control_options':
            self.key_explanation()
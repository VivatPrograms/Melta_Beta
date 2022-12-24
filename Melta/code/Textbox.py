from Settings import *
class TextBox:
    def __init__(self,pos,textbox_from,font):
        self.pos = pos
        self.textbox_from = textbox_from
        self.font = font
        self.text = ''
        self.selected = False
        self.image1 = pygame.image.load('../graphics/items/unplaceables/other/text_box.png')
        self.draw_img()
    
    def draw_img(self):
        self.image = pygame.transform.scale(self.image1,(self.image1.get_width()*reshape_game.x,self.image1.get_height()*reshape_game.y))
        self.rect = self.image.get_rect(center=self.pos)
        txt = self.font.render(self.text,False,'white')
        self.image.blit(txt,txt.get_rect(center=(self.rect.width/2,self.rect.height/2)))

    def draw(self):
        pygame.display.get_surface().blit(self.image,self.rect)
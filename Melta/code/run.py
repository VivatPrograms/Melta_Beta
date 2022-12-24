import sys,time
from Settings import *
from Main import *
from debug import debug

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.code = Main()
        
    def run(self):
        while True:
            click = False
            key_press = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()          
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = event.button
                if event.type == pygame.KEYDOWN:
                    key_press = event.key
                if event.type == pygame.MOUSEWHEEL:
                    self.code.zoom_scale += event.y
            self.screen.fill('black')
            self.code.run(click,key_press)
            self.clock.tick(FPS)
            pygame.display.update()
if __name__ == '__main__':
    pygame.display.set_caption('Melta')
    game = Game()
    game.run() 
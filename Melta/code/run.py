import sys,time
from Settings import *
from Main import *
from debug import debug

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.code = Main()
        
    def run(self):
        while True:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()          
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = event.button
            self.screen.fill('black')
            self.code.run(click)
            self.clock.tick(60)
            pygame.display.update()

if __name__ == '__main__':
    pygame.display.set_caption('Melta')
    game = Game()
    game.run() 
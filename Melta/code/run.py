import pygame,sys,time
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.code.run()
            self.clock.tick(FPS)
            self.fps_counter = self.clock.get_fps()
            debug(self.fps_counter)
            pygame.display.update()

if __name__ == '__main__':
    pygame.display.set_caption('Melta')
    game = Game()
    game.run()
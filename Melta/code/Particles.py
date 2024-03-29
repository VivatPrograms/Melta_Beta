from Import_support import import_sprite_sheet
from random import choice
from Settings import *
class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'Slash' : [],
        }
        for attack in self.frames.keys():
            full_path =  f'../graphics/animations/attacks/{attack}/SpriteSheet.png'
            images = import_sprite_sheet(full_path,(32,32))
            for i in range(len(images)):
                self.frames[attack].append(images[i])

    def reflect_images(self,frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_particles(self,animation_type,pos,groups,spriterect):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups,spriterect)
    
    def create_destruction_particles(self,pos,groups,size,spriterect):
        full_path = '../graphics/animations/smokes/Smoke/SpriteSheet.png'
        animation_frames = import_sprite_sheet(full_path,size)
        ParticleEffect(pos,animation_frames,groups,spriterect)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups,spriterect):
        super().__init__(groups)
        self.type = 'particle'
        self.name = self.type
        self.pos = pos
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.spriterect = spriterect

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = pygame.transform.scale(self.frames[int(self.frame_index)],(self.spriterect.width,self.spriterect.height))

    def update(self):
        self.animate()
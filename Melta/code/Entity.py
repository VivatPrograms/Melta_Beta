from time import perf_counter
import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups,pos):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 8
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(pos)

    def move(self, speed, dt, walking=True, attacking=False):
        if walking and not attacking:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.position.x += self.direction.x * speed * dt
            self.hitbox.x = self.position.x
            self.collision('horizontal')
            self.position.y += self.direction.y * speed * dt
            self.hitbox.y = self.position.y
            self.collision('vertical')

    def knockback(self,distance,dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.position.x += self.direction.x * distance * dt
        self.hitbox.x = round(self.position.x)
        self.collision('horizontal')
        self.position.y += self.direction.y * distance * dt
        self.hitbox.y = round(self.position.y)
        self.collision('vertical')
        self.rect.topleft = self.hitbox.topleft

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    else:
                        self.hitbox.right = sprite.hitbox.left
                    self.position.x = self.hitbox.x
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    else:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.position.y = self.hitbox.y
                    
    def wave_value(self,dt):
        value = sin(perf_counter()*dt)
        if value >= 0:
            return 255
        else:
            return 0
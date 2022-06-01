from random import randint

import pygame

from Settings import *
from Object import Object
from Item import Item
from Player import Player
from Noise import PerlinNoise
from Import_support import *
from UI import UI
from Weapon import Weapon
from Enemy import Enemy
from Particles import AnimationPlayer

class Main:
    def __init__(self):
        #class imports
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.player = Player((grid_width // 2 * tile_size, grid_width // 2 * tile_size), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
        self.animation_player = AnimationPlayer()
        self.perlin = PerlinNoise()
        self.ui = UI()
        # self.magic_player = MagicPlayer(self.animation_player)
        self.Tile_map = import_sprite_sheet('../graphics/tilemap/Floor.png')
        #click cooldown
        self.click_cooldown = 400
        self.clicking_cooldown = None
        self.click_time = None
        self.clicking = False
        self.offset = pygame.math.Vector2()
        self.object_collide = False
        self.input = False
        #breaking
        self.time_to_hold = 100
        self.hold_timer = 0
        self.breaking = False
        self.breaking_surf = pygame.Surface((86,22))
        #map
        self.generate_map()

    def generate_map(self):
        self.perlin.generate_noise()
        self.grid = self.perlin.container
        self.map = pygame.Surface((tile_size * grid_width, tile_size * grid_width))
        for key in self.grid.keys():
            for coord in self.grid[key]:
                #general setup
                rect = self.Tile_map[0].get_rect(topleft=(coord))
                #obstacles/enemies
                if key == 'rock':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],'rock')
                elif key == 'tree':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],'tree')
                elif key == 'enemy':
                    Enemy('squid', coord, [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                          self.damage_player, self.trigger_death_particles, self.add_exp)
                #biomes
                if key == 'water':
                    self.map.blit(self.Tile_map[22*12+8], rect)
                elif key == 'beach':
                    self.map.blit(self.Tile_map[22*1+1], rect)
                elif key == 'forest':
                    self.map.blit(self.Tile_map[22*11+3], rect)
                elif key == 'rainforest':
                    self.map.blit(self.Tile_map[22*12+2], rect)
                elif key == 'savanna':
                    self.map.blit(self.Tile_map[22*5+3], rect)
                elif key == 'desert':
                    self.map.blit(self.Tile_map[22*5], rect)
                elif key == 'plains':
                    self.map.blit(self.Tile_map[22*12+3], rect)

    def map_update(self):
        self.map_rect = self.map.get_rect()
        self.map_pos = self.map_rect.topleft - self.offset
        self.offset.x = self.player.rect.centerx - WIDTH // 2
        self.offset.y = self.player.rect.centery - HEIGHT // 2

    # ---------------------------Map Interactables/Sprites-------------------------------

    def manage_input(self):
        key = pygame.key.get_pressed()
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset = mouse_pos + self.offset
        self.object_collide = False
        self.breaking = False
        for sprite in self.interactables.sprites():
            if sprite.rect.collidepoint(mouse_offset):
                self.object_collide = True
                if pygame.mouse.get_pressed()[0]:
                    if sprite.type == 'block':
                        self.breaking = True
                        self.hold_timer += 1
                        self.break_block(sprite,self.hold_timer)
                        self.display_breaking(sprite,self.hold_timer,self.time_to_hold,mouse_offset)
                    elif sprite.type == 'item_drop':
                        self.collect_item(sprite)
                else:
                    self.hold_timer = 0

        if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
            if key[pygame.K_p]:
                if not self.clicking:
                    self.clicking = True
                    self.click_time = pygame.time.get_ticks()
                    if not self.object_collide:
                        self.place_block(mouse_offset)
            elif key[pygame.K_q]:
                if not self.clicking:
                    self.clicking = True
                    self.click_time = pygame.time.get_ticks()
                    self.drop_item()
    def display_breaking(self,sprite,hold_time,max_time,mouse_offset):
        bg_rect = self.breaking_surf.get_rect(topleft=(0,0))
        pygame.draw.rect(self.breaking_surf,'black',bg_rect)
        ratio = hold_time / max_time
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.breaking_surf,'red',current_rect)
    def break_block(self,sprite,hold_timer):
        if hold_timer >= self.time_to_hold:
            sprite.kill()
            Item(sprite, sprite.rect.center, [self.visible_sprites,self.interactables])
            self.hold_timer = 0
            self.breaking_pos = None
    def place_block(self,mouse_pos):
        if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type_before == 'block':
            mouse_offset = (mouse_pos//tile_size)*tile_size
            Object(mouse_offset, [self.visible_sprites,self.obstacle_sprites,self.interactables], self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name)
            self.remove_item(self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def drop_item(self):
        Item(self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'], self.player.rect.topleft + self.player.facing_offset,[self.visible_sprites, self.interactables])
        self.remove_item(self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def collect_item(self,sprite):
        sprite.kill()
        self.ui.add_item(sprite,1,self.ui.inventory)
    def remove_item(self,sprite):
        self.ui.remove_item(sprite,1,self.ui.inventory)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.clicking:
            if current_time - self.click_time >= self.click_cooldown:
                self.clicking = False

    def update_sprites(self):
        self.manage_input()
        self.cooldowns()

    #---------------------------Player attack Logic-------------------------------

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

    def player_attack_update(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.name == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.name)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def run(self,click):
        self.map_update()
        self.update_sprites()
        self.player_attack_update()
        self.display_surface.blit(self.map,self.map_pos)
        self.visible_sprites.draw(self.offset)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.update()
        self.ui.update(click)
        if self.breaking:
           self.display_surface.blit(self.breaking_surf,(0,0))

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self,offset):
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            pygame.display.get_surface().blit(sprite.image, sprite.rect.topleft - offset)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'name') and sprite.name == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

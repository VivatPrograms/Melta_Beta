from random import randint, choice
import copy
from re import T
from numpy import tile
import pygame
from math import dist
from Settings import *
from Object import Object
from Item import Item
from Player import Player
from Noise import PerlinNoise
from Import_support import *
from Ground import Ground
from UI import UI
from Weapon import Weapon
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
        self.Tile_map = import_sprite_sheet('../graphics/Tilemap.png')
        #click cooldown
        self.click_cooldown = 400
        self.clicking_cooldown = None
        self.click_time = None
        self.clicking = False
        self.offset = pygame.math.Vector2()
        self.object_collide = False
        #breaking
        self.time_to_hold = 100
        self.hold_timer = 0
        self.breaking = False
        self.breaking_surf = pygame.Surface((86,22))
        #map
        self.generate_map()
        
    #Map creation/Object creation
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
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names['rock']),'rock')
                elif key == 'tree':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names['tree']),'tree')
                elif key == 'cactus':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names['cactus']),'cactus')
                # elif key == 'enemy':
                #     Enemy('squid', coord, [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                #           self.damage_player, self.trigger_death_particles, self.add_exp)
                #biomes
                if key == 'water':
                    self.map.blit(pygame.image.load('../graphics/tiles/water.png').convert_alpha(), rect)
                elif key == 'forest':
                    self.map.blit(pygame.image.load('../graphics/tiles/forest.png').convert_alpha(), rect)
                elif key == 'rainforest':
                    self.map.blit(pygame.image.load('../graphics/tiles/rainforest.png').convert_alpha(), rect)
                elif key == 'savanna':
                    self.map.blit(pygame.image.load('../graphics/tiles/savanna.png').convert_alpha(), rect)
                elif key == 'desert':
                    self.map.blit(pygame.image.load('../graphics/tiles/desert.png').convert_alpha(), rect)
                elif key == 'plains':
                    self.map.blit(pygame.image.load('../graphics/tiles/plains.png').convert_alpha(), rect)
                #water surrounded
                if key == 'left':
                    self.map.blit(self.Tile_map[16*12+3], rect)
                if key == 'right':
                    self.map.blit(self.Tile_map[16*12+6], rect)
                if key == 'top':
                    self.map.blit(self.Tile_map[16*11+4], rect)
                if key == 'bottom':
                    self.map.blit(self.Tile_map[16*13+4], rect)
                if key == 'topleft':
                    self.map.blit(self.Tile_map[16*4], rect)
                if key == 'bottomleft':
                    self.map.blit(self.Tile_map[16*5], rect)
                if key == 'topright':
                    self.map.blit(self.Tile_map[16*4+1], rect)
                if key == 'bottomright':
                    self.map.blit(self.Tile_map[16*5+1], rect)
                if key == 'surrounded_topleft':
                    self.map.blit(self.Tile_map[16*11+3], rect)
                if key == 'surrounded_bottomleft':
                    self.map.blit(self.Tile_map[16*13+3], rect)
                if key == 'surrounded_topright':
                    self.map.blit(self.Tile_map[16*11+6], rect)
                if key == 'surrounded_bottomright':
                    self.map.blit(self.Tile_map[16*13+6], rect)
        self.ground_class = Ground(self.map,self.Tile_map)
        self.ground = copy.deepcopy(self.perlin.biomes)
        for y in self.perlin.biomes:
            for x in self.perlin.biomes[y]:
                self.ground[y][x] = {'ground':self.perlin.biomes[y][x],'seeded_ground':False,'seed':None,'growth_time':None,'mixed':False}

    def map_update(self):
        self.map_rect = self.map.get_rect()
        self.map_pos = self.map_rect.topleft - self.offset
        self.offset.x = self.player.rect.centerx - WIDTH // 2
        self.offset.y = self.player.rect.centery - HEIGHT // 2
        
    # ---------------------------Map Interactables/Sprites-------------------------------

    def mouse_input(self):
        self.mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mouse_offset = self.mouse_pos + self.offset
        self.object_collide = False
        self.breaking = False
        collisions = 0
        for sprite in self.interactables.sprites():
            if sprite.rect.collidepoint(self.mouse_offset):
                collisions += 1
                self.object_collide = True
                if pygame.mouse.get_pressed()[0]:
                    if sprite.type == 'block':
                        self.hold_timer += 1 // collisions
                        self.breaking = True
                        self.break_block(sprite,self.hold_timer)
                        self.display_breaking(sprite,self.hold_timer,self.time_to_hold)
                    else:
                        self.collect_item(sprite)
                else:
                    self.breaking = False
                    self.hold_timer = 0
        if pygame.mouse.get_pressed()[2] and not self.object_collide:
            if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
                if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'seed':
                    self.seed_ground()
        elif pygame.mouse.get_pressed()[0] and not self.object_collide:
            self.harvest()
    def seed_ground(self):
        self.ground_class.seeding_logic(self.ground,self.ui,self.mouse_offset,
                                        self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].key)
    def harvest(self):
        self.ground_class.harvest(self.ground,self.ui,self.mouse_offset)
                                  
        #make seeding logic more logic.
    def key_input(self):
        key = pygame.key.get_pressed()
        if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
            if not self.object_collide:
                if key[pygame.K_p]:
                    if not self.clicking:
                        self.clicking = True
                        self.click_time = pygame.time.get_ticks()
                        self.place_block(self.mouse_offset)
            if key[pygame.K_q]:
                if not self.clicking:
                    self.clicking = True
                    self.click_time = pygame.time.get_ticks()
                    self.drop_item()
        if key[pygame.K_i]:
            if not self.clicking:
                self.clicking = True
                self.click_time = pygame.time.get_ticks()
                self.ground_class.ground_logic(self.mouse_offset,self.ground,self.perlin.biomes)

        for y in self.ground:
            for x in self.ground[y]:
                if self.ground[y][x]['seeded_ground']:
                    self.ground_class.run(self.ground,y,x)

    #Block logic
    def break_block(self,sprite,hold_timer):
        if hold_timer >= self.time_to_hold:
            sprite.kill()
            self.hold_timer = 0
            self.breaking_pos = None
            if randint(0,3) == 1:
                Item(sprite, sprite.rect.center, [self.visible_sprites,self.interactables],False)
            elif randint(0,3) == 2:
                Item(sprite, sprite.rect.center, [self.visible_sprites,self.interactables],True)
    def place_block(self,mouse_pos):
        mouse_offset = mouse_pos//tile_size
        biome = self.perlin.biomes[mouse_offset[1]][mouse_offset[0]]
        if biome != 'water':
            if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type_before == 'block' and self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'item_drop':
                Object(mouse_offset*tile_size, [self.visible_sprites,self.obstacle_sprites,self.interactables], self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name,self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].key)
                self.remove_item(self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def display_breaking(self,sprite,hold_time,max_time):
        self.under_sprite_pos = sprite.rect.center - self.offset - (42,0)
        bg_rect = self.breaking_surf.get_rect(topleft=(0,0))
        ratio = hold_time / max_time
        current_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * ratio
        self.breaking_surf.fill('black')
        pygame.draw.rect(self.breaking_surf,'red',current_rect)
        pygame.draw.rect(self.breaking_surf,'black',bg_rect,2)
    #Item logic
    def drop_item(self):
        Item(self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'], self.player.rect.topleft + self.player.facing_offset,[self.visible_sprites, self.interactables],
             True if self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'seed' else False)
        self.remove_item(self.ui.inventory[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def collect_item(self,sprite):
        sprite.kill()
        self.ui.add_item(sprite,1)
    def remove_item(self,sprite):
        self.ui.remove_item(sprite,1)
    #More general stuff
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.clicking:
            if current_time - self.click_time >= self.click_cooldown:
                self.clicking = False
    def animations(self):
        if self.breaking:
           self.display_surface.blit(self.breaking_surf,self.under_sprite_pos)
        else:
            self.hold_timer = 0
                    
    def update_sprites(self):
        self.mouse_input()
        self.key_input()
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
        self.animations()

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
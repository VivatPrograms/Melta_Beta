from random import randint, choice
from math import sin
from time import perf_counter
import copy
from Enemy import Enemy
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
        #general
        self.display_surface = pygame.display.get_surface()
        self.map = pygame.Surface((tile_size*grid_width,tile_size*grid_width))
        self.map_rect = self.map.get_rect()
        self.offset_limit = pygame.math.Vector2(self.map_rect.width - WIDTH,self.map_rect.height - HEIGHT)
        self.border = pygame.math.Vector2(self.map_rect.width-tile_size,self.map_rect.height-tile_size)
        print(self.offset_limit)
        #import classes
        self.visible_sprites = YSortCameraGroup(self.map,self.map_rect,self.offset_limit)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.player = Player((grid_width // 2 * tile_size, grid_width // 2 * tile_size),
         [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.border)
        self.animation_player = AnimationPlayer()
        self.perlin = PerlinNoise()
        self.ui = UI(self.player,self.visible_sprites,self.interactables)
        # self.magic_player = MagicPlayer(self.animation_player)
        self.Tile_map = import_sprite_sheet('../graphics/Tilemap.png')
        #click cooldown
        self.attacking = False
        self.attacked = False
        self.click_cooldown = 0.4
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
        #ui
        self.keyboard_input = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
        self.pressed = False
        self.font = pygame.font.Font(None, 32)
        self.last_time = perf_counter()
        
    #Map creation/Object creation
    def generate_map(self):
        self.coords = []
        self.perlin.generate_noise()
        self.grid = self.perlin.container
        for key in self.grid.keys():
            for coord in self.grid[key]:
                self.coords.append(coord)
                #general setup
                rect = self.Tile_map[0].get_rect(topleft=(coord))
                #obstacles/enemies
                if key == 'rock':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names['rock']))
                elif key == 'tree':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names['tree']))
                elif key == 'cactus':
                    self.object = Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names['cactus']))
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
        self.ground = copy.deepcopy(self.perlin.biomes)
        self.ground_class = Ground(self.map,self.Tile_map,self.ground,self.visible_sprites,self.interactables)
        for y in self.perlin.biomes:
            for x in self.perlin.biomes[y]:
                self.ground[y][x] = {'ground':self.perlin.biomes[y][x],'seeded_ground':False,'seed':None,'growth_time':None,'mixed':False}
        self.spawn_enemy(10)

    def spawn_enemy(self,times):
        for _ in range(times):
            random_coord = choice(self.coords)
            Enemy('axolot', random_coord, [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                    self.damage_player, self.trigger_death_particles, self.add_exp, self.border)
        
    # ---------------------------Input-------------------------------

    def input(self,click):
        try:
            self.menu_input()
            if not self.ui.main_menu:
                if not self.ui.crafting_table:
                    self.allow_input(click)
            elif not self.ui.crafting_table:
                if not self.ui.main_menu:
                    self.allow_input(click)
        except KeyError:
            pass

    def allow_input(self,click):
        self.mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mouse_offset = self.mouse_pos + self.offset
        self.breaking = False
        self.mouse_input(click)
        self.farm_input()

    def mouse_input(self,click):
        collisions = 0
        self.object_collide = False
        for sprite in self.interactables.sprites():
            if sprite.rect.collidepoint(self.mouse_offset):
                collisions += 1
                self.object_collide = True
                if click == 3 and 'table' in sprite.name:
                    self.ui.crafting_table = True
                if pygame.mouse.get_pressed()[0]:
                    if sprite.type == 'block':
                        self.hold_timer += 40 // collisions * self.dt
                        self.breaking = True
                        self.break_block(sprite,self.hold_timer)
                        self.display_breaking(sprite,self.hold_timer,self.time_to_hold)
                    else:
                        self.collect_item(sprite)
                else:
                    self.breaking = False
                    self.hold_timer = 0
            
    def farm_input(self):
        if pygame.mouse.get_pressed()[2] and not self.object_collide:
            if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
                if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'seed':
                    self.seed_ground()
        elif pygame.mouse.get_pressed()[0] and not self.object_collide:
            self.harvest()
        elif not pygame.mouse.get_pressed()[0] and not self.object_collide:
            self.tree_info()
            
    def menu_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            if not self.pressed:
                self.pressed = True
                if not self.ui.crafting_table:
                    self.ui.main_menu = not self.ui.main_menu
                    if not self.ui.main_menu:
                        self.ui.return_items(self.ui.crafting_menu) 
                else:
                    self.ui.crafting_table = not self.ui.crafting_table
                    if not self.ui.crafting_table:
                        self.ui.return_items(self.ui.big_crafting_menu)
        else:
            self.pressed = False
        for y in self.ground:
            for x in self.ground[y]:
                if self.ground[y][x]['seeded_ground']:
                    self.ground_class.run(self.ground,y,x,self.current_time)
        if not self.ui.main_menu:
            self.movement_input(key)
            self.keys_input(key)
        else:
            self.player.direction.x = 0
            self.player.direction.y = 0
                    
    def movement_input(self,key):
        if not self.player.attacking:
            #movement input
            if key[pygame.K_w]:
                self.player.status = 'Up_Walk'
                self.player.direction.y = -1
            elif key[pygame.K_s]:
                self.player.status = 'Down_Walk'
                self.player.direction.y = 1
            else:
                self.player.direction.y = 0
            if key[pygame.K_a]:
                self.player.status = 'Left_Walk'
                self.player.direction.x = -1
            elif key[pygame.K_d]:
                self.player.status = 'Right_Walk'
                self.player.direction.x = 1
            else:
                self.player.direction.x = 0
            if key[pygame.K_SPACE]:
                if not self.player.vulnerable and self.ui.current_stamina >= 12:
                    self.ui.remove_stamina(12)
                    self.player.attack_time = perf_counter()
                    self.player.attacking = True
                    self.create_attack()
                
    def keys_input(self,key):
        if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
            if not self.object_collide:
                if key[pygame.K_p]:
                    if not self.clicking:
                        self.clicking = True
                        self.click_time = perf_counter()
                        self.place_block(self.mouse_offset)
            if key[pygame.K_q]:
                if not self.clicking:
                    self.clicking = True
                    self.click_time = perf_counter()
                    self.drop_item()
        if key[pygame.K_i]:
            if not self.clicking and not self.object_collide:
                self.clicking = True
                self.click_time = perf_counter()
                self.ground_class.ground_logic(self.mouse_offset,self.ground,self.perlin.biomes)
        for index,input in enumerate(self.keyboard_input):
            if key[input]:
                self.ui.change = True
                self.ui.selected_slot = [index,0]

    #---------------------------Farming logic----------------------------------
                    
    def seed_ground(self):
        self.ground_class.seeding_logic(self.ground,self.ui,self.mouse_offset,
                                        self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name,
                                        self.current_time)
    def harvest(self):
        self.ground_class.harvest(self.ground,self.ui,self.mouse_offset)
    def tree_info(self):
        self.ground_class.show_info(self.ground,self.mouse_offset,self.current_time)
        
    #----------------------------------Block logic-----------------------------------
    def break_block(self,sprite,hold_timer):
        if hold_timer >= self.time_to_hold:
            sprite.kill()
            self.hold_timer = 0
            self.breaking_pos = None
            offset = pygame.math.Vector2(randint(-64,64),randint(-64,64))
            if randint(0,2) == 1:
                Item(sprite, sprite.rect.center+offset, [self.visible_sprites,self.interactables],False,1)
            elif randint(0,2) == 2:
                Item(sprite, sprite.rect.center+offset, [self.visible_sprites,self.interactables],True,1)
    def place_block(self,mouse_pos):
        mouse_offset = mouse_pos//tile_size
        land = self.ground[mouse_offset[1]][mouse_offset[0]]
        biome = self.perlin.biomes[mouse_offset[1]][mouse_offset[0]]
        if not self.ground_class.beach_check(biome):
            if biome != 'water' and not land['ground'] == 'plowed_ground':
                if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type_before == 'block' and self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'item_drop':
                    Object(mouse_offset*tile_size, [self.visible_sprites,self.obstacle_sprites,self.interactables], self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name)
                    self.remove_item(self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def display_breaking(self,sprite,hold_time,max_time):
        self.under_sprite_pos = sprite.rect.center - self.offset - (42,0)
        bg_rect = self.breaking_surf.get_rect(topleft=(0,0))
        ratio = hold_time / max_time
        current_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * ratio
        self.breaking_surf.fill('black')
        pygame.draw.rect(self.breaking_surf,'red',current_rect)
        pygame.draw.rect(self.breaking_surf,'black',bg_rect,2)

    #------------------------------Item logic----------------------------------------

    def drop_item(self):
        Item(self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'], self.player.rect.topleft + self.player.facing_offset,[self.visible_sprites, self.interactables],
             True if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'seed' else False,1)
        self.remove_item(self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def collect_item(self,sprite):
        if self.ui.add_item(sprite,sprite.amount):
            sprite.kill()
    def remove_item(self,sprite):
        self.ui.remove_item(sprite,1)

    #--------------------------------ESSENTIALS------------------------------------

    def cooldowns(self):
        if self.clicking:
            if self.current_time - self.click_time >= self.click_cooldown:
                self.clicking = False

    def merge_item(self):
        prev_sprite1 = None
        prev_sprite2 = None
        for sprite1 in self.interactables.sprites():
            if sprite1.type == 'item_drop' or sprite1.type == 'seed':
                img = sprite1.image.copy()
                txt = self.font.render(str(sprite1.amount),True,'white')
                pos = (sprite1.pos[0],round(sin(perf_counter()*8)*3)+sprite1.pos[1])
                img.blit(txt,(font_offset,font_offset))
                self.display_surface.blit(img, pos)
                for sprite2 in self.interactables.sprites():
                    if sprite1.type == sprite2.type and sprite1.name == sprite2.name:
                        if sprite1 != sprite2:
                            if prev_sprite1 != sprite2 and prev_sprite2 != sprite1:
                                if sprite1.rect.colliderect(sprite2.rect):
                                    prev_sprite1 = sprite1
                                    prev_sprite2 = sprite2
                                    #+self.offset in the next line cuz the sprite isnt drawed in self.visible_sprites look line 159
                                    Item(sprite1,sprite1.pos+self.offset,[self.visible_sprites,self.interactables],
                                        True if sprite1.type == 'seed' else False,
                                        sprite1.amount + sprite2.amount)
                                    sprite1.kill()
                                    sprite2.kill()

    def animations(self):
        if self.breaking:
           self.display_surface.blit(self.breaking_surf,self.under_sprite_pos)
        else:
            self.hold_timer = 0
            
        if self.ground_class.time_left != None:
            txt = pygame.font.SysFont(None,48).render(str(self.ground_class.time_left), True, (255, 255, 255))
            txt_box = pygame.Surface((len(str(self.ground_class.time_left))*18,28))
            txt_box.blit(txt,(0,0))
            self.display_surface.blit(txt_box,self.mouse_pos-pygame.math.Vector2(0,32))

    def create_dt(self):
        self.current_time = perf_counter()
        self.dt = self.current_time - self.last_time
        if self.dt > 0.1:
            self.dt = 0.1
        self.last_time = self.current_time

    def get_offset(self):
        self.map_edge = False

        if not self.map_edge:
            self.offset.x = self.player.rect.centerx - WIDTH // 2
            self.offset.y = self.player.rect.centery - HEIGHT // 2
        else:
            self.offset.x = self.player.rect.centerx
            self.offset.y = self.player.rect.centery
            
        if self.offset.x < 0: self.offset.x, self.map_edge = 0, True
        if self.offset.x > self.offset_limit.x: self.offset.x, self.map_edge = self.offset_limit.x, True
        if self.offset.y < 0: self.offset.y, self.map_edge = 0, True
        if self.offset.y > self.offset_limit.y: self.offset.y, self.map_edge = self.offset_limit.y, True
                    
    def update_sprites(self,click):
        self.get_offset()
        self.input(click)
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
        if self.attackable_sprites:
            for target_sprite in self.attackable_sprites:
                if self.attack_sprites:
                    for attack_sprite in self.attack_sprites:
                        collision_sprites = attack_sprite.rect.colliderect(target_sprite.rect)
                        if collision_sprites:
                            if not target_sprite.being_attacked and target_sprite.name == 'enemy':
                                target_sprite.get_damage(self.player, attack_sprite.name)
                        else:
                            target_sprite.being_attacked = False
                else:
                    target_sprite.being_attacked = False

    def damage_player(self, amount, attack_type, pos, disable_attack):
        disable_attack()
        self.ui.remove_health(amount)
        self.player.hurt_time = perf_counter()
        self.animation_player.create_particles(attack_type, pos, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_death_particles(pos,[self.visible_sprites])

    def add_exp(self, amount):
        self.ui.current_exp += amount

    def update_visible_sprites(self):
        for sprite in self.visible_sprites:
            if sprite.type != 'entity':
                sprite.update()
            else:
                sprite.update(self.current_time,self.dt)

    def run(self,click):
        self.create_dt()
        self.update_sprites(click)
        self.player_attack_update()
        self.visible_sprites.draw(self.offset)
        self.visible_sprites.enemy_update(self.player)
        self.update_visible_sprites()
        self.ui.update(click,self.current_time,self.dt)
        self.merge_item()
        self.animations()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self,map,map_rect,offset_limit):
        super().__init__()
        self.map = map
        self.map_rect = map_rect
        self.offset_limit = offset_limit

    def draw(self,offset):
        self.map_pos = self.map_rect.topleft - offset
        pygame.display.get_surface().blit(self.map, self.map_pos)
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            sprite.pos = sprite.rect.topleft - offset
            if not sprite.type == 'item_drop' and not sprite.type == 'seed':
                pygame.display.get_surface().blit(sprite.image, sprite.pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'name') and sprite.name == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
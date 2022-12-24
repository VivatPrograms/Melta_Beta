from code import interact
from random import randint, choice, randrange
from math import sin
from time import perf_counter
import copy
from Enemy import Enemy
from Settings import *
from Object import Object
from ObjectDisplay import ObjectDisplay
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
        self.create_map()
        self.display_surface = pygame.display.get_surface()
        self.offset_limit = pygame.math.Vector2(self.map_rect.width-WIDTH,self.map_rect.height-HEIGHT)
        self.border = pygame.math.Vector2(self.map_rect.width-round(tile_size*reshape_game.x),self.map_rect.height-round(tile_size*reshape_game.y))
        #import classes
        self.visible_sprites = YSortCameraGroup(self.map,self.map_rect,self.offset_limit)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.player = Player((grid_width // 2 * round(tile_size*reshape_game.x), grid_width // 2 * round(tile_size*reshape_game.y)),
         [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.border)
        self.animation_player = AnimationPlayer()
        self.perlin = PerlinNoise()
        self.ui = UI(self.player,self.visible_sprites,self.interactables)
        # self.magic_player = MagicPlayer(self.animation_player)
        self.Tile_map = import_sprite_sheet('../graphics/Tilemap.png',(tile_size,tile_size))
        #click cooldown
        self.zoom_scale = 1
        self.object_display = None
        self.press = False
        self.attacking = False
        self.attacked = False
        self.click_cooldown = 0.4
        self.clicking_cooldown = None
        self.click_time = None
        self.clicking = False
        self.offset = pygame.math.Vector2()
        self.object_collide = False
        self.using_hoe = False
        self.hoeing_time = 0.4
        self.placing = False
        #breaking
        self.time_to_hold = 100
        #map
        self.generate_map()
        #ui
        self.open_chest = False
        self.keyboard_input = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
        self.pressed = False
        self.font = pygame.font.Font('../font/mc_font.ttf', round(32*reshape_game.x))
        self.last_time = perf_counter()
        self.ui.add_item(Item(Object((0,0),None,'black_pickaxe'),(0,0),None,False,1),200)
        self.ui.add_item(Item(Object((0,0),None,'black_axe'),(0,0),None,False,1),64)
        self.ui.add_item(Item(Object((0,0),None,'black_hoe'),(0,0),None,False,1),64)
        self.ui.add_item(Item(Object((0,0),None,'black_sword_1'),(0,0),None,False,1),64)
        self.ui.add_item(Item(Object((0,0),None,'oak_tree'),(0,0),None,False,1),64)
        self.ui.add_item(Item(Object((0,0),None,'oak_chest'),(0,0),None,False,1),64)
        self.ui.add_item(Item(Object((0,0),None,'oak_chest'),(0,0),None,True,1),64)

    def create_map_chunks(self):
        chunks = []
        number_of_chunks = grid_width // chunk_size
        for y in range(number_of_chunks):
            chunks.append([])
            for lst in chunks:
                lst.append(pygame.Surface((round(tile_size*reshape_game.x)*chunk_size,round(tile_size*reshape_game.y)*chunk_size)))
        return chunks
    def create_map(self):
        self.map = pygame.Surface((round(tile_size*reshape_game.x)*grid_width,round(tile_size*reshape_game.y)*grid_width))
        self.map_rect = self.map.get_rect()
    #Map creation/Object creation
    def generate_map(self):
        self.coords = []
        self.perlin.generate_noise()
        self.grid = self.perlin.container
        for key in self.grid.keys():
            for coord in self.grid[key]:
                self.coords.append(coord)
                #general setup
                rect = pygame.Rect((coord[0],coord[1]),(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
                #obstacles/enemies
                for name in objects:
                    if key == name:
                        Object(coord,[self.visible_sprites,self.obstacle_sprites,self.interactables],choice(names[name]))
                for name in biomes:
                    if key == name:
                        img = pygame.image.load(f'../graphics/tiles/{name}.png').convert_alpha()
                        tile_size_ratio = pygame.math.Vector2(self.map_rect.width)
                        self.map.blit(pygame.transform.scale(img,(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y))), rect)
        self.ground = copy.deepcopy(self.perlin.biomes)
        self.ground_class = Ground(self.map,self.Tile_map,self.ground,self.visible_sprites,self.interactables)
        for y in self.perlin.biomes:
            for x in self.perlin.biomes[y]:
                self.ground[y][x] = {'ground':self.perlin.biomes[y][x],'seeded_ground':False,'seed':None,
                'growth_time':None,'end_time':None,'all_time':None,'mixed':False}
        self.spawn_enemy(10)

    def spawn_enemy(self,times):
        for _ in range(times):
            random_coord = choice(self.coords)
            Enemy('axolot', random_coord, [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                    self.damage_player, self.trigger_destruction_particles, self.add_exp, self.border)
        
    # ---------------------------Input-------------------------------

    def input(self,click):
        try:
            self.menu_input(click)
            if not self.ui.active_menu == 'player_crafting_table':
                if not self.ui.active_menu == 'crafting_table':
                    self.farm_input()
            elif not self.ui.active_menu == 'crafting_table':
                if not self.ui.active_menu == 'player_crafting_table':
                    self.farm_input()
        except KeyError:
            pass
            
    def farm_input(self):
        if pygame.mouse.get_pressed()[2] and not self.object_collide:
            if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
                if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type == 'seed':
                    self.seed_ground()
        elif pygame.mouse.get_pressed()[0] and not self.object_collide:
            self.harvest()
        elif not pygame.mouse.get_pressed()[0] and not self.object_collide:
            self.tree_info()

    def change_active(self,menu_name):
        if self.ui.active_menu == menu_name:
            self.ui.active_menu = None
        else:
            try:
                if not 'options' in self.ui.active_menu: self.ui.active_menu = menu_name
            except TypeError: self.ui.active_menu = menu_name

    def keybind_input(self,key,keybind):
        if key[ord(keybind)]:
            return True
        return False

    def menu_input(self,click):
        key = pygame.key.get_pressed()
        if key[ord(keybinds['Basic crafting menu'])]:
            if not self.pressed:
                self.pressed = True
                self.ui.inventory_open = True
                if self.ui.active_menu == 'chest':
                    self.ui.active_menu = None
                    self.ui.return_drag()
                elif not self.ui.active_menu == 'crafting_table':
                    self.change_active('player_crafting_table')
                    if not self.ui.active_menu == 'player_crafting_table':
                        self.ui.return_items(self.ui.crafting_menu) 
                        self.ui.return_drag()
                else:
                    self.change_active('crafting_table')
                    if not self.ui.active_menu == 'crafting_table':
                        self.ui.return_items(self.ui.big_crafting_menu)
                        self.ui.return_drag()
        elif key[pygame.K_ESCAPE]:
            if not self.pressed:
                self.pressed = True
                self.ui.inventory_open = True
                if self.ui.active_menu:
                    if self.ui.active_menu != 'options':
                        self.ui.active_menu = 'options'
                    else:
                        self.ui.active_menu = None
                else:
                    self.ui.active_menu = 'options'
        else:
            self.pressed = False
        for y in self.ground:
            for x in self.ground[y]:
                if self.ground[y][x]['seeded_ground']:
                    self.ground_class.run(self.ground,y,x,self.current_time)
        if not self.ui.active_menu:
            self.movement_input(key)
        else:
            self.player.direction.x = 0
            self.player.direction.y = 0
        self.keys_input(key,click)
        
    def movement_input(self,key):
        if not self.player.attacking:
            #movement input
            if key[ord(keybinds['Walk up'])]:
                self.player.status = 'Up_Walk'
                self.player.direction.y = -1
            elif key[ord(keybinds['Walk down'])]:
                self.player.status = 'Down_Walk'
                self.player.direction.y = 1
            else:
                self.player.direction.y = 0
            if key[ord(keybinds['Walk left'])]:
                self.player.status = 'Left_Walk'
                self.player.direction.x = -1
            elif key[ord(keybinds['Walk right'])]:
                self.player.status = 'Right_Walk'
                self.player.direction.x = 1
            else:
                self.player.direction.x = 0
            if key[ord(keybinds['Attack'])]:
                if not self.player.vulnerable and self.ui.current_stamina >= 12:
                    if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
                        if self.ui.check_item(self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]],['sword','lance']):
                            self.player.weapon = self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name
                            self.ui.remove_stamina(12)
                            self.player.attack_time = perf_counter()
                            self.player.attacking = True
                            self.create_attack()
                
    def keys_input(self,key,click):
        self.placing = False
        self.selected_slot_input(key)
        if key[61]: self.zoom_scale += 0.075
        if key[45]: self.zoom_scale -= 0.075
        if not self.ui.active_menu:
            if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None:
                if key[ord(keybinds['Drop selected item'])]:
                    if not self.clicking:
                        self.clicking = True
                        self.click_time = perf_counter()
                        self.drop_item()
        if key[ord(keybinds['Create farmable land'])]:
            if not self.clicking and not self.object_collide:
                self.clicking = True
                self.click_time = perf_counter()
                self.ground_class.ground_logic(self.mouse_map_offset,self.ground,self.perlin.biomes)
        elif key[ord(keybinds['Enable/disable inventory'])]:
            if not self.press and not self.ui.active_menu:
                self.ui.inventory_open = not self.ui.inventory_open
                if not self.ui.inventory_open:
                    self.ui.return_drag()
            self.press = True
        else:
            self.press = False

    def selected_slot_input(self,key):
        try:
            if not 'options' in self.ui.active_menu: self.change_selected_slot(key)
        except TypeError: self.change_selected_slot(key)
    
    def change_selected_slot(self,key):
        for slot in list_of_slots:
            if key[ord(keybinds[slot])]:
                self.ui.change = True
                self.ui.selected_slot = [int(slot[-1])-1,0]

    #---------------------------Farming logic----------------------------------
                    
    def seed_ground(self):
        self.ground_class.seeding_logic(self.ground,self.ui,self.mouse_map_offset,
                                        self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name,
                                        self.current_time)
    def harvest(self):
        if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'] != None and 'hoe' in self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name:
            if self.ground_class.harvest(self.ground,self.ui,self.mouse_map_offset,self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name):
                self.using_hoe = True
                self.hoe_time = perf_counter()
                self.set_status(self.check_negative(self.mouse_offset))
        else:
            self.ground_class.harvest(self.ground,self.ui,self.mouse_map_offset,'None')
    def tree_info(self):
        self.ground_class.show_info(self.ground,self.mouse_map_offset,self.current_time)
        
    #----------------------------------Block logic-----------------------------------
    def reachable_placement(self,pos):
        reachable_distance = tile_size*resize*5
        obj_display_vector = pygame.math.Vector2(pos)
        player_vector = pygame.math.Vector2(self.player.rect.center)
        distance = (player_vector-obj_display_vector).magnitude()
        if distance <= reachable_distance:
            return True
        return False
    def reachable_sprite(self,sprite):
        reachable_distance = tile_size*resize*3
        sprite_vector = pygame.math.Vector2(sprite.rect.center)
        player_vector = pygame.math.Vector2(self.player.rect.center)
        distance = (player_vector-sprite_vector).magnitude()
        if distance <= reachable_distance:
            return True
        sprite.being_damaged = False
        sprite.damage_received = 0
        return False
    def breaking_process(self,sprite,all_breaking):
        for break_sprite in all_breaking:
            if break_sprite == all_breaking[0]:
                self.block = sprite
                sprite.being_damaged = True
                sprite.damage_received += self.deal_breaking_damage(20,self.dt,sprite)
            else:
                sprite.being_damaged = False
                sprite.damage_received = 0
        self.break_block(self.block)
        self.draw_breaking(self.block,self.time_to_hold)
    def breaking_speed(self,sprite):
        for types in ['oak','birch','redwood']:
            if types in sprite.name:
                sprite.damage_received += self.deal_damage(20 * self.dt)
                break
    def break_block(self,sprite):
        if sprite.damage_received >= self.time_to_hold:
            sprite.kill()
            sprite.damage_received = 0
            self.breaking_pos = None
            offset = pygame.math.Vector2(randrange(-64,64),randrange(-64,64))
            if randint(0,2) == 1:
                Item(sprite, sprite.rect.center+offset, [self.visible_sprites,self.interactables],False,1)
            elif randint(0,2) == 2:
                Item(sprite, sprite.rect.center+offset, [self.visible_sprites,self.interactables],True,1)
            self.trigger_destruction_particles(sprite.rect.topleft,(32,32),sprite.rect)
    def place_block(self):
        land = self.ground[self.mouse_map_offset[1]][self.mouse_map_offset[0]]
        biome = self.perlin.biomes[self.mouse_map_offset[1]][self.mouse_map_offset[0]]
        if land['ground'] != 'plowed_ground':
            if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type_before == 'block' and self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].folder == 'placeables':
                if self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].type != 'seed':
                    Object(self.tile_offset, [self.visible_sprites,self.obstacle_sprites,self.interactables], self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'].name)
                    self.remove_item(self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
    def draw_breaking(self,sprite,max_time):
        sprite.damage_bar_pos = sprite.rect.center - self.offset - (42*reshape_game.x,0)
        bg_rect = sprite.damage_bar.get_rect(topleft=(0,0))
        ratio = sprite.damage_received / max_time
        current_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * ratio
        sprite.damage_bar.fill(dark_color['health'])
        pygame.draw.rect(sprite.damage_bar,'#FF6961',current_rect)
        pygame.draw.rect(sprite.damage_bar,'#3a3a50',bg_rect,round(2*resize))
    def deal_breaking_damage(self,dmg,dt,sprite):
        slot = self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]
        if slot['ID'] != None:
            if 'axe' in slot['ID'].name:
                if self.axe_breakables(sprite.name) and not 'pickaxe' in slot['ID'].name:
                    return (dmg*dt) * breaking_speed[slot['ID'].name.split('_')[0]]
                if not self.axe_breakables(sprite.name) and 'pickaxe' in slot['ID'].name:
                    return (dmg*dt) * breaking_speed[slot['ID'].name.split('_')[0]]
        return dmg*dt
    def axe_breakables(self,name):
        for wood_type in ['oak','birch','redwood','cactus']:
            if wood_type in name:
                return True
        return False
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
        if self.using_hoe:
            if self.current_time - self.hoe_time >= self.hoeing_time:
                self.using_hoe = False

    def player_input(self,click,sprite,all_breaking):
        if sprite.type == 'item_drop' or sprite.type == 'seed':
            if self.player.hitbox.colliderect(sprite.rect):
                self.collect_item(sprite)
        if self.reachable_sprite(sprite):
            if sprite.rect.collidepoint(self.mouse_offset):
                self.object_collide = True
                if click == 3 and 'table' in sprite.name:
                    if not self.placing and sprite.type == 'block':
                        self.ui.active_menu = 'crafting_table'
                elif click == 3 and 'chest' in sprite.name:
                    if not self.placing and sprite.type == 'block':
                        self.ui.active_menu = 'chest'
                        self.open_chest = sprite
                        self.ui.ui_update(self.ui.chest_menu_surf,self.open_chest.chest_inventory,False)
                elif pygame.mouse.get_pressed()[0]:
                    if sprite.type == 'block':
                        all_breaking.append(sprite)
                        self.breaking_process(sprite,all_breaking)
                else:
                    sprite.being_damaged = False
                    sprite.damage_received = 0
            else:
                sprite.being_damaged = False
                sprite.damage_received = 0

    def merge_item(self,click):
        prev_sprite1 = None
        prev_sprite2 = None
        self.object_collide = False
        all_breaking = []
        for sprite1 in self.interactables.sprites():
            if not self.ui.active_menu: self.player_input(click,sprite1,all_breaking)
            if sprite1.type == 'item_drop' or sprite1.type == 'seed':
                img = sprite1.image.copy()
                txt = self.font.render(str(sprite1.amount),False,'white')
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

    def display_breaking(self,sprite):
        slot = self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]
        if slot['ID'] != None:
            if 'axe' in slot['ID'].name:
                img = pygame.transform.rotate(slot['ID'].inv_image.copy(),sin(perf_counter()*15)*45)
                img = pygame.transform.flip(img,self.check_negative(self.block.rect.center),False)
                self.display_surface.blit(img,(self.player.rect.topleft-tool_offset[self.check_negative(self.block.rect.center)])-self.offset)
        self.set_status(self.check_negative(self.block.rect.center))
        if sprite.damage_received != 0:
            self.display_surface.blit(sprite.damage_bar,sprite.damage_bar_pos)

    def set_status(self,left):
        if left:
            self.player.status = self.player.status.replace(self.player.status.split('_')[0],'Left')
        else:
            self.player.status = self.player.status.replace(self.player.status.split('_')[0],'Right')

    def check_negative(self,pos):
        num = pygame.math.Vector2(self.player.rect.center) - pos
        if num[0] >= 0:
            negative = True
        else:
            negative = False
        return negative

    def animations(self):
        all_time = self.ground[self.mouse_map_offset[1]][self.mouse_map_offset[0]]['all_time']
        for sprite in self.interactables.sprites():
            if sprite.type == 'block':
                if sprite.being_damaged:
                    self.display_breaking(sprite)
                else:
                    sprite.damage_received = 0
        if self.using_hoe:
            slot = self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]
            img = pygame.transform.rotate(slot['ID'].inv_image.copy(),sin(perf_counter()*15)*45)
            img = pygame.transform.flip(img,self.check_negative(self.mouse_offset),False)
            self.display_surface.blit(img,(self.player.rect.topleft-tool_offset[self.check_negative(self.mouse_offset)])-self.offset)
        if all_time != None:
            txt_box = pygame.Surface((len(f'{round(growth_time-all_time)} seconds until harvest')*round(12*reshape_game.x),round(28*reshape_game.x)))
            rect = txt_box.get_rect(center=self.mouse_pos-(4*reshape_game.x,4*reshape_game.y))
            txt = pygame.font.Font('../font/mc_font.ttf',round(24*reshape_game.x)).render((f'{round(growth_time-all_time)} seconds until harvest'), True, (255, 255, 255))
            pygame.draw.rect(self.display_surface,'#93E9BE',rect)
            self.display_surface.blit(txt,txt_box.get_rect(center=self.mouse_pos))
            pygame.draw.rect(self.display_surface,'#3a3a50',rect,round(2*resize))

    def create_dt(self):
        self.current_time = perf_counter()
        self.dt = self.current_time - self.last_time
        if self.dt > 0.1:
            self.dt = 0.1
        self.last_time = self.current_time

    def get_offset(self):
        self.mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mouse_offset = self.mouse_pos + self.offset
        self.mouse_map_offset = pygame.math.Vector2()
        self.mouse_map_offset.x = self.mouse_offset.x//round(tile_size*reshape_game.x)
        self.mouse_map_offset.y = self.mouse_offset.y//round(tile_size*reshape_game.y)
        self.tile_offset = pygame.math.Vector2()
        self.tile_offset.x = self.mouse_map_offset.x*round(tile_size*reshape_game.x)
        self.tile_offset.y = self.mouse_map_offset.y*round(tile_size*reshape_game.y)
        self.offset.x = self.player.rect.centerx - WIDTH // 2
        self.offset.y = self.player.rect.centery - HEIGHT // 2
            
        if self.offset.x < 0: self.offset.x = 0
        if self.offset.x > self.offset_limit.x: self.offset.x = self.offset_limit.x
        if self.offset.y < 0: self.offset.y = 0
        if self.offset.y > self.offset_limit.y: self.offset.y = self.offset_limit.y

    def update_sprites(self):
        self.get_offset()
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
        self.animation_player.create_particles(attack_type, pos, [self.visible_sprites],pygame.Rect((pos),(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y))))

    def trigger_destruction_particles(self, pos, size, spriterect):
        self.animation_player.create_destruction_particles(pos,[self.visible_sprites],size,spriterect)

    def add_exp(self, amount):
        self.ui.current_exp += amount

    def show_block(self):
        if self.ui.active_menu == None and self.reachable_placement(self.mouse_offset):
            return True
        return False

    def update_visible_sprites(self):
        self.object_display = ObjectDisplay(self.tile_offset-self.offset, self.ui.inventory_menu[self.ui.selected_slot[1]][self.ui.selected_slot[0]]['ID'])
        color = (100,136,234)
        for sprite in self.visible_sprites:
            if sprite.type != 'entity':
                sprite.update()
                if sprite.type == 'block' and sprite.open_chest:
                    self.display_chest(sprite)
            else:
                sprite.update(self.current_time,self.dt)
            rect = pygame.Rect((sprite.rect.topleft-self.offset),(sprite.rect.width,sprite.rect.height))
            if self.object_display.block and rect.colliderect(self.object_display.rect):
                color = '#FF6961'
                break
        if self.reachable_placement(self.mouse_offset) and self.object_display.block: self.object_display.draw(color)
        if pygame.mouse.get_pressed()[2]:
            if not self.clicking and self.object_display.block:
                if self.reachable_placement(self.mouse_offset) and color == (100,136,234):
                    self.clicking = True
                    self.click_time = perf_counter()
                    self.place_block()
                    self.placing = True

    def back_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            if not self.pressed:
                self.pressed = True
                if self.ui.active_menu:
                    if self.ui.active_menu != 'main_menu_options':
                        self.ui.active_menu = 'main_menu_options'
                    else:
                        self.ui.active_menu = None
                else:
                    self.ui.active_menu = 'main_menu_options'
        else:
            self.pressed = False
    
    def game(self,click):
        self.player_attack_update()
        self.update_sprites()
        self.input(click)
        self.visible_sprites.draw(self.offset)
        self.visible_sprites.enemy_update(self.player)
        self.merge_item(click)
        self.update_visible_sprites()
        self.animations()
    def main_menu(self):
        self.back_input()
        img = pygame.transform.scale(background_img,(WIDTH,HEIGHT))
        self.display_surface.blit(img,(0,0))

    def run_state(self,click):
        self.create_dt()
        if self.ui.ingame:
            self.game(click)
        else:
            self.main_menu()

    def run(self,click,key_press):
        self.run_state(click)
        self.ui.update(click,key_press,self.current_time,self.dt,self.open_chest if self.open_chest else None)

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
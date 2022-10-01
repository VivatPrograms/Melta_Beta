from multiprocessing import allow_connection_pickling
from Settings import *
from Crafting_recipes import *
from Object import Object
from Item import Item
import copy

class UI:
    def __init__(self,player,visible_sprites,interactables):
        super().__init__()
        #general stuff
        self.player = player
        self.visible_sprites = visible_sprites
        self.interactables = interactables
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        #setup
        self.dragging = False
        self.dragging_item = None
        self.dragging_amount = None
        self.main_menu = False
        self.crafting_table = False
        self.change = False
        self.clicking = False
        self.click_cooldown = 0.4
        self.upgrade_cost = 45
        self.selected_slot = [0,0]
        self.selected_crafting_slot = [0,0]
        self.selected_big_crafting_slot = [0,0]
        self.selected_output_slot = [0,0]
        self.bar = pygame.Surface((3*tile_size, tile_size))
        self.upgrade = pygame.Surface((tile_size,5*tile_size))
        #stats rects
        self.health_rect = self.bar.get_rect(topleft=(0,0))
        self.stamina_rect = self.bar.get_rect(topleft=(0,tile_size))
        self.level_rect = pygame.Rect((0,2*tile_size),(tile_size, tile_size))
        self.exp_rect = pygame.Rect((tile_size,2*tile_size),(2*tile_size, tile_size))
        self.upgrade_rect = self.upgrade.get_rect(topleft=(0,3*tile_size))
        #current stats
        self.current_health = 75
        self.current_stamina = 30
        self.current_exp = 540
        #inventory
        self.inventory_menu = {0:{0: {'ID':None,'amount':0},1:{'ID':None,'amount':0},2:{'ID':None,'amount':0},
                        3:{'ID':None,'amount':0},4:{'ID':None,'amount':0},5:{'ID':None,'amount':0},
                        6:{'ID':None,'amount':0},7:{'ID':None,'amount':0},8:{'ID':None,'amount':0}}}
        self.inventory_surf = pygame.Surface((9*tile_size,1*tile_size))
        self.inventory_rect = self.inventory_surf.get_rect(center=(WIDTH // 2, HEIGHT - 32))
        #crafting
        self.crafting_menu = {0: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}},
                              1: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}}}
        self.crafting_surf = pygame.Surface((2*tile_size,2*tile_size))
        self.crafting_rect = self.crafting_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        #crafting table
        self.big_crafting_menu = {0: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}, 2: {'ID': None, 'amount': 0}},
                                1: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}, 2: {'ID': None, 'amount': 0}},
                                2: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}, 2: {'ID': None, 'amount': 0}}}
        self.big_crafting_surf = pygame.Surface((3*tile_size,3*tile_size))
        self.big_crafting_rect = self.big_crafting_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + tile_size//2))
        #crafting item
        self.output_menu = {0: {0: {'ID': None, 'amount': 0}}}
        self.output_surf = pygame.Surface((tile_size,tile_size))
        self.output_rect = self.output_surf.get_rect(center=self.crafting_rect.center - pygame.math.Vector2(0,self.crafting_rect.height-32))
        #draw ui
        self.ui_update(self.inventory_surf,self.inventory_menu,True)
        self.ui_update(self.crafting_surf,self.crafting_menu,False)
        self.ui_update(self.big_crafting_surf,self.big_crafting_menu,False)
        self.ui_update(self.output_surf,self.output_menu,False)
        self.display_all_upgrades()

    def check_item(self,slot,names):
        for name in names:
            if name in slot['ID'].name:
                return True
            return False

    def add_item(self, ID, amount):
        self.change = True
        for y in self.inventory_menu.keys():
            for slot in self.inventory_menu[y].values():
                if slot['ID'] != None and ID != None:
                    if slot['ID'].name == ID.name and slot['ID'].type == ID.type:
                        slot['amount'] += amount
                        return True

        for y in self.inventory_menu.keys():
            for slot in self.inventory_menu[y].values():
                if slot['ID'] == None:
                    slot['ID'] = ID
                    slot['amount'] += amount
                    return True      
                
        self.drop()
        return False
    
    def drop(self,menu):
        for y in menu.keys():
            for x in menu[y].keys():
                slot = menu[y][x]
                if slot['ID'] != None:
                    Item(slot['ID'], self.player.rect.topleft + self.player.facing_offset,[self.visible_sprites, self.interactables],
                        True if slot['ID'].type == 'seed' else False, 1)
                    self.remove(slot,1)
        return False

    def remove_item(self, ID, amount):
        self.change = True
        old_menu = {}
        for key, value in self.inventory_menu.items():
            old_menu[key] = {**value}

        for y in self.inventory_menu.keys():
            for slot in self.inventory_menu[y].values():
                if slot['ID'] == ID:
                    if slot['amount'] >= amount:
                        slot['amount'] -= amount
                        if slot['amount'] == 0:
                            slot['ID'] = None
                        return True
                    else:
                        amount -= slot['amount']
                        slot['ID'] = None
                        slot['amount'] = 0

        self.inventory_menu = old_menu
        return False

    def input(self,click):
        self.mouse_pos = pygame.mouse.get_pos()
        if click:
            if self.main_menu:
                if self.crafting_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.crafting_menu,self.crafting_rect,[self.selected_crafting_slot],False,True)
                    elif click == 3:
                        self.slot_input(self.crafting_menu,self.crafting_rect,[self.selected_crafting_slot],True,True)
                    self.change = True
                elif self.output_rect.collidepoint(self.mouse_pos):
                    self.slot_input(self.output_menu,self.output_rect,[self.selected_output_slot],True,True)
                    self.change = True
                elif self.upgrade_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.upgrade_input()
                elif self.inventory_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],False,True)
                        self.change = True
                    elif click == 3:
                        self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],True,True)
                        self.change = True
            elif self.crafting_table:
                if self.big_crafting_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.big_crafting_menu,self.big_crafting_rect,[self.selected_crafting_slot],False,True)
                    elif click == 3:
                        self.slot_input(self.big_crafting_menu,self.big_crafting_rect,[self.selected_big_crafting_slot],True,True)
                    self.change = True
                elif self.output_rect.collidepoint(self.mouse_pos):
                    self.slot_input(self.output_menu,self.output_rect,[self.selected_output_slot],True,True)
                    self.change = True
                elif self.upgrade_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.upgrade_input()
                elif self.inventory_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],False,True)
                        self.change = True
                    elif click == 3:
                        self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],True,True)
                        self.change = True
            else:
                if self.inventory_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],False,False)
                        self.change = True
                    elif click == 3:
                        self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],True,False)
                        self.change = True

    def upgrade_input(self):
        for y in range(5):
            slot = pygame.Rect(pygame.math.Vector2(0 * tile_size, y * tile_size) + self.upgrade_rect.topleft,(tile_size, tile_size))
            if slot.collidepoint(self.mouse_pos):
                self.upgrade_stat(y)
                
    def upgrade_stat(self,index):
        stat = stats[index]
        if self.current_exp >= self.upgrade_cost:
            if player_data[stat] < player_max[stat]:
                player_data[stat] = player_data[stat] * 1.1
            self.current_exp -= self.upgrade_cost

    def slot_input(self,menu,rect,selected_slot,right_click,allow_drag):
        for y in menu.keys():
            for x in menu[y]:
                slot = pygame.Rect(pygame.math.Vector2(x * tile_size, y * tile_size) + rect.topleft,(tile_size, tile_size))
                if slot.collidepoint(self.mouse_pos):
                    if self.dragging and self.dragging_item['ID'] != None:
                        if not menu == self.output_menu:
                            self.drop_item(y,x,menu)
                        else:
                            if allow_drag:
                                if self.dragging_item['ID'] != None and self.output_menu[y][x]['ID'] != None:
                                    if self.dragging_item['ID'].name == self.output_menu[y][x]['ID'].name:
                                        self.dragging_amount += 1
                                        self.delete()
                    elif not self.dragging and menu[y][x]['ID'] != None:
                        if allow_drag:
                            self.dragging = True
                            self.dragging_item = menu[y][x].copy()
                            self.dragging_item['ID'].amount = self.get_amount(right_click)
                            self.remove(menu[y][x],self.dragging_amount)
                            if menu == self.output_menu:
                                self.delete()
                    selected_slot[0][0] = x
                    selected_slot[0][1] = y

    def return_drag(self):
        if self.dragging:
            self.add_item(self.dragging_item['ID'],self.dragging_amount)
            self.kill_dragging()
                    
    def get_amount(self,right_click):
        if not right_click:
            self.dragging_amount = self.dragging_item['amount']
        elif right_click:
            if self.dragging_item['amount'] >= 2:
                self.dragging_amount = self.dragging_item['amount']//2
            else:
                self.dragging_amount = self.dragging_item['amount']
        return self.dragging_item['amount']
                    
    def cooldowns(self,time):
        if self.clicking:
            if time - self.click_time >= self.click_cooldown:
                self.clicking = False

    def drop_item(self,y,x,menu):
        if menu[y][x]['ID'] != None:
            if self.dragging_item['ID'].name == menu[y][x]['ID'].name:
                if self.dragging_item['ID'].type == menu[y][x]['ID'].type:
                    menu[y][x]['amount'] += self.dragging_amount
                    self.kill_dragging()
                else:
                    if self.dragging_item['ID'].type == 'item_drop' and menu[y][x]['ID'].type == 'seed':
                        menu[y][x]['ID'], self.dragging_item['ID'] = self.dragging_item['ID'], menu[y][x]['ID']
                        menu[y][x]['amount'], self.dragging_amount = self.dragging_amount, menu[y][x]['amount']
                    elif self.dragging_item['ID'].type == 'seed' and menu[y][x]['ID'].type == 'item_drop':
                        menu[y][x]['ID'], self.dragging_item['ID'] = self.dragging_item['ID'], menu[y][x]['ID']
                        menu[y][x]['amount'], self.dragging_amount = self.dragging_amount, menu[y][x]['amount']
            else:
                menu[y][x]['ID'], self.dragging_item['ID'] = self.dragging_item['ID'], menu[y][x]['ID']
                menu[y][x]['amount'], self.dragging_amount = self.dragging_amount, menu[y][x]['amount']
        else:
            menu[y][x]['ID'] = self.dragging_item['ID']
            menu[y][x]['amount'] += self.dragging_amount
            self.kill_dragging()
        
    def kill_dragging(self):
        self.dragging_item = None
        self.dragging_amount = None
        self.dragging = False
            
    def remove(self,menu,subtract):
        self.change = True
        if menu['amount'] >= subtract:
            menu['amount'] -= subtract
            if menu['amount'] == 0:
                menu['ID'] = None
        else:
            menu['ID'] = None
            menu['amount'] = 0

    def ui_update(self,surf,menu,allow):
        if menu != None:
            surf.fill('black')
            for y in menu.keys():
                if y != 'ID' or y != 'amount':
                    for x in menu[y].keys():
                        if menu[y][x]['ID'] != None:
                            text = self.font.render(str(menu[y][x]['amount']), True, 'white')
                            font_rect = text.get_rect(topleft=(tile_size * x + font_offset, tile_size * y + font_offset))
                            surf.blit(menu[y][x]['ID'].inv_image, (x * tile_size, y * tile_size))
                            surf.blit(text, font_rect)
                        pygame.draw.rect(surf, 'gold', pygame.Rect((x * tile_size, y * tile_size), (tile_size, tile_size)), 2)
                        if allow:
                            pygame.draw.rect(surf, 'aqua', pygame.Rect((self.selected_slot[0] * tile_size, 0), (tile_size, tile_size)), 2)
        else:
            self.output_surf.fill('black')
            if self.crafting_item != None:
                img = pygame.image.load(f'../graphics/objects/{self.crafting_item.name}.png').subsurface(
                    pygame.Rect((0, 0), (tile_size, tile_size)))
                self.output_surf.blit(img, (0, 0))
            pygame.draw.rect(self.output_surf, 'gold', pygame.Rect((0, 0), (tile_size, tile_size)), 2)
        
    def delete(self):
        if self.main_menu:
            for y in self.crafting_menu.keys():
                for x in self.crafting_menu[y].keys():
                    self.remove(self.crafting_menu[y][x],1)
        elif self.crafting_table:
            for y in self.big_crafting_menu.keys():
                for x in self.big_crafting_menu[y].keys():
                    self.remove(self.big_crafting_menu[y][x],1)

    def outputs(self):
        x_level = []
        y_level = []
        if self.main_menu:
            crafting = [[None,None],[None,None]]
            crafting2 = [[None,None],[None,None]]
            self.output(self.crafting_menu,x_level,y_level,crafting,crafting2)
            self.crafting(crafting,crafting2,crafting[0]+crafting[1],3,x_level,y_level)
        elif self.crafting_table:
            crafting = [[None,None,None],[None,None,None],[None,None,None]]
            crafting2 = [[None,None,None],[None,None,None],[None,None,None]]
            self.output(self.big_crafting_menu,x_level,y_level,crafting,crafting2)
            self.crafting(crafting,crafting2,crafting[0]+crafting[1]+crafting[2],8,x_level,y_level)

    def crafting(self,crafting,crafting2,lists,index,x_level,y_level):
        for types in recipes.keys():
            self.kill_loop = False
            for key in recipes[types].keys():
                craft = crafting.copy()
                craft = self.get_craft(craft)
                for recipe in recipes[types][key]:
                    if types == 0:
                        if lists.count(recipe) == 1 and lists.count(None) == index:
                            self.do_output(key)  
                            break
                        else:
                            self.dont_output() 
                    elif types == 1:
                        if craft == recipe and x_level[0] == x_level[1]:
                            if y_level[0] + 1 == y_level[1] or y_level[0] - 1 == y_level[1]: 
                                self.do_output(key) 
                                break
                        else:
                            self.dont_output() 
                    elif types == 2:
                        if craft == recipe and y_level[0] == y_level[1]:
                            if x_level[0] - 1 == x_level[1] or x_level[0] + 1 == x_level[1]: 
                                self.do_output(key) 
                                break
                        else:
                            self.dont_output() 
                    elif types == 3:
                        if craft == recipe:
                            if x_level[0] + x_level[1] == x_level[2] + x_level[3]:
                                self.do_output(key) 
                                break  
                        else:
                            self.dont_output() 
                    elif types == 4:
                        if crafting2 == recipe:
                            self.do_output(key) 
                            break  
                        else:
                            self.dont_output() 
                if self.kill_loop:
                    break
            if self.kill_loop:
                break

    def get_craft(self,craft):
        for n in range(len(craft)):
            self.repeat_delete(craft)
        if [] in craft:
            craft.remove([])
        return craft

    def repeat_delete(self,craft):
        for lst in craft:
            for j in lst: 
                if j == None:
                    lst.remove(None)

    def output(self,menu,x_,y_,crafting,crafting2):
        for y in menu.keys():
            for x in menu[y].keys():
                if menu[y][x]['ID'] != None:
                    if menu[y][x]['ID'].type != 'seed':
                        crafting[y][x] = menu[y][x]['ID'].name
                        crafting2[y][x] = menu[y][x]['ID'].name
                        x_.append(x) 
                        y_.append(y)
                else:
                    crafting[y][x] = None
                    crafting2[y][x] = None
        return crafting
                    
    def dont_output(self):
        self.crafting_item = None
        self.output_menu[0][0]['ID'] = self.crafting_item 
        self.output_menu[0][0]['amount'] = 0
        
    def do_output(self,key):
        self.crafting_item = Item(Object((0,0),None,key),(0,0),None,False,1)
        self.output_menu[0][0]['ID'] = self.crafting_item 
        self.output_menu[0][0]['amount'] += 1 
        self.kill_loop = True  
                    
    def return_items(self,menu):
        self.dont_output()
        for y in menu.keys():
            for x in menu[y].keys():
                if menu[y][x]['ID'] != None:
                    self.add_item(menu[y][x]['ID'],menu[y][x]['amount'])
                    self.remove(menu[y][x],menu[y][x]['amount'])
                    
    def display_all_stats(self):
        self.display_stats('health',self.current_health,self.health_rect,'red')
        self.display_stats('stamina',self.current_stamina,self.stamina_rect,'aqua')
        self.display_level('white')
        self.display_stats('exp',self.current_exp-(self.current_exp//50*50),self.exp_rect,'green')
        
    def display_stats(self,stat,current,rect,color):
        ratio = current / player_data[stat]
        current_rect = rect.copy()
        current_rect.width = rect.width * ratio
        pygame.draw.rect(self.display_surface,'black',rect) 
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,'black',rect,2) 
        
    def display_level(self,color):
        text = pygame.font.Font(None,86).render(str(self.current_exp // player_data['exp']), True, color)
        pos = self.level_rect.topright - self.get_pos(len(str(self.current_exp // 50)))
        pygame.draw.rect(self.display_surface,'black',self.level_rect) 
        self.display_surface.blit(text,pos)
    
    def get_pos(self,length):
        if length == 1:
            pos = pygame.math.Vector2(48, -4)
        else:
            pos = pygame.math.Vector2(tile_size * len(str(self.current_exp // 50)) // len(str(self.current_exp // 50)), -4)
        return pos

    def remove_stamina(self,amount):
        self.current_stamina -= amount
        if self.current_stamina <= 0:
            self.current_stamina = 0

    def remove_health(self,amount):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def regain_hp_stamina(self,dt):
        if self.current_health < player_data['health']:
            self.current_health += player_data['health'] * 0.015 * dt
        if self.current_stamina < player_data['stamina']:
            self.current_stamina += player_data['stamina'] * 0.05 * dt
    
    def display_all_upgrades(self):
        self.display_upgrade('red',(0,tile_size*0))
        self.display_upgrade('aqua',(0,tile_size*1))
        self.display_upgrade('white',(0,tile_size*2))
        self.display_upgrade('brown',(0,tile_size*3))
        self.display_upgrade('darkred',(0,tile_size*4))
        
    def display_upgrade(self,color,pos):
        pygame.draw.rect(self.upgrade,color,pygame.Rect((pos),(tile_size, tile_size))) 

    def other(self):
        if self.change:
            self.ui_update(self.inventory_surf,self.inventory_menu,True)
            self.ui_update(self.crafting_surf,self.crafting_menu,False)
            self.ui_update(self.big_crafting_surf,self.big_crafting_menu,False)
            self.outputs()
            self.ui_update(self.output_surf,self.output_menu,False)
            self.change = False
        if self.dragging == True and self.dragging_item['ID'] != None:
            txt = self.font.render(str(self.dragging_amount),True,'white')
            dragging_surface = pygame.Surface((tile_size,tile_size), pygame.SRCALPHA, 32).convert_alpha()
            dragging_surface.blit(self.dragging_item['ID'].image,(0,0))
            dragging_surface.blit(txt,(font_offset,font_offset))
            self.display_surface.blit(dragging_surface,self.mouse_pos)

    def draw(self):
        self.display_all_stats()
        self.display_all_upgrades()
        self.display_surface.blit(self.inventory_surf, self.inventory_rect)
        if self.main_menu:
            self.display_surface.blit(self.crafting_surf,self.crafting_rect)
            self.display_surface.blit(self.output_surf,self.output_rect)
            self.display_surface.blit(self.upgrade,self.upgrade_rect)
        elif self.crafting_table:
            self.display_surface.blit(self.big_crafting_surf,self.big_crafting_rect)
            self.display_surface.blit(self.output_surf,self.output_rect)
            self.display_surface.blit(self.upgrade,self.upgrade_rect)

    def update(self,click,time,dt):
        self.cooldowns(time)
        self.input(click)
        self.regain_hp_stamina(dt)
        self.draw()
        self.other()
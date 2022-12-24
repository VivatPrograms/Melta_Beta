from Settings import *
from Crafting_recipes import *
from Object import Object
from Item import Item
from Button import Button
from Textbox import TextBox
class UI:
    def __init__(self,player,visible_sprites,interactables):
        super().__init__()
        #general stuff
        self.player = player
        self.visible_sprites = visible_sprites
        self.interactables = interactables
        self.display_surface = pygame.display.get_surface()
        self.font_size = round(24 * resize)
        self.font = pygame.font.Font('../font/mc_font.ttf', self.font_size)
        #setup
        self.pressed = False
        self.changing_keybind = False
        self.dragging = False
        self.active_menu = None
        self.ingame = True
        self.change = False
        self.main_menu = False
        self.crafting_table = False
        self.clicking = False
        self.click_cooldown = 0.4
        self.upgrade_cost = 45
        self.selected_slot = [0,0]
        self.selected_other_slot = [0,0]
        self.bar = pygame.Surface((4.5*round(tile_size*reshape_game.x), self.font_size))
        self.upgrade = pygame.Surface((self.font_size*reshape_game.x,5*round(tile_size*reshape_game.y)))
        #inventory
        self.inventory_open = True
        self.inventory_menu = {0:{0: {'ID':None,'amount':0},1:{'ID':None,'amount':0},2:{'ID':None,'amount':0},
                        3:{'ID':None,'amount':0},4:{'ID':None,'amount':0},5:{'ID':None,'amount':0},
                        6:{'ID':None,'amount':0},7:{'ID':None,'amount':0},8:{'ID':None,'amount':0}}}
        self.inventory_surf = pygame.Surface((9*round(tile_size*reshape_game.x),1*round(tile_size*reshape_game.y)))
        self.inventory_rect = self.inventory_surf.get_rect(center=(WIDTH // 2, HEIGHT - 32 - HEIGHT//10))
        #crafting
        self.crafting_menu = {0: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}},
                              1: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}}}
        self.crafting_surf = pygame.Surface((2*round(tile_size*reshape_game.x),2*round(tile_size*reshape_game.y)))
        self.crafting_rect = self.crafting_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        #crafting table
        self.big_crafting_menu = {0: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}, 2: {'ID': None, 'amount': 0}},
                                1: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}, 2: {'ID': None, 'amount': 0}},
                                2: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}, 2: {'ID': None, 'amount': 0}}}
        self.big_crafting_surf = pygame.Surface((3*round(tile_size*reshape_game.x),3*round(tile_size*reshape_game.y)))
        self.big_crafting_rect = self.big_crafting_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + round(tile_size*reshape_game.y)//2))
        #crafting item
        self.output_menu = {0: {0: {'ID': None, 'amount': 0}}}
        self.output_surf = pygame.Surface((round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
        self.output_rect = self.output_surf.get_rect(center=self.crafting_rect.center - pygame.math.Vector2(0,self.crafting_rect.height-32*reshape_game.y))
        #chest
        self.chest_menu_surf = pygame.Surface((9*round(tile_size*reshape_game.x),3*round(tile_size*reshape_game.y)))
        self.chest_menu_rect = self.chest_menu_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        #stats rects
        self.health_rect = self.bar.get_rect(topleft=(self.inventory_rect.x,self.inventory_rect.y-self.font_size))
        self.stamina_rect = self.bar.get_rect(topleft=(self.inventory_rect.x+4.5*round(tile_size*reshape_game.x),self.inventory_rect.y-self.font_size))
        self.level_rect = pygame.Rect((self.inventory_rect.centerx-self.font_size//2,self.inventory_rect.y-3.5*self.font_size),(self.font_size*2*reshape_game.x, self.font_size*2*reshape_game.y))
        self.exp_rect = pygame.Rect((self.inventory_rect.x,self.inventory_rect.y-1.5*self.font_size),(9*round(tile_size*reshape_game.x), self.font_size//2))
        self.upgrade_rect = self.upgrade.get_rect(topleft=(0,3*round(self.font_size*reshape_game.y)))
        self.health_upgrades = 0
        self.stamina_upgrades = 0
        #current stats
        self.current_health = 75
        self.current_stamina = 30
        self.current_exp = 540
        #buttons
        self.buttons = [Button('MAIN MENU',(WIDTH//2,HEIGHT//4.5),['main_menu_options'],'options_button',['options'],self.font,None),
                        Button('CONTROLS',(WIDTH//2,HEIGHT//4.5+1.25*height_offset['options_button']),['control_options'],'options_button',['options'],self.font,None),
                        Button('WORLD SEARCH',(WIDTH//2,HEIGHT//4.5+2.5*height_offset['options_button']),['world_search_options'],'options_button',['options'],self.font,None),
                        Button('UPGRADES',(WIDTH//2,HEIGHT//4.5+3.75*height_offset['options_button']),['upgrades_options'],'options_button',['options'],self.font,None),
                        Button(keybinds['Walk up'],(WIDTH//4,HEIGHT//6+0*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Walk up'),
                        Button(keybinds['Walk left'],(WIDTH//4,HEIGHT//6+1*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Walk left'),
                        Button(keybinds['Walk down'],(WIDTH//4,HEIGHT//6+2*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Walk down'),
                        Button(keybinds['Walk right'],(WIDTH//4,HEIGHT//6+3*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Walk right'),
                        Button(keybinds['Enable/disable inventory'],(WIDTH//4,HEIGHT//6+4*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Enable/disable inventory'),
                        Button(keybinds['Create farmable land'],(WIDTH//4,HEIGHT//6+5*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Create farmabale land'),
                        Button(keybinds['Basic crafting menu'],(WIDTH//4,HEIGHT//6+6*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Basic crafting menu'),
                        Button(keybinds['Drop selected item'],(WIDTH//4,HEIGHT//6+7*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Drop selected item'),
                        Button(keybinds['Attack'],(WIDTH//4,HEIGHT//6+8*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Attack'),
                        Button(keybinds['Select slot 1'],(WIDTH//1.5,HEIGHT//6+0*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 1'),
                        Button(keybinds['Select slot 2'],(WIDTH//1.5,HEIGHT//6+1*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 2'),
                        Button(keybinds['Select slot 3'],(WIDTH//1.5,HEIGHT//6+2*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 3'),
                        Button(keybinds['Select slot 4'],(WIDTH//1.5,HEIGHT//6+3*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 4'),
                        Button(keybinds['Select slot 5'],(WIDTH//1.5,HEIGHT//6+4*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 5'),
                        Button(keybinds['Select slot 6'],(WIDTH//1.5,HEIGHT//6+5*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 6'),
                        Button(keybinds['Select slot 7'],(WIDTH//1.5,HEIGHT//6+6*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 7'),
                        Button(keybinds['Select slot 8'],(WIDTH//1.5,HEIGHT//6+7*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 8'),
                        Button(keybinds['Select slot 9'],(WIDTH//1.5,HEIGHT//6+8*height_offset['options_button']),['control_options'],'key_button',['control_options'],self.font,'Select slot 9'),
                        Button('PLAY',(WIDTH//2,HEIGHT//3.5+2.5*height_offset['options_button']),['connect_options'],'options_button',['main_menu_options'],self.font,None),
                        Button('CONNECT',(WIDTH//1.5,HEIGHT//6+5*height_offset['options_button']),['world_search_options'],'options_button',['connect_options'],self.font,None),
                        ]
        self.text_boxes = [
            TextBox((WIDTH//1.5,HEIGHT//6+0*height_offset['options_button']),'connect_options',self.font),
            TextBox((WIDTH//1.5,HEIGHT//6+1*height_offset['options_button']),'connect_options',self.font)
        ]
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

    def input(self,click,key_press,open_chest):
        self.inventories_input(click,open_chest)
        self.buttons_input(click)
        self.textboxes_input(click,key_press)
        self.change_keybind(key_press)

    def change_keybind(self,key_press):
        if self.changing_keybind and key_press:
            try:
                keybinds[self.changing_keybind.explanation] = chr(key_press)
                self.changing_keybind.name = chr(key_press)
                self.changing_keybind.draw_image('key_button')
                self.changing_keybind = False
            except ValueError: pass

    def buttons_input(self,click):
        for button in self.buttons:
            for i in range(len(button.button_from)):
                if button.button_from[i] == self.active_menu:
                    if self.active_menu != 'control_options':
                        self.changing_keybind = False
                    if button.rect.collidepoint(self.mouse_pos):
                        button.offset = 4
                        if click == 1:
                            if self.active_menu == 'control_options':
                                if self.changing_keybind: self.changing_keybind.draw_image('key_button')
                                button.draw_image('selected_key_button')
                                self.changing_keybind = button
                            self.active_menu = button.button_to[i]
                            self.check_if_ingame()
                            break
                    else:
                        button.offset = 0

    def check_if_ingame(self):
        if self.active_menu == 'main_menu_options': self.ingame = False
        elif self.active_menu == None: self.ingame = True

    def textboxes_input(self,click,key_press):
        key = pygame.key.get_pressed()
        for textbox in self.text_boxes:
            if textbox.textbox_from == self.active_menu:
                if textbox.rect.collidepoint(self.mouse_pos) and click == 1:
                    textbox.selected = True
                elif not textbox.rect.collidepoint(self.mouse_pos) and click == 1:
                    textbox.selected = False
            if textbox.selected:
                letter = None
                if key_press:
                    try:
                        if chr(key_press) in legal_letters or key_press == 8: letter = key_press
                    except ValueError: pass
                if letter:
                    if not self.pressed:
                        if letter == 8: 
                            textbox.text = self.remove_last_str(textbox.text)
                            self.pressed = True
                        else: 
                            if len(textbox.text) <= text_limit:
                                textbox.text = textbox.text + chr(self.return_fixed_letter(key,letter))
                                self.pressed = True
                else: self.pressed = False
                textbox.draw_img()

    def return_fixed_letter(self,key,letter):
        if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]: return ord(chr(letter).upper())
        elif pygame.key.get_mods() == pygame.KMOD_CAPS: return ord(chr(letter).upper())
        return letter

    def remove_last_str(self,txt):
        text = txt[:-1]
        return text
                    
    def inventories_input(self,click,open_chest):
        self.mouse_pos = pygame.mouse.get_pos()
        if click:
            if self.active_menu == 'player_crafting_table':
                if self.crafting_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.crafting_menu,self.crafting_rect,[self.selected_other_slot],False,True)
                    elif click == 3:
                        self.slot_input(self.crafting_menu,self.crafting_rect,[self.selected_other_slot],True,True)
                    self.change = True
                elif self.output_rect.collidepoint(self.mouse_pos):
                    self.slot_input(self.output_menu,self.output_rect,[self.selected_other_slot],True,True)
                    self.change = True
                elif self.upgrade_rect.collidepoint(self.mouse_pos):
                    if click == 1:self.upgrade_input()
                elif self.inventory_rect.collidepoint(self.mouse_pos):self.inventory_collisions(click)
            elif self.active_menu == 'crafting_table':
                if self.big_crafting_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(self.big_crafting_menu,self.big_crafting_rect,[self.selected_other_slot],False,True)
                    elif click == 3:
                        self.slot_input(self.big_crafting_menu,self.big_crafting_rect,[self.selected_other_slot],True,True)
                    self.change = True
                elif self.output_rect.collidepoint(self.mouse_pos):
                    self.slot_input(self.output_menu,self.output_rect,[self.selected_other_slot],True,True)
                    self.change = True
                elif self.upgrade_rect.collidepoint(self.mouse_pos):
                    if click == 1:self.upgrade_input()
                elif self.inventory_rect.collidepoint(self.mouse_pos):self.inventory_collisions(click)
            elif self.active_menu == 'chest':
                if self.chest_menu_rect.collidepoint(self.mouse_pos):
                    if click == 1:
                        self.slot_input(open_chest.chest_inventory,self.chest_menu_rect,[self.selected_other_slot],False,True)
                    elif click == 3:
                        self.slot_input(open_chest.chest_inventory,self.chest_menu_rect,[self.selected_other_slot],True,True)
                    self.change = True
                elif self.upgrade_rect.collidepoint(self.mouse_pos):
                    if click == 1:self.upgrade_input()
                elif self.inventory_rect.collidepoint(self.mouse_pos):self.inventory_collisions(click)
            else:
                if self.inventory_rect.collidepoint(self.mouse_pos):
                    if self.inventory_open:
                        if click == 1:
                            self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],False,False)
                            self.change = True
                        elif click == 3:
                            self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],True,False)
                            self.change = True

    def inventory_collisions(self,click):
        if self.inventory_open:
            if click == 1:
                self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],False,True)
                self.change = True
            elif click == 3:
                self.slot_input(self.inventory_menu,self.inventory_rect,[self.selected_slot],True,True)
                self.change = True

    def upgrade_input(self):
        for y in range(5):
            slot = pygame.Rect(pygame.math.Vector2(0 * round(tile_size*reshape_game.x), y * round(tile_size*reshape_game.y)) + self.upgrade_rect.topleft,(round(tile_size*reshape_game.x), round(tile_size*reshape_game.y)))
            if slot.collidepoint(self.mouse_pos):
                self.upgrade_stat(y)

    def slot_input(self,menu,rect,selected_slot,right_click,allow_drag):
        for y in menu.keys():
            for x in menu[y]:
                slot = pygame.Rect(pygame.math.Vector2(x * round(tile_size*reshape_game.x), y * round(tile_size*reshape_game.y)) + rect.topleft,
                (round(tile_size*reshape_game.x), round(tile_size*reshape_game.y)))
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

    def upgrade_stat(self,index):
        stat = stats[index]
        if self.current_exp >= self.upgrade_cost:
            if player_data[stat] < player_max[stat]:
                player_data[stat] = player_data[stat] * 1.1
                self.current_exp -= self.upgrade_cost
                if stat == 'health':
                    self.health_upgrades += 1
                elif stat == 'stamina':
                    self.stamina_upgrades += 1

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
            for y in menu.keys():
                if y != 'ID' or y != 'amount':
                    for x in menu[y].keys():
                        img = pygame.transform.scale(pygame.image.load('../graphics/items/unplaceables/other/slot_inside.png'),(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
                        surf.blit(img,(x * round(tile_size * reshape_game.x), y * round(tile_size * reshape_game.y)))
                        if menu[y][x]['ID'] != None:
                            text = self.font.render(str(menu[y][x]['amount']), False, 'white')
                            font_rect = text.get_rect(topleft=(round(reshape_game.x*tile_size) * x + font_offset,round(reshape_game.y*tile_size) * y + font_offset))
                            surf.blit(menu[y][x]['ID'].inv_image, (x * round(tile_size * reshape_game.x), y * round(tile_size * reshape_game.y)))
                            surf.blit(text, font_rect)
                        img = pygame.transform.scale(pygame.image.load('../graphics/items/unplaceables/other/slot.png'),(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
                        surf.blit(img,(x * round(tile_size * reshape_game.x), y * round(tile_size * reshape_game.y)))
                        if allow:
                            img = pygame.transform.scale(pygame.image.load('../graphics/items/unplaceables/other/selected_slot.png'),(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
                            surf.blit(img,(self.selected_slot[0] * round(tile_size * reshape_game.x), y * round(tile_size * reshape_game.y)))
        else:
            img = pygame.transform.scale(pygame.image.load('../graphics/items/unplaceables/other/slot_inside.png'),(round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
            self.output_surf.blit(img,(0, 0))
            if self.crafting_item != None:
                img = pygame.image.load(f'../graphics/objects/{self.crafting_item.name}.png').subsurface(
                    pygame.Rect((0, 0), (round(tile_size*reshape_game.x), round(tile_size*reshape_game.y))))
                self.output_surf.blit(img, (0, 0))
            pygame.draw.rect(self.output_surf, 'gold', pygame.Rect((0, 0), (round(tile_size*reshape_game.x), round(tile_size*reshape_game.y))), 2)
        
    def delete(self):
        if self.active_menu == 'player_crafting_table':
            for y in self.crafting_menu.keys():
                for x in self.crafting_menu[y].keys():
                    self.remove(self.crafting_menu[y][x],1)
        elif self.active_menu == 'crafting_table':
            for y in self.big_crafting_menu.keys():
                for x in self.big_crafting_menu[y].keys():
                    self.remove(self.big_crafting_menu[y][x],1)

    def outputs(self):
        x_level = []
        y_level = []
        if self.active_menu == 'player_crafting_table':
            crafting = [[None,None],[None,None]]
            crafting2 = [[None,None],[None,None]]
            self.output(self.crafting_menu,x_level,y_level,crafting,crafting2)
            self.crafting(crafting,crafting2,crafting[0]+crafting[1],3,x_level,y_level)
        elif self.active_menu == 'crafting_table':
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
        self.display_stats('health',self.current_health,self.health_rect,'#FF6961')
        self.display_stats('stamina',self.current_stamina,self.stamina_rect,'#6488ea')
        self.display_level('white')
        self.display_stats('exp',self.current_exp-(self.current_exp//50*50),self.exp_rect,'#71eeb8')
        
    def display_stats(self,stat,current,rect,color):
        ratio = current / player_data[stat]
        current_rect = rect.copy()
        current_rect.width = rect.width * ratio
        pygame.draw.rect(self.display_surface,dark_color[stat],rect) 
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,'#3a3a50',rect,round(2*resize)) 
        if stat == 'stamina' and self.inventory_menu[self.selected_slot[1]][self.selected_slot[0]]['ID'] != None:
            if self.check_item(self.inventory_menu[self.selected_slot[1]][self.selected_slot[0]],['sword','lance']):
                self.draw_attack_line(stat,rect)
    
    def draw_attack_line(self,stat,rect):
        new_ratio = 12/player_data[stat]*rect.width
        start_pos = (new_ratio+rect.x,rect.y+2)
        end_pos = (new_ratio+rect.x,rect.y+self.font_size-3)
        pygame.draw.line(self.display_surface,'#fbeee4',start_pos,end_pos,3)

    def display_level(self,color):
        if self.current_exp // 50 > 0:
            text = pygame.font.Font('../font/mc_font.ttf',self.font_size*2).render(str(self.current_exp // player_data['exp']), False, color)
            pos = (self.exp_rect.centerx-self.font_size*self.get_pos(len(str(self.current_exp // 50))),self.exp_rect.y-self.font_size*1.5)
            self.display_surface.blit(text,pos)
    
    def get_pos(self,length):
        return 0.5*length

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
            self.current_health += 0.025 + 0.2*self.health_upgrades * dt
        if self.current_stamina < player_data['stamina']:
            self.current_stamina += 0.045 + 0.025*self.stamina_upgrades * dt
    
    def display_all_upgrades(self):
        self.display_upgrade('red',(0,tile_size*0))
        self.display_upgrade('aqua',(0,tile_size*1))
        self.display_upgrade('white',(0,tile_size*2))
        self.display_upgrade('brown',(0,tile_size*3))
        self.display_upgrade('darkred',(0,tile_size*4))
        
    def display_upgrade(self,color,pos):
        pygame.draw.rect(self.upgrade,color,pygame.Rect((pos),(round(tile_size*reshape_game.x), round(tile_size*reshape_game.y)))) 
        
    def draw(self,open_chest):
        self.display_all_upgrades()
        if self.active_menu == 'player_crafting_table':
            self.display_surface.blit(self.crafting_surf,self.crafting_rect)
            self.display_surface.blit(self.output_surf,self.output_rect)
            self.display_surface.blit(self.upgrade,self.upgrade_rect)
        elif self.active_menu == 'crafting_table':
            self.display_surface.blit(self.big_crafting_surf,self.big_crafting_rect)
            self.display_surface.blit(self.output_surf,self.output_rect)
            self.display_surface.blit(self.upgrade,self.upgrade_rect)
        elif self.active_menu == 'chest':
            self.display_surface.blit(self.chest_menu_surf,self.chest_menu_rect)
            self.display_surface.blit(self.upgrade,self.upgrade_rect)
        else:
            if self.active_menu != None:
                self.inventory_open = False
                for button in self.buttons:
                    for i in range(len(button.button_from)):
                        if button.button_from[i] == self.active_menu:
                            button.draw(i)
                            break
                for textbox in self.text_boxes:
                    if textbox.textbox_from == self.active_menu:
                        textbox.draw()

        if self.inventory_open:
            self.display_all_stats()
            self.display_surface.blit(self.inventory_surf, self.inventory_rect)
        #dragging drawing
        if self.change:
            self.ui_update(self.inventory_surf,self.inventory_menu,True)
            self.ui_update(self.crafting_surf,self.crafting_menu,False)
            self.ui_update(self.big_crafting_surf,self.big_crafting_menu,False)
            self.outputs()
            self.ui_update(self.output_surf,self.output_menu,False)
            if self.active_menu == 'chest':
                self.ui_update(self.chest_menu_surf,open_chest.chest_inventory,False)
            self.change = False
        if self.dragging == True and self.dragging_item['ID'] != None:
            txt = self.font.render(str(self.dragging_amount),False,'white')
            dragging_surface = pygame.Surface((round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)), pygame.SRCALPHA, 32).convert_alpha()
            dragging_surface.blit(self.dragging_item['ID'].image,(0,0))
            dragging_surface.blit(txt,(font_offset,font_offset))
            self.display_surface.blit(dragging_surface,self.mouse_pos)

    def update(self,click,key_press,time,dt,open_chest):
        self.cooldowns(time)
        self.input(click,key_press,open_chest)
        self.regain_hp_stamina(dt)
        self.draw(open_chest)
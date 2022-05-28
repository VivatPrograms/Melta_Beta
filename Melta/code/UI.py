import pygame
from Settings import *
from Crafting_recipes import *
from Object import Object
from Item import Item

class UI:
    def __init__(self):
        #general stuff
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        #input
        self.click_cooldown = 400
        self.clicking = False
        self.dragging_inv_item = False
        self.dragging_crafting_item = False
        self.selected_slot = [0,0]
        self.selected_crafting_slot = [0,0]
        self.inventory_change = True
        self.crafting_change = True
        #UI
        self.colliding = False
        self.ui_surface = pygame.Surface((WIDTH,HEIGHT))
        self.ui_rect = self.ui_surface.get_rect(topleft=(0,0))
        #inventory
        self.inventory = {0:{0: {'ID':None,'amount':0},1:{'ID':None,'amount':0},2:{'ID':None,'amount':0},
                        3:{'ID':None,'amount':0},4:{'ID':None,'amount':0},5:{'ID':None,'amount':0},
                        6:{'ID':None,'amount':0},7:{'ID':None,'amount':0},8:{'ID':None,'amount':0}}}
        self.inv_surf = pygame.Surface((9*tile_size,1*tile_size))
        self.inv_rect = self.inv_surf.get_rect(center=(WIDTH // 2, HEIGHT - 32))
        #crafting
        self.crafting_menu = {0: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}},
                              1: {0: {'ID': None, 'amount': 0}, 1: {'ID': None, 'amount': 0}}}
        self.crafting_surf = pygame.Surface((2*tile_size,2*tile_size))
        self.crafting_rect = self.crafting_surf.get_rect(topleft=(0,HEIGHT-2*tile_size))
        #crafting item
        self.crafting_item = None
        self.crafting_item_pos = (tile_size//2,HEIGHT-3*tile_size)
        self.crafting_item_surf = pygame.Surface((tile_size,tile_size))
        self.crafting_item_rect = self.crafting_item_surf.get_rect(topleft=self.crafting_item_pos)
        #general stuff
        self.ui_update(self.inv_surf,self.inventory,self.selected_slot)

    def add_item(self, ID, amount, menu):
        if menu == self.inventory:
            self.inventory_change = True
        elif menu == self.crafting_menu:
            self.crafting_change = True
        for y in menu.keys():
            for slot in menu[y].values():
                if slot['ID'] != None and ID != None:
                    if slot['ID'].name == ID.name:
                        slot['amount'] += amount
                        return True

        for y in menu.keys():
            for slot in menu[y].values():
                if slot['ID'] == None:
                    slot['ID'] = ID
                    slot['amount'] += amount
                    return True
        return False

    def remove_item(self, ID, amount, menu):
        if menu == self.inventory:
           self.inventory_change = True
        elif menu == self.crafting_menu:
            self.crafting_change = True
        old_menu = {}
        for key, value in menu.items():
            old_menu[key] = {**value}

        for y in menu.keys():
            for slot in menu[y].values():
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

        menu = old_menu
        return False

    def input(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if self.inv_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
            for y in self.inventory.keys():
                for x in self.inventory[y]:
                    pos = pygame.math.Vector2(x * tile_size, y * tile_size) + self.inv_rect.topleft
                    slot = pygame.Rect((pos), (tile_size, tile_size))
                    if slot.collidepoint(self.mouse_pos):
                        self.selected_slot = [x,y]
                        self.inventory_change = True
                        if not self.clicking:
                            self.dragging_inv_item = True
                            if self.dragging_crafting_item:
                                self.drag_n_drop([self.inventory,self.crafting_menu],[x,self.selected_crafting_slot[0]],[y,self.selected_crafting_slot[1]])
        elif self.crafting_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
            for y in self.crafting_menu.keys():
                for x in self.crafting_menu[y].keys():
                    pos = pygame.math.Vector2(x * tile_size, y * tile_size) + self.crafting_rect.topleft
                    slot = pygame.Rect((pos), (tile_size, tile_size))
                    if slot.collidepoint(self.mouse_pos):
                        self.selected_crafting_slot = [x,y]
                        self.crafting_change = True
                        if not self.clicking:
                            self.dragging_crafting_item = True
                            if self.dragging_inv_item:
                                self.drag_n_drop([self.crafting_menu,self.inventory],[x,self.selected_slot[0]],[y,self.selected_slot[1]])
        elif self.crafting_item_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
            if self.crafting_item != None:
                self.add_item(Item(Object((0,0),None,self.crafting_item),self.crafting_item_pos,None),1,self.inventory)
                for y in self.crafting_menu.keys():
                    for x in self.crafting_menu[y].keys():
                        self.remove(self.crafting_menu[y][x],1,self.crafting_menu[y][x]['amount'])
        elif pygame.mouse.get_pressed()[0]:
            self.dragging_inv_item = False
            self.dragging_crafting_item = False

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.clicking:
            if current_time - self.click_time >= self.click_cooldown:
                self.clicking = False

    def drag_n_drop(self,menu,x,y):
        if menu[0][y[0]][x[0]]['ID'] == None:
            if menu[1][y[1]][x[1]]['ID'] != None:
                menu[0][y[0]][x[0]]['ID'] = menu[1][y[1]][x[1]]['ID']
                menu[0][y[0]][x[0]]['amount'] += 1
                self.remove(menu[1][y[1]][x[1]], 1, menu[1][y[1]][x[1]]['amount'])
                self.clicking = True
                self.click_time = pygame.time.get_ticks()
        elif menu[0][y[0]][x[0]]['ID'] != None:
            if menu[1][y[1]][x[1]]['ID'] != None:
                if menu[0][y[0]][x[0]]['ID'].name == menu[1][y[1]][x[1]]['ID'].name:
                    menu[0][y[0]][x[0]]['amount'] += 1
                    self.remove(menu[1][y[1]][x[1]], 1, menu[1][y[1]][x[1]]['amount'])
                    self.clicking = True
                    self.click_time = pygame.time.get_ticks()

    def remove(self,menu,subtract,amount):
        self.inventory_change = True
        self.crafting_change = True
        if amount >= subtract:
            menu['amount'] -= subtract
            if menu['amount'] == 0:
                menu['ID'] = None
        else:
            menu['ID'] = None
            menu['amount'] = 0

    def drag_item(self,menu,slot,dragging):
        if menu[slot[1]][slot[0]]['ID'] != None:
            if dragging:
                self.display_surface.blit(menu[slot[1]][slot[0]]['ID'].image,self.mouse_pos)

    def ui_update(self,surf,menu,slot):
        if menu != None:
            surf.fill('black')
            for y in menu.keys():
                for x in menu[y].keys():
                    if menu[y][x]['ID'] != None:
                        text = self.font.render(str(menu[y][x]['amount']), True, 'white')
                        font_rect = text.get_rect(topleft=(tile_size * x + font_offset, tile_size * y + font_offset))
                        surf.blit(menu[y][x]['ID'].image, (x * tile_size, y * tile_size))
                        surf.blit(text, font_rect)
                    # outlines
                    if slot == [x,y]:
                        pygame.draw.rect(surf, 'red', pygame.Rect((x * tile_size, y * tile_size), (tile_size, tile_size)), 2)
                    else:
                        pygame.draw.rect(surf, 'gold', pygame.Rect((x * tile_size, y * tile_size), (tile_size, tile_size)), 2)
            if slot == self.selected_slot:
                self.inventory_change = False
            elif slot == self.selected_crafting_slot:
                self.crafting_change = False
        else:
            self.crafting_item_surf.fill('black')
            if self.crafting_item != None:
                img = pygame.image.load(f'../graphics/objects/{self.crafting_item}.png').subsurface(
                    pygame.Rect((0, 0), (tile_size, tile_size)))
                self.crafting_item_surf.blit(img, (0, 0))
            pygame.draw.rect(self.crafting_item_surf, 'gold', pygame.Rect((0, 0), (tile_size, tile_size)), 2)

    def crafting(self):
        crafting = [[None,None],[None,None]]
        for y in self.crafting_menu.keys():
            for x in self.crafting_menu[y].keys():
                if self.crafting_menu[y][x]['ID'] != None:
                    crafting[y][x] = self.crafting_menu[y][x]['ID'].name
        for key in recipes.keys():
            if crafting == recipes[key]:
                self.crafting_item = key
            else:
                self.crafting_item = None

    def other(self):
        if self.inventory_change:
            self.ui_update(self.inv_surf,self.inventory,self.selected_slot)
        if self.crafting_change:
            self.ui_update(self.crafting_surf,self.crafting_menu,self.selected_crafting_slot)
            self.crafting()
            self.ui_update(self.crafting_item_surf,None,None)
        if self.dragging_inv_item:
            self.drag_item(self.inventory,self.selected_slot,self.dragging_inv_item)
        if self.dragging_crafting_item:
            self.drag_item(self.crafting_menu,self.selected_crafting_slot,self.dragging_crafting_item)

    def draw(self):
        self.display_surface.blit(self.inv_surf, self.inv_rect)
        self.display_surface.blit(self.crafting_surf,self.crafting_rect)
        self.display_surface.blit(self.crafting_item_surf,self.crafting_item_rect)

    def update(self):
        self.cooldowns()
        self.input()
        self.draw()
        self.other()
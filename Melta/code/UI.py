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
        self.selected_slot = [0,0]
        self.selected_crafting_slot = [0,0]
        self.inventory_change = True
        self.crafting_change = True
        self.breaking_pos = None
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
        #dragging system
        self.dragging = False
        self.dragging_item = None
        #general stuff
        self.ui_update(self.inv_surf,self.inventory,self.selected_slot)
        self.int = 0

    def add_item(self, ID, amount):
        self.inventory_change = True
        self.crafting_change = True
        for y in self.inventory.keys():
            for slot in self.inventory[y].values():
                if slot['ID'] != None and ID != None:
                    if slot['ID'].name == ID.name:
                        slot['amount'] += amount
                        return True

        for y in self.inventory.keys():
            for slot in self.inventory[y].values():
                if slot['ID'] == None:
                    slot['ID'] = ID
                    slot['amount'] += amount
                    return True
        return False

    def remove_item(self, ID, amount):
        self.inventory_change = True
        self.crafting_change = True
        old_menu = {}
        for key, value in self.inventory.items():
            old_menu[key] = {**value}

        for y in self.inventory.keys():
            for slot in self.inventory[y].values():
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

        self.inventory = old_menu
        return False

    def input(self,click):
        self.mouse_pos = pygame.mouse.get_pos()
        if click:
            if self.inv_rect.collidepoint(self.mouse_pos):
                for y in self.inventory.keys():
                    for x in self.inventory[y]:
                        pos = pygame.math.Vector2(x * tile_size, y * tile_size) + self.inv_rect.topleft
                        slot = pygame.Rect((pos), (tile_size, tile_size))
                        if slot.collidepoint(self.mouse_pos):
                            if self.dragging and self.dragging_item['ID'] != None:
                                self.drop_item(y,x,self.inventory)
                            elif not self.dragging and self.inventory[y][x]['ID'] != None:
                                self.dragging = True
                                self.dragging_item = self.inventory[y][x]
                            self.selected_slot = [x,y]
                            self.inventory_change = True
            elif self.crafting_rect.collidepoint(self.mouse_pos):
                for y in self.crafting_menu.keys():
                    for x in self.crafting_menu[y].keys():
                        pos = pygame.math.Vector2(x * tile_size, y * tile_size) + self.crafting_rect.topleft
                        slot = pygame.Rect((pos), (tile_size, tile_size))
                        if slot.collidepoint(self.mouse_pos):
                            if self.dragging and self.dragging_item['ID'] != None:
                                self.drop_item(y,x,self.crafting_menu)
                            elif not self.dragging and self.crafting_menu[y][x]['ID'] != None:
                                self.dragging = True
                                self.dragging_item = self.crafting_menu[y][x]
                            self.selected_crafting_slot = [x,y]
                            self.crafting_change = True
            elif self.crafting_item_rect.collidepoint(self.mouse_pos):
                if self.crafting_item != None:
                    self.add_item(Item(Object((0,0),None,self.crafting_item),self.crafting_item_pos,None),1)
                    for y in self.crafting_menu.keys():
                        for x in self.crafting_menu[y].keys():
                            self.remove(self.crafting_menu[y][x],1,self.crafting_menu[y][x]['amount'])
            else:
                self.dragging = False
                self.dragging_item = None

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.clicking:
            if current_time - self.click_time >= self.click_cooldown:
                self.clicking = False

    def drop_item(self,y,x,menu):
        if menu[y][x]['ID'] != None:
            if self.dragging_item['ID'].name == menu[y][x]['ID'].name:
                menu[y][x]['amount'] += 1
                self.remove(self.dragging_item,1,self.dragging_item['amount'])
        else:
            menu[y][x]['ID'] = self.dragging_item['ID']
            menu[y][x]['amount'] += 1
            self.remove(self.dragging_item,1,self.dragging_item['amount'])
        self.dragging_item = None
        self.dragging = False
            
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
        if self.dragging == True and self.dragging_item['ID'] != None:
            self.display_surface.blit(self.dragging_item['ID'].image,self.mouse_pos)

    def draw(self):
        self.display_surface.blit(self.inv_surf, self.inv_rect)
        self.display_surface.blit(self.crafting_surf,self.crafting_rect)
        self.display_surface.blit(self.crafting_item_surf,self.crafting_item_rect)

    def update(self,click):
        self.cooldowns()
        self.input(click)
        self.draw()
        self.other()
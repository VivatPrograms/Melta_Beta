import pygame
from random import randint,choice
from Settings import *
from Item import Item
from Object import Object
from Crafting_recipes import tree_recipes

class Ground:
    def __init__(self,map,Tile_map):
        self.map = map
        self.Tile_map = Tile_map
        self.image = pygame.Surface((tile_size,tile_size))
        
    def ground_logic(self,mouse_pos,ground,perlin):
        mouse_offset = mouse_pos//tile_size
        biome = perlin[mouse_offset[1]][mouse_offset[0]]
        print(biome)
        if ground[mouse_offset[1]][mouse_offset[0]]['ground'] == 'plowed_ground':
            self.restore_ground(mouse_offset,ground,perlin)
        else:
            if biome != 'water':
                ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'plowed_ground'
                self.image.blit(self.Tile_map[2],(0,0))
                self.draw(mouse_offset)

    def seeding_logic(self,ground,ui,mouse_pos,seed):
        mouse_offset = mouse_pos//tile_size
        land = ground[mouse_offset[1]][mouse_offset[0]]
        if land['ground'] is 'plowed_ground':
            if land['seeded_ground']: 
                if land['seed'] is not seed and not land['mixed']:
                    if seed in tree_recipes[land['seed']]:
                        self.ground_changer(ground,mouse_offset,land['seeded_ground'],
                            tree_recipes[land['seed']][seed],growth_times[seed],True)
                        ui.remove(ui.inventory[ui.selected_slot[1]][ui.selected_slot[0]],1,
                                  ui.inventory[ui.selected_slot[1]][ui.selected_slot[0]]['amount'])
                        self.draw(mouse_offset)
            else:
                self.ground_changer(ground,mouse_offset,True,seed,growth_times[seed],False)
                ui.remove(ui.inventory[ui.selected_slot[1]][ui.selected_slot[0]],1,
                          ui.inventory[ui.selected_slot[1]][ui.selected_slot[0]]['amount'])
                self.draw(mouse_offset)
                
    def harvest(self,ground,ui,mouse_pos):
        mouse_offset = mouse_pos//tile_size
        land = ground[mouse_offset[1]][mouse_offset[0]]
        if land['ground'] is 'plowed_ground' and land['seeded_ground']:
            if land['growth_time'] is 0:
                self.randomise_tree(ui,land)
                self.ground_changer(ground,mouse_offset,False,None,None,False)
                self.image.blit(self.Tile_map[22*8+1],(0,0))
                self.draw(mouse_offset)
                
    def ground_changer(self,ground,mouse_offset,seeded_ground,seed,growth_time,mixed):
        ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] = seeded_ground
        ground[mouse_offset[1]][mouse_offset[0]]['seed'] = seed
        ground[mouse_offset[1]][mouse_offset[0]]['growth_time'] = growth_time
        ground[mouse_offset[1]][mouse_offset[0]]['mixed'] = mixed
                
    def randomise_tree(self,ui,land):
        seeds = self.amount_picker(True)
        blocks = self.amount_picker(False)
        if seeds > 0:
            ui.add_item(Item(Object((0,0),None,choice(names[land['seed']]),land['seed']),(0,0),None,True),seeds)
        ui.add_item(Item(Object((0,0),None,choice(names[land['seed']]),land['seed']),(0,0),None,False),blocks)
            
    def amount_picker(self,seeds):
        if seeds:
            return randint(0,1)
        else:
            return randint(1,4)
                
    def check_growth(self,ground,y,x):
        self.phase_update = None
        if ground[y][x]['seeded_ground']:
            if ground[y][x]['growth_time'] != None:
                if ground[y][x]['growth_time'] >= 1:
                    ground[y][x]['growth_time'] -= 1
                    if ground[y][x]['growth_time'] >= growth_times['tree'] // 2:
                        self.phase_update = 1
                    elif ground[y][x]['growth_time'] > 0:
                        self.phase_update = 2
                else:
                    ground[y][x]['growth_time'] = 0 
                    self.phase_update = 3

    def update_map(self,seed,y,x):
        if self.phase_update is not None:
            self.image.blit(self.Tile_map[22*8+1],(0,0))
            self.image.blit(pygame.image.load(f'../graphics/seeds/tree_phase_{self.phase_update}.png'),(0,0))
            self.draw(pygame.math.Vector2(x,y))
            
    def draw(self,mouse_offset):
        self.map.blit(self.image,mouse_offset*tile_size)
        
    def restore_ground(self,mouse_offset,ground,perlin):
        if perlin[mouse_offset[1]][mouse_offset[0]] == 'beach':
            self.map.blit(self.Tile_map[22*1+1],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'beach'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'forest':
            self.map.blit(self.Tile_map[22*11+3],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'forest'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'rainforest':
            self.map.blit(self.Tile_map[22*12+2],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'rainforest'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'savanna':
            self.map.blit(self.Tile_map[22*5+3],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'savanna'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'desert':
            self.map.blit(self.Tile_map[22*5],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'desert'
        elif perlin[mouse_offset[1]][mouse_offset[0]] == 'plains':
            self.map.blit(self.Tile_map[22*12+3],mouse_offset*tile_size)
            ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'plains'
        
    def run(self,ground,y,x):
        self.check_growth(ground,y,x)
        self.update_map(ground[y][x]['seed'],y,x)
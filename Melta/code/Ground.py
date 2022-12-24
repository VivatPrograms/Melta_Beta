import random
from Settings import *
from Item import Item
from Object import Object
from Crafting_recipes import tree_recipes

class Ground:
    def __init__(self,map,Tile_map,ground,visible_sprites,interactables):
        self.map = map
        self.Tile_map = Tile_map
        self.ground = ground
        self.visible_sprites = visible_sprites
        self.interactables = interactables
        self.image = pygame.Surface((round(tile_size*reshape_game.x),round(tile_size*reshape_game.y)))
        self.time_left = None
        
    def beach_check(self,biome):
        dont_run = False
        for x in change_tile.values():
            if x == biome:
                dont_run = True
        return dont_run
    
    def ground_logic(self,mouse_offset,ground,perlin):
        biome = perlin[mouse_offset[1]][mouse_offset[0]]
        if ground[mouse_offset[1]][mouse_offset[0]]['ground'] == 'plowed_ground':
            self.restore_ground(mouse_offset,ground,perlin)
        else:
            if biome != 'water':
                if not self.beach_check(biome):
                    ground[mouse_offset[1]][mouse_offset[0]]['ground'] = 'plowed_ground'
                    self.image.blit(pygame.transform.scale(self.Tile_map[2],(self.image.get_width(),self.image.get_height())),(0,0))
                    self.draw(mouse_offset)

    def seeding_logic(self,ground,ui,mouse_offset,seed,time):
        land = ground[mouse_offset[1]][mouse_offset[0]]
        if land['ground'] == 'plowed_ground':
            if land['seeded_ground']: 
                for item in tree_recipes.keys():
                    for recipe in tree_recipes[item]:
                        if land['seed'] !=  seed and not land['mixed']:
                            if land['seed'] in recipe and seed in recipe:
                                self.image.blit(self.Tile_map[2],(0,0))
                                self.ground_changer(ground,mouse_offset,land['seeded_ground'],
                                    item,random.randint(1,4),time,True)
                                ui.remove(ui.inventory_menu[ui.selected_slot[1]][ui.selected_slot[0]],1)
                                self.draw(mouse_offset)
                                break
            else:
                self.ground_changer(ground,mouse_offset,True,seed,random.randint(1,4),time,False)
                ui.remove(ui.inventory_menu[ui.selected_slot[1]][ui.selected_slot[0]],1)
                self.draw(mouse_offset)
                
    def harvest(self,ground,ui,mouse_offset,hoe):
        land = ground[mouse_offset[1]][mouse_offset[0]]
        if land['ground'] == 'plowed_ground' and land['seeded_ground']:
            if land['all_time'] == growth_time:
                self.randomise_tree(land,mouse_offset,hoe)
                self.ground_changer(ground,mouse_offset,False,None,None,None,False)
                self.image.blit(pygame.transform.scale(self.Tile_map[2],(self.image.get_width(),self.image.get_height())),(0,0))
                self.draw(mouse_offset)
                return True
        return False
                
    def show_info(self,ground,mouse_offset,time):
        land = ground[mouse_offset[1]][mouse_offset[0]]
        if land['growth_time'] != None:
            self.time_left = round(growth_time - land['all_time'])
        else:
            self.time_left = None
                
    def ground_changer(self,ground,mouse_offset,seeded_ground,seed,amount,growing_time,mixed):
        ground[mouse_offset[1]][mouse_offset[0]]['seeded_ground'] = seeded_ground
        ground[mouse_offset[1]][mouse_offset[0]]['seed'] = seed
        ground[mouse_offset[1]][mouse_offset[0]]['amount'] = amount
        ground[mouse_offset[1]][mouse_offset[0]]['growth_time'] = growing_time
        ground[mouse_offset[1]][mouse_offset[0]]['mixed'] = mixed
        if growing_time != None:
            ground[mouse_offset[1]][mouse_offset[0]]['end_time'] = growing_time + growth_time
        else:
            ground[mouse_offset[1]][mouse_offset[0]]['all_time'] = None

    def randomise_tree(self,land,mouse_offset,hoe):
        pos = pygame.math.Vector2()
        pos.x = mouse_offset.x*round(reshape_game.x*tile_size)
        pos.y = mouse_offset.y*round(reshape_game.y*tile_size)
        extra_seed = hoe_buff[hoe]['seed'] if random.random() <= 0.33 else 0
        extra_block = hoe_buff[hoe]['block'] if random.random() <= 0.33 else 0
        if random.random() <= 0.5:
            Item(Object((0,0),None,land['seed']),(pos[0]+random.randrange(-32,32),pos[1]+random.randrange(-32,32)),[self.visible_sprites,self.interactables],True,1+extra_seed)
        Item(Object((0,0),None,land['seed']),(pos[0]+random.randrange(-32,32),pos[1]+random.randrange(-32,32)),[self.visible_sprites,self.interactables],False,land['amount']+extra_block)
                
    def check_growth(self,ground,y,x,time):
        if time - ground[y][x]['growth_time'] < growth_time:
            ground[y][x]['all_time'] = time - ground[y][x]['growth_time']
        else:
            ground[y][x]['all_time'] = growth_time

    def update_map(self,land,y,x,time):
        item = land['seed']
        growth_index = land['all_time'] / growth_time
        size = (round(tile_size*reshape_game.x)*growth_index,round(tile_size*reshape_game.y)*growth_index)
        pos = (round((tile_size*reshape_game.x)/2)-size[0],round((tile_size*reshape_game.y)/2)-size[1])
        img = pygame.transform.scale(pygame.image.load(f'../graphics/items/placeables/objects/bush.png'),size)
        item_img = pygame.transform.scale(pygame.image.load(f'../graphics/items/placeables/objects/{item}.png').subsurface(pygame.Rect((0,0),(22*reshape_game.x,22*reshape_game.y))),(22,22))
        self.draw_plant(land,pos,y,x,img,item_img)
        
    def draw_plant(self,land,pos,y,x,img,item_img):
        self.image.blit(self.Tile_map[2],(0,0))
        self.image.blit(img,pos)
        if land['all_time'] == growth_time:
            for i in range(land['amount']):
                self.image.blit(item_img,block_positions[i])
        self.draw(pygame.math.Vector2(x,y))
            
    def draw(self,mouse_offset):
        real_offset = pygame.math.Vector2()
        real_offset.x = mouse_offset.x*round(reshape_game.x*tile_size)
        real_offset.y = mouse_offset.y*round(reshape_game.y*tile_size)
        self.map.blit(self.image,real_offset)
        
    def restore_ground(self,mouse_offset,ground,perlin):
        real_offset = pygame.math.Vector2()
        real_offset.x = mouse_offset.x*round(reshape_game.x*tile_size)
        real_offset.y = mouse_offset.y*round(reshape_game.y*tile_size)
        for name in biomes:
            if perlin[mouse_offset[1]][mouse_offset[0]] == name:
                img = pygame.transform.scale(pygame.image.load(f'../graphics/tiles/{name}.png'),(self.image.get_width(),self.image.get_height()))
                self.map.blit(img,real_offset)
                ground[mouse_offset[1]][mouse_offset[0]]['ground'] = name
        
    def run(self,ground,y,x,time):
        self.check_growth(ground,y,x,time)
        self.update_map(ground[y][x],y,x,time)
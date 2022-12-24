import pygame
#Settings for map
grid_width =34
watermass = 1.5

#biomes for map
plains = 'P'
stone = 'S'
dessert = 'D'
trees = 'T'

screen = pygame.display.set_mode()
WIDTH, HEIGHT = screen.get_size()
FPS = 165
tile_size = 64
default_width = 1280
default_height = 720
reshape_game = pygame.math.Vector2(WIDTH/default_width,HEIGHT/default_height) 
resize = (reshape_game.x+reshape_game.y)/2
#hitbox offset
HITBOX_OFFSET = {
    'player':-26,
    'object':-40,
    'grass':-10,
    'invisible':0
}
#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
#general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

#upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

#Weapons
weapon_data = {
    'black_sword_1' : {'cooldown' : 0.25, 'damage' : 150}
}
weapon_width = {
    'sword':8
}
weapon_height = {
    'sword':16
}

#Magic
magic_data = {
    'flame':{'strength':5,'cost':20,'graphic':'../graphics/particles/flame/fire.png'},
    'heal':{'strength':20,'cost':10,'graphic':'../graphics/particles/heal/heal.png'}}

#Enemies
monster_data = {
    'axolot': {'health': 100,'exp':100,'damage':20,'attack_type': 'Slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 64, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
#Player
player_data = {
    'health' : 100,
    'stamina' : 50,
    'exp' : 50,
    'speed' : 5,
    'resistance' : 1,
    'strength' : 1
}
player_max = {
    'health' : 300,
    'stamina' : 150,
    'speed' : 1.5,
    'resistance' : 3,
    'strength' : 3
}
stats = {
    0 : 'health',
    1 : 'stamina',
    2 : 'speed',
    3 : 'resistance',
    4 : 'strength'
}
dark_color = {
    'health': '#803632',
    'stamina': '#384c80',
    'exp': '#3d8063',
}
animation_index = {
    'Down':0,
    'Up':1,
    'Left':2,
    'Right':3
}
growth_times = {
    'tree':100,
    'rock':100,
    'cactus':100,
    'bush':100,
    'white_flowers':100,
    'yellow_flowers':100,
    'red_flowers':100,
    'blue_flowers':100,
    'sunflower':100,
    'black_crystal':100,
}
growth_time = 10
object_path = '../graphics/objects'
names = {'tree' : ['oak_tree','birch_tree',
              'redwood_tree_1','redwood_tree_2'],
        'rock' : ['rock','small_rock'],
        'cactus' : ['cactus_0','cactus_1']}
water_dir = {
    -1: {-1:'topleft',
         0:'top',
         1:'topright'},
    0: {-1:'left',
         1:'right'},
    1: {-1:'bottomleft',
        0:'bottom',
        1:'bottomright'}}
object_chance = {
    'tree':(0,10),
    'rock':(0,10),
    'cactus':(0,10)
}
tool_offset = {
    True : pygame.math.Vector2(tile_size*reshape_game.x//3,0),
    False : pygame.math.Vector2(0,0)
}
breaking_speed = {
    'black' : 2,
    'white' : 2,
    'blue' : 4,
    'aqua' : 6,
    'pink' : 8,
    'mystical' : 10,
}
biome_objects = {
    'plains':{'tree':0.1,'rock':0.2,'objects':['tree','rock']},
    'forest':{'tree':0.25,'rock':0.1,'objects':['tree','rock']},
    'rainforest':{'tree':0.35,'rock':0.08,'objects':['tree','rock']},
    'savanna':{'tree':0.1,'rock':0.2,'cactus':0.05,'objects':['tree','rock','cactus']},
    'desert':{'rock':0.15,'cactus':0.2,'objects':['rock','cactus']},
}
hoe_buff = {
    'None' : {'seed' : 0, 'block' : 0},
    'black_hoe' : {'seed' : 0, 'block' : 1},
    'white_hoe' : {'seed' : 0, 'block' : 1},
    'aqua_hoe' : {'seed' : 1, 'block' : 0},
    'blue_hoe' : {'seed' : 0, 'block' : 2},
    'pink_hoe' : {'seed' : 1, 'block' : 1},
    'mystical_hoe' : {'seed' : 2, 'block' : 0},
}
#idek i folders tsg visa full path ir viskas
paths = {
    'stick' : '../graphics/items/unplaceables/misc/',
    'aqua_pickaxe' : '../graphics/items/unplaceables/tools/pickaxes',
    'black_pickaxe' : '../graphics/items/unplaceables/tools/pickaxes',
    'blue_pickaxe' : '../graphics/items/unplaceables/tools/pickaxes',
    'mythical_pickaxe' : '../graphics/items/unplaceables/tools/pickaxes',
    'pink_pickaxe' : '../graphics/items/unplaceables/tools/pickaxes',
    'white_pickaxe' : '../graphics/items/unplaceables/tools/pickaxes',
    'aqua_axe' : '../graphics/items/unplaceables/tools/axes',
    'black_axe' : '../graphics/items/unplaceables/tools/axes',
    'blue_axe' : '../graphics/items/unplaceables/tools/axes',
    'mythical_axe' : '../graphics/items/unplaceables/tools/axes',
    'pink_axe' : '../graphics/items/unplaceables/tools/axes',
    'white_axe' :'../graphics/items/unplaceables/tools/axes',
    'aqua_hoe' : '../graphics/items/unplaceables/tools/hoes',
    'black_hoe' : '../graphics/items/unplaceables/tools/hoes',
    'blue_hoe' : '../graphics/items/unplaceables/tools/hoes',
    'mythical_hoe' : '../graphics/items/unplaceables/tools/hoes',
    'pink_hoe' : '../graphics/items/unplaceables/tools/hoes',
    'white_hoe' : '../graphics/items/unplaceables/tools/hoes',
    'aqua_lance_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'black_lance_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'blue_lance_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'white_lance_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'mystical_lance_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'pink_lance_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'aqua_lance_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'black_lance_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'blue_lance_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'white_lance_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'mystical_lance_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'pink_lance_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'aqua_sword_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'black_sword_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'blue_sword_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'white_sword_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'mystical_sword_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'pink_sword_1' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'aqua_sword_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'black_sword_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'blue_sword_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'white_sword_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'mystical_sword_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'pink_sword_2' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'aqua_sword_3' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'black_sword_3' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'blue_sword_3' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'white_sword_3' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'mystical_sword_3' : '../graphics/items/unplaceables/tools/weapons/Sprite',
    'pink_sword_3' : '../graphics/items/unplaceables/tools/weapons/Sprite',
}

block_positions = [(8,8),(32,12),(8,28),(32,32)]
chest_inventory = {0:{0:{'ID':None,'amount':0},1:{'ID':None,'amount':0},2:{'ID':None,'amount':0},
                        3:{'ID':None,'amount':0},4:{'ID':None,'amount':0},5:{'ID':None,'amount':0},
                        6:{'ID':None,'amount':0},7:{'ID':None,'amount':0},8:{'ID':None,'amount':0}},
                    1:{0:{'ID':None,'amount':0},1:{'ID':None,'amount':0},2:{'ID':None,'amount':0},
                        3:{'ID':None,'amount':0},4:{'ID':None,'amount':0},5:{'ID':None,'amount':0},
                        6:{'ID':None,'amount':0},7:{'ID':None,'amount':0},8:{'ID':None,'amount':0}},
                    2:{0:{'ID':None,'amount':0},1:{'ID':None,'amount':0},2:{'ID':None,'amount':0},
                        3:{'ID':None,'amount':0},4:{'ID':None,'amount':0},5:{'ID':None,'amount':0},
                        6:{'ID':None,'amount':0},7:{'ID':None,'amount':0},8:{'ID':None,'amount':0}}}
change_tile = {
    "[['w', '.', '.'], ['w', '_', '.'], ['w', '.', '.']]":'left',
    "[['w', '.', '.'], ['w', '_', '.'], ['.', '.', '.']]":'left',
    "[['.', '.', '.'], ['w', '_', '.'], ['w', '.', '.']]":'left',
    "[['.', '.', '.'], ['w', '_', '.'], ['.', '.', '.']]":'left',
    "[['w', '.', '.'], ['.', '_', '.'], ['w', '.', '.']]":'left',
    
    "[['.', '.', 'w'], ['.', '_', 'w'], ['.', '.', 'w']]":'right',
    "[['.', '.', 'w'], ['.', '_', 'w'], ['.', '.', '.']]":'right',
    "[['.', '.', '.'], ['.', '_', 'w'], ['.', '.', 'w']]":'right',
    "[['.', '.', '.'], ['.', '_', 'w'], ['.', '.', '.']]":'right',
    "[['.', '.', 'w'], ['.', '_', '.'], ['.', '.', 'w']]":'right',
    
    "[['w', 'w', 'w'], ['.', '_', '.'], ['.', '.', '.']]":'top',
    "[['w', 'w', '.'], ['.', '_', '.'], ['.', '.', '.']]":'top',
    "[['.', 'w', 'w'], ['.', '_', '.'], ['.', '.', '.']]":'top',
    "[['.', 'w', '.'], ['.', '_', '.'], ['.', '.', '.']]":'top',
    "[['w', '.', 'w'], ['.', '_', '.'], ['.', '.', '.']]":'top',
    
    "[['.', '.', '.'], ['.', '_', '.'], ['w', 'w', 'w']]":'bottom',
    "[['.', '.', '.'], ['.', '_', '.'], ['w', 'w', '.']]":'bottom',
    "[['.', '.', '.'], ['.', '_', '.'], ['.', 'w', 'w']]":'bottom',
    "[['.', '.', '.'], ['.', '_', '.'], ['.', 'w', '.']]":'bottom',
    "[['.', '.', '.'], ['.', '_', '.'], ['w', '.', 'w']]":'bottom',
    
    "[['w', '.', '.'], ['.', '_', '.'], ['.', '.', '.']]":'topleft',
    "[['.', '.', '.'], ['.', '_', '.'], ['w', '.', '.']]":'bottomleft',
    "[['.', '.', 'w'], ['.', '_', '.'], ['.', '.', '.']]":'topright',
    "[['.', '.', '.'], ['.', '_', '.'], ['.', '.', 'w']]":'bottomright',
    
    "[['w', 'w', '.'], ['w', '_', '.'], ['.', '.', '.']]":'surrounded_topleft',
    "[['w', 'w', '.'], ['w', '_', '.'], ['w', '.', '.']]":'surrounded_topleft',
    "[['w', 'w', 'w'], ['w', '_', '.'], ['.', '.', '.']]":'surrounded_topleft',
    "[['w', 'w', 'w'], ['w', '_', '.'], ['w', '.', '.']]":'surrounded_topleft',
    "[['.', 'w', 'w'], ['w', '_', '.'], ['.', '.', '.']]":'surrounded_topleft',
    "[['.', 'w', 'w'], ['w', '_', '.'], ['w', '.', '.']]":'surrounded_topleft',
    "[['w', 'w', 'w'], ['.', '_', '.'], ['w', '.', '.']]":'surrounded_topleft',
    
    "[['.', '.', '.'], ['w', '_', '.'], ['w', 'w', '.']]":'surrounded_bottomleft',
    "[['w', '.', '.'], ['w', '_', '.'], ['w', 'w', '.']]":'surrounded_bottomleft',
    "[['.', '.', '.'], ['w', '_', '.'], ['w', 'w', 'w']]":'surrounded_bottomleft',
    "[['w', '.', '.'], ['w', '_', '.'], ['w', 'w', 'w']]":'surrounded_bottomleft',
    "[['.', '.', '.'], ['w', '_', '.'], ['.', 'w', 'w']]":'surrounded_bottomleft',
    "[['w', '.', '.'], ['w', '_', '.'], ['.', 'w', 'w']]":'surrounded_bottomleft',
    "[['w', '.', '.'], ['.', '_', '.'], ['w', 'w', 'w']]":'surrounded_bottomleft',
    
    "[['.', 'w', 'w'], ['.', '_', 'w'], ['.', '.', '.']]":'surrounded_topright',
    "[['.', 'w', 'w'], ['.', '_', 'w'], ['.', '.', 'w']]":'surrounded_topright',
    "[['w', 'w', 'w'], ['.', '_', 'w'], ['.', '.', '.']]":'surrounded_topright',
    "[['w', 'w', 'w'], ['.', '_', 'w'], ['.', '.', 'w']]":'surrounded_topright',
    "[['w', 'w', '.'], ['.', '_', 'w'], ['.', '.', '.']]":'surrounded_topright',
    "[['w', 'w', '.'], ['.', '_', 'w'], ['.', '.', 'w']]":'surrounded_topright',
    "[['w', 'w', 'w'], ['.', '_', '.'], ['.', '.', 'w']]":'surrounded_topright',
    
    "[['.', '.', '.'], ['.', '_', 'w'], ['.', 'w', 'w']]":'surrounded_bottomright',
    "[['.', '.', 'w'], ['.', '_', 'w'], ['.', 'w', 'w']]":'surrounded_bottomright',
    "[['.', '.', '.'], ['.', '_', 'w'], ['w', 'w', 'w']]":'surrounded_bottomright',
    "[['.', '.', 'w'], ['.', '_', 'w'], ['w', 'w', 'w']]":'surrounded_bottomright',
    "[['.', '.', '.'], ['.', '_', 'w'], ['w', 'w', '.']]":'surrounded_bottomright',
    "[['.', '.', 'w'], ['.', '_', 'w'], ['w', 'w', '.']]":'surrounded_bottomright',
    "[['.', '.', 'w'], ['.', '_', '.'], ['w', 'w', 'w']]":'surrounded_bottomright'
}

keybinds = {
    'Walk up':'w',
    'Walk left':'a',
    'Walk down':'s',
    'Walk right':'d',
    'Enable/disable inventory':'i',
    'Create farmable land':'p',
    'Basic crafting menu':'e',
    'Drop selected item':'q',
    'Attack':chr(32),
    'Select slot 1':'1',
    'Select slot 2':'2',
    'Select slot 3':'3',
    'Select slot 4':'4',
    'Select slot 5':'5',
    'Select slot 6':'6',
    'Select slot 7':'7',
    'Select slot 8':'8',
    'Select slot 9':'9',
}

list_of_slots = ['Select slot 1','Select slot 2','Select slot 3',
                'Select slot 4','Select slot 5','Select slot 6',
                'Select slot 7','Select slot 8','Select slot 9',]

background_img = pygame.image.load('../graphics/items/unplaceables/other/Background_image.png')
dark = pygame.Surface((background_img.get_width(), background_img.get_height()), flags=pygame.SRCALPHA)
dark.fill((125, 25, 25, 100))
background_img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
#will subtract 50 from the RGB values of the surface called image.
text_limit = 16
legal_letters = 'qwertyuiopasdfghjklzxcvbnm0123456789'
options_button = pygame.image.load(f'../graphics/items/unplaceables/other/options_button.png')
key_button = pygame.image.load(f'../graphics/items/unplaceables/other/key_button.png')
height_offset = {
    'options_button':options_button.get_height()*reshape_game.y,
    'key_button':key_button.get_height()*reshape_game.y,
}
font_offset = 4*reshape_game.x
chunk_size = 5
offset_limit = pygame.math.Vector2(WIDTH//1920,HEIGHT//1080)
biomes = ['forest','rainforest','savanna','desert','plains']
objects = ['rock','tree','cactus']
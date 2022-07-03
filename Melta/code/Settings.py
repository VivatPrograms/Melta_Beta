
#Settings for map
grid_width = 50
watermass = 1.5

#biomes for map
plains = 'P'
stone = 'S'
dessert = 'D'
trees = 'T'

WIDTH = 1280
HEIGHT = 720
FPS = 60
tile_size = 64
#hitbox offset
HITBOX_OFFSET = {
    'player':-26,
    'object':-40,
    'grass':-10,
    'invisible':0
}
#UI
font_offset = 2
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
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}

#Magic
magic_data = {
    'flame':{'strength':5,'cost':20,'graphic':'../graphics/particles/flame/fire.png'},
    'heal':{'strength':20,'cost':10,'graphic':'../graphics/particles/heal/heal.png'}}

#Enemies
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

growth_times = {
    'tree':100,
    'rock':200,
    'cactus':50
}
object_path = '../graphics/objects'
names = {'tree' : ['oak_tree','birch_tree',
              'magical_tree','mystical_tree'],
        'rock' : ['rock','small_rock'],
        'cactus' : ['cactus_0','cactus_1','small_cactus_0','small_cactus_1']}
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
object_offset = {
    'birch_tree':(32,96),
    'oak_tree':(32,96),
    'magical_tree':(32,96),
    'mystical_tree':(32,96),
    'rock':(28,32),
    'small_rock':(28,32),
    'cactus_0':(8,32),
    'cactus_1':(8,32),
    'small_cactus_0':(2,6),
    'small_cactus_1':(2,6)
}

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
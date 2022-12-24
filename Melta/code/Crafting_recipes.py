recipes = {
    0 : {'stone' : ['rock'],
            'stone' : ['small_rock'],
            'oak_wood' : ['oak_tree'],
            'birch_wood' : ['birch_tree'],
            'redwood_wood' : ['redwood_tree_1',
            'redwood_tree_2']},
    1: {'black_sword_1' : [[['black_crystal'],['stick']]],
    'blue_sword_1' : [[['blue_crystal'],['stick']]],
    'white_sword_1' : [[['white_crystal'],['stick']]],
    'pink_sword_1' : [[['pink_crystal'],['stick']]],
    'aqua_sword_1' : [[['aqua_crystal'],['stick']]],
    'mystical_sword_1' : [[['mystical_crystal'],['stick']]],
    'stick' : [[['oak_wood'],['oak_wood']]]},
    2 : {'oak_table' : [[['oak_table_small','oak_table_small']]],
    'birch_table' : [[['birch_table_small','birch_table_small']]],
    'redwood_table' : [[['redwood_table_small','redwood_table_small']]]},
    3 : {'oak_table_small' : [[['oak_wood','oak_wood'],['oak_wood','oak_wood']]],
        'birch_table_small' : [[['birch_wood','birch_wood'],['birch_wood','birch_wood']]],
        'redwood_table_small' : [[['redwood_tree_2','redwood_tree_2'],['redwood_tree_2','redwood_tree_2']],
        [['redwood_tree_1','redwood_tree_1'],['redwood_tree_1','redwood_tree_1']]]},
    4 : {'aqua_lance_1':[[[None,None,'aqua_crystal'],[None,'stick',None],['stick',None,None]]],
    'blue_lance_1':[[[None,None,'blue_crystal'],[None,'stick',None],['stick',None,None]]],
    'black_lance_1':[[[None,None,'black_crystal'],[None,'stick',None],['stick',None,None]]],
    'mystical_lance_1':[[[None,None,'mystical_crystal'],[None,'stick',None],['stick',None,None]]],
    'pink_lance_1':[[[None,None,'pink_crystal'],[None,'stick',None],['stick',None,None]]],
    'white_lance_1':[[[None,None,'white_crystal'],[None,'stick',None],['stick',None,None]]],
    'aqua_pickaxe':[[['aqua_crystal','aqua_crystal','aqua_crystal'],[None,'stick',None],[None,'stick',None]]],
    'blue_pickaxe':[[['blue_crystal','blue_crystal','blue_crystal'],[None,'stick',None],[None,'stick',None]]],
    'black_pickaxe':[[['black_crystal','black_crystal','black_crystal'],[None,'stick',None],[None,'stick',None]]],
    'mystical_pickaxe':[[['mystical_crystal','mystical_crystal','mystical_crystal'],[None,'stick',None],[None,'stick',None]]],
    'pink_pickaxe':[[['pink_crystal','pink_crystal','pink_crystal'],[None,'stick',None],[None,'stick',None]]],
    'white_pickaxe':[[['white_crystal','white_crystal','white_crystal'],[None,'stick',None],[None,'stick',None]]],
    'aqua_axe':[[['aqua_crystal','aqua_crystal',None],['aqua_crystal','stick',None],[None,'stick',None]],
                [[None,'aqua_crystal','aqua_crystal'],[None,'stick','aqua_crystal'],[None,'stick',None]]],
    'black_axe':[[['black_crystal','black_crystal',None],['black_crystal','stick',None],[None,'stick',None]],
                [[None,'black_crystal','black_crystal'],[None,'stick','black_crystal'],[None,'stick',None]]],
    'blue_axe':[[['blue_crystal','blue_crystal',None],['blue_crystal','stick',None],[None,'stick',None]],
                [[None,'blue_crystal','blue_crystal'],[None,'stick','blue_crystal'],[None,'stick',None]]],
    'mystical_axe':[[['mystical_crystal','mystical_crystal',None],['mystical_crystal','stick',None],[None,'stick',None]],
                [[None,'mystical_crystal','mystical_crystal'],[None,'stick','mystical_crystal'],[None,'stick',None]]],
    'pink_axe':[[['pink_crystal','pink_crystal',None],['pink_crystal','stick',None],[None,'stick',None]],
                [[None,'aqua_crystal','aqua_crystal'],[None,'stick','aqua_crystal'],[None,'stick',None]]],
    'white_axe':[[['white_crystal','white_crystal',None],['white_crystal','stick',None],[None,'stick',None]],
                [[None,'white_crystal','white_crystal'],[None,'stick','white_crystal'],[None,'stick',None]]],
    'aqua_hoe':[[['aqua_crystal','aqua_crystal',None],[None,'stick',None],[None,'stick',None]],
                [[None,'aqua_crystal','aqua_crystal'],[None,'stick',None],[None,'stick',None]]],
    'black_hoe':[[['black_crystal','black_crystal',None],[None,'stick',None],[None,'stick',None]],
                [[None,'black_crystal','black_crystal'],[None,'stick',None],[None,'stick',None]]],
    'blue_hoe':[[['blue_crystal','blue_crystal',None],[None,'stick',None],[None,'stick',None]],
                [[None,'blue_crystal','blue_crystal'],[None,'stick',None],[None,'stick',None]]],
    'mystical_hoe':[[['mystical_crystal','mystical_crystal',None],[None,'stick',None],[None,'stick',None]],
                [[None,'mystical_crystal','mystical_crystal'],[None,'stick',None],[None,'stick',None]]],
    'pink_hoe':[[['pink_crystal','pink_crystal',None],[None,'stick',None],[None,'stick',None]],
                [[None,'aqua_crystal','aqua_crystal'],[None,'stick',None],[None,'stick',None]]],
    'white_hoe':[[['white_crystal','white_crystal',None],[None,'stick',None],[None,'stick',None]],
                [[None,'white_crystal','white_crystal'],[None,'stick',None],[None,'stick',None]]],
    'oak_chest':[[['oak_wood','oak_wood','oak_wood'],['oak_wood',None,'oak_wood'],['oak_wood','oak_wood','oak_wood']]],
    'birch_chest':[[['birch_wood','birch_wood','birch_wood'],['birch_wood',None,'birch_wood'],['birch_wood','birch_wood','birch_wood']]],
    'redwood_chest':[[['redwood_wood','redwood_wood','redwood_wood'],['redwood_wood',None,'redwood_wood'],['redwood_wood','redwood_wood','redwood_wood']]],}
}


tree_recipes = {
    'bush' : [['oak_tree','rock'],
              ['birch_tree','rock'],
              ['redwood_tree_1','rock'],
              ['redwood_tree_2','rock'],
              ['oak_tree','rock'],
              ['birch_tree','rock'],
              ['redwood_tree_1','rock'],
              ['redwood_tree_2','rock'],],
    'white_flowers' : [['birch_tree','bush']],
    'yellow_flowers' : [['oak_tree','bush']],                              
    'red_flowers' : [['redwood_tree_1','bush']],
    'blue_flowers' : [['redwood_tree_2','bush']], 
    'sunflower' : [['oak_tree','cactus_1'],
                ['birch_tree','cactus_1'],
                ['redwood_tree_1','cactus_1'],
                ['redwood_tree_2','cactus_1']],
    'black_crystal' : [['rock','white_flowers'],
                       ['rock','yellow_flowers'],
                       ['rock','red_flowers'],
                       ['rock','blue_flowers']],
    'chalkboard' : [['rock','oak_mirror'],
                    ['rock','birch_mirror'],
                    ['rock','redwood_mirror']],
    'drawer' : [['oak_tree','oak_table_small'],
                ['birch_tree','birch_table_small'],
                ['redwood_tree','redwood_table_small']],
    'oak_wardrobe_small' : [['oak_tree','oak_mirror']],
    'birch_wardrobe_small' : [['birch_tree','birch_mirror']],
    'redwood_wardrobe_small' : [['redwood_tree','redwood_mirror']],
    'white_crystal' : [['tree','white_flowers']],
    'oak_mirror' : [['oak_tree','glass']],
    'birch_mirror' : [['birch_tree','glass']],
    'redwood_mirror' : [['redwood_tree','glass']],
    'glass' : [['bush','cactus_0'],
               ['bush','cactus_1']],
    'aqua_crystal' : [['white_crystal','blue_crystal']],
    'oak_bookshelf' : [['oak_table_small','cactus_0'],
                       ['oak_table_small','cactus_1']],
    'birch_bookshelf' : [['birch_table_small','cactus_0'],
                       ['birch_table_small','cactus_1']],
    'redwood_bookshelf' : [['sredwood_table_small','cactus_0'],
                    ['redwood_table_small','cactus_1']],
    'locker' : [['black_crystal','oak_wardrobe_small'],
                ['black_crystal','birch_wardrobe_small'],
                ['black_crystal','redwood_wardrobe_small']],
    'blue_crystal' : [['locker','glass']],
    'tv' : [['locker','oak_mirror'],
            ['locker','birch_mirror'],
            ['locker','redwood_mirror']],
    'green_chalkboard' : [['locker','oak_hanging_mirror'],
                          ['locker','birch_hanging_mirror'],
                          ['locker','redwood_hanging_mirror']],
    'oak_hanging_mirror' : [['oak_mirror','chalkboard']],
    'birch_hanging_mirror' : [['birch_mirror','chalkboard']],
    'redwood_hanging_mirror' : [['redwood_mirror','chalkboard']],
    'oak_wardrobe' : [['oak_wardrobe_small','oak_bookshelf']],
    'birch_wardrobe' : [['birch_wardrobe_small','birch_bookshelf']],
    'redwood_wardrobe' : [['redwood_wardrobe_small','redwood_bookshelf']],
    'pink_crystal' : [['aqua_crystal','sunflower']],

}
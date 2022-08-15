recipes = {
    0 : {'stone' : 'rock',
            'stone' : 'small_rock',
            'oak_wood' : 'oak_tree',
            'birch_wood' : 'birch_tree',
            'redwood_wood' : 'redwood_tree_1',
            'redwood_wood' : 'redwood_tree_2',},
    1: {'stone' : [['oak_wood'],['oak_wood']]},
    2 : {'oak_table' : [['oak_wood','oak_wood'],['oak_wood','oak_wood']],
        'birch_table' : [['birch_wood','birch_wood'],['birch_wood','birch_wood']],
        'redwood_table' : [['redwood_tree_2','redwood_tree_2'],['redwood_tree_2','redwood_tree_2']]},
}

tree_recipes = {
    'bush' : [['oak_tree','rock'],
              ['birch_tree','rock'],
              ['redwood_tree_1','rock'],
              ['redwood_tree_2','rock']],
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
    'drawer' : [['oak_tree','oak_table'],
                ['birch_tree','birch_table'],
                ['redwood_tree','redwood_table']],
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
    'oak_bookshelf' : [['oak_table','cactus_0'],
                       ['oak_table','cactus_1']],
    'birch_bookshelf' : [['birch_table','cactus_0'],
                       ['birch_table','cactus_1']],
    'redwood_bookshelf' : [['redwood_table','cactus_0'],
                    ['redwood_table','cactus_1']],
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

recipes_type_0 = {
    'tree' : 'tree'
}

recipes_type_1 = {
    'rock' : [['tree'],['tree']]
}

recipes_type_2 = {
    'oak_table' : [['oak_wood','oak_wood'],['oak_wood','oak_wood']],
    'birch_table' : [['birch_wood','birch_wood'],['birch_wood','birch_wood']],
    'redwood_table' : [['redwood_wood','redwood_wood'],['redwood_wood','redwood_wood']]
}
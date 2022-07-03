recipes = {
    'rock' : {
        'type':1,
        'recipe':[['rock'],['rock']]
    },
    'tree' : {
        'type':0,
        'recipe':'tree'
    }  
    
}

tree_recipes = {
    'tree' : {'rock':'rock'},
    'rock' : {'tree':'tree'}
}

recipes_type_0 = {
    'tree' : 'tree'
}

recipes_type_1 = {
    'rock' : [['tree'],['tree']]
}
from Settings import *
from Import_support import *
from Entity import Entity
from time import perf_counter

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,border):
        super().__init__(groups,pos,border)
        #general setup
        self.name = 'player'
        self.type = 'entity'
        self.player_name = 'Noble'
        self.weapon = None
        #sprite setup
        self.image = pygame.Surface((tile_size*reshape_game.x,tile_size*reshape_game.y))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-16*reshape_game.x,-24*reshape_game.y)
        #Functions
        self.obstacle_sprites = obstacle_sprites
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        #graphics setup
        self.import_player_assets()
        self.status = 'Down_Idle'
        # movement
        self.attacking = False
        self.attacking_time = None
        self.attack_cooldown = None
        self.attack_time = None
        self.facing_offset = pygame.math.Vector2()
        #vulnerable
        self.vulnerable = False
        self.vulnerable_time = None
        self.vulnerable_cooldown = None
        #import sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.1)

    def import_player_assets(self):
        character_path = f'../graphics/entities/characters/{self.player_name}/animations'
        self.animations = {'Down':{'Attack':[],'Idle':[],'Walk':[]},
                            'Up':{'Attack':[],'Idle':[],'Walk':[]},
                            'Left':{'Attack':[],'Idle':[],'Walk':[]},
                            'Right':{'Attack':[],'Idle':[],'Walk':[]}}
        for direction in self.animations.keys():
            for animation in self.animations[direction].keys():
                full_path = character_path +'/'+ animation+'.png'
                images = import_sprite_sheet(full_path,(16,16))
                index = animation_index[direction]
                if animation == 'Walk':
                    for i in range(4):
                        self.animations[direction][animation].append(pygame.transform.scale(images[index+i*4],(tile_size*reshape_game.x,tile_size*reshape_game.y)))
                else:
                    self.animations[direction][animation].append(pygame.transform.scale(images[index],(tile_size*reshape_game.x,tile_size*reshape_game.y)))

    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if '_Walk' in self.status:
                self.status = self.status.replace('_Walk','')   
                if not 'Idle' in self.status and not 'Attack' in self.status:
                    self.status = self.status + '_Idle'
        #attacking status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'Attack' in self.status:
                if 'Idle' in self.status:
                    self.status = self.status.replace('_Idle','_Attack')
                else:
                    self.status = self.status + '_Attack'
        else:
            if 'Attack' in self.status:
                self.status = self.status.replace('_Attack','_Idle')

    def get_facing_offset(self):
        if self.status == 'Up_Walk':
            self.facing_offset.x = 0
            self.facing_offset.y = -tile_size*reshape_game.y
        elif self.status == 'Down_Walk':
            self.facing_offset.x = 0
            self.facing_offset.y = tile_size*reshape_game.y
        elif self.status == 'Left_Walk':
            self.facing_offset.x = -tile_size*reshape_game.x
            self.facing_offset.y = 0
        elif self.status == 'Right_Walk':
            self.facing_offset.x = tile_size*reshape_game.x
            self.facing_offset.y = 0

    def cooldowns(self,time):
        if self.vulnerable:
            self.attacking = False
            if time - self.vulnerable_time >= weapon_data[self.weapon]['cooldown']:
                self.vulnerable = False
        if self.attacking:
            if time - self.attack_time >= weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.vulnerable = True
                self.vulnerable_time = perf_counter()
                self.destroy_attack()

    def get_full_weapon_damage(self):
        base_dmg = player_data['strength']
        weapon_dmg = weapon_data[self.weapon]['damage']
        return base_dmg + weapon_dmg

    def animate(self,dt):
        animation = self.animations[self.status.split('_')[0]][self.status.split('_')[1]]
        #loop over frame index
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]
    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self,time,dt):
        self.cooldowns(time)
        self.get_status()
        self.get_facing_offset()
        self.animate(dt)
        self.move(player_data['speed']*150,dt)

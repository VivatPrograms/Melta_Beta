import pygame
from time import perf_counter
from Settings import *
from Entity import Entity
from Import_support import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):
        #general setup
        super().__init__(groups,pos)
        self.name = 'enemy'
        self.type = 'entity'
        #graphics setup
        self.import_enemy_assets(monster_name)
        self.status = 'Down_Idle'
        self.image = self.animations[self.status.split('_')[0]][self.status.split('_')[1]][0]
        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        #player interaction
        self.attacking = False
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 0.75
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 0.5
        #sounds
        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.1)
        self.hit_sound.set_volume(0.1)
        self.attack_sound.set_volume(0.1)

    def import_enemy_assets(self,name):
        character_path = f'../graphics/enemies/{name}'
        self.animations = {'Down':{'Idle':[],'Walk':[]},
                            'Up':{'Idle':[],'Walk':[]},
                            'Left':{'Idle':[],'Walk':[]},
                            'Right':{'Idle':[],'Walk':[]}}
        for direction in self.animations.keys():
            for animation in self.animations[direction].keys():
                full_path = character_path +'/SpriteSheet.png'
                images = import_sprite_sheet(full_path,(16,16))
                index = animation_index[direction]
                if animation == 'Walk':
                    for i in range(4):
                        self.animations[direction][animation].append(pygame.transform.scale(images[index+i*4],(64,64)))
                else:
                    self.animations[direction][animation].append(pygame.transform.scale(images[index],(64,64)))

    def get_player_distance_direction(self,player):
        enemy_vector=pygame.math.Vector2(self.rect.center)
        player_vector=pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self,player):
        self.attacking = False
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius:
            self.attacking = True
        elif distance <= self.notice_radius:
            if 'Idle' in self.status:
                if not 'Walk' in self.status:
                    self.status = self.status.replace('_Idle','_Walk')
        else:
            if not '_Idle' in self.status:
                if 'Walk' in self.status:
                    self.status = self.status.replace('_Walk','')
                self.status = self.status + '_Idle'

    def actions(self,player):
        if self.attacking and self.can_attack:
            player_pos = pygame.math.Vector2(player.rect.topleft)
            enemy_pos = pygame.math.Vector2(self.rect.topleft)
            diff = enemy_pos - player_pos
            pos = player_pos + diff / 2
            self.attack_sound.play()
            self.attack_time = perf_counter()
            self.damage_player(self.attack_damage,self.attack_type,pos,self.disable_attack)
        elif 'Walk' in self.status:
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def disable_attack(self):
        self.can_attack = False

    def animate(self,dt):
        animation = self.animations[self.status.split('_')[0]][self.status.split('_')[1]]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            if self.attacking:
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value(dt)
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self,time):
        if not self.can_attack:
            if time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        self.hit_sound.play()
        self.direction = self.get_player_distance_direction(player)[1]
        self.health -= player.get_full_weapon_damage()
        self.hit_time = perf_counter()
        self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.topleft, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def hit_reaction(self,dt):
        if not self.vulnerable:
            self.direction *= - self.resistance
            self.knockback(self.speed*3,dt)

    def update(self,time,dt):
        self.move(self.speed*1.5,dt,True if 'Walk' in self.status else False,self.attacking)
        self.cooldowns(time)
        self.hit_reaction(dt)
        self.animate(dt)
        self.check_death()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)

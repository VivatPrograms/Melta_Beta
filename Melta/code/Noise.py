from perlin import Perlin
import random
from random import randint as r
from Settings import *
# random.seed(1648)
class PerlinNoise:
    def __init__(self):
        self.noise = Perlin(r(0,1000))
        self.container = {'water':[],'forest':[],'rainforest':[],'plains':[],'savanna':[],'desert':[],'tree':[],'rock':[],'cactus':[],
                          'enemy':[],
                          'topleft':[],'top':[],'topright':[],'left':[],'right':[],'bottomleft':[],'bottom':[],'bottomright':[],
                          'surrounded_topleft':[],'surrounded_topright':[],'surrounded_bottomleft':[],'surrounded_bottomright':[]}
        self.biomes = {}
    def generate_noise(self):
        high = 0
        low = 0
        self.temp_grid = []
        for y in range(grid_width):
            self.temp_grid.append([])
            for x in range(grid_width):
                ht = self.noise.two(x, y)
                if ht > high:
                    high = ht
                if ht < low:
                    low = ht
                noise=self.clamp(self.noise.two(x, y), low, high, -10, 50)
                self.temp_grid[y].append(noise)

        self.hum_grid = []
        for y in range(grid_width):
            self.hum_grid.append([])
            for x in range(grid_width):
                ht = self.noise.two(x, y)
                if ht > high:
                    high = ht
                if ht < low:
                    low = ht
                noise=self.clamp(self.noise.two(x, y), low, high, -10, 50)
                self.hum_grid[y].append(noise)

        self.generate_map()

    def clamp(self,oldValue , oldMin, oldMax, newMin, newMax):
        try:
            oldRange = (oldMax - oldMin)
            newRange = (newMax - newMin)
            newValue = (((oldValue - oldMin) * newRange) // oldRange) + newMin
            return newValue
        except:
            return 0

    def generate_map(self):
        grid = []
        for y in range(grid_width):
            grid.append([])
            for x in range(grid_width):
                grid[y].append(self.biome_output(self.temp_grid[y][x], self.hum_grid[y][x]))

        for row_index,row in enumerate(grid):
            self.biomes[row_index] = {}
            for col_index,value in enumerate(row):
                coord = (round(tile_size*reshape_game.x)*col_index,round(tile_size*reshape_game.y)*row_index)
                self.biomes[row_index][col_index] = value
                self.container[value].append(coord)
                self.randomise_object(value,coord)
                        
    def randomise_object(self,biome,coord):
        object = random.choice(biome_objects[biome]['objects'])
        if biome_objects[biome][object] > random.random():
            self.container[object].append(coord)

    def biome_output(self,temp,rainfall):
        if temp <=3 and rainfall <= 3:
            return 'forest'
        elif 10<temp <=15 and 10<rainfall <= 15:
            return 'forest'
        elif 15<temp <=25 and 15<rainfall <= 25:
            return 'rainforest'
        elif 20<temp<=40 and 20<rainfall <= 40:
            return 'savanna'
        elif 30<temp and 30<rainfall:
            return 'desert'
        else:
            return 'plains'
        
    def nearby_water(self, matrix, row_index, col_index):
        code = [['.','.','.'],['.','_','.'],['.','.','.']]
        for i in range(-1,2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0) and not row_index + i < 0 and not col_index + j < 0:
                    try:
                        if matrix[row_index + i][col_index + j] == "water":
                            code[i+1][j+1] = 'w'
                    except IndexError:
                        pass
        for lst in code:
            if 'w' in lst:
                if str(code) in change_tile:
                    return change_tile[str(code)]
                else:
                    return 'water'
        return False
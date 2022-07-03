from perlin import Perlin
import random
from random import randint as r
from Settings import *
random.seed(1648)
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
                coord = tile_size*col_index,tile_size*row_index
                if value == 'water':
                    self.biomes[row_index][col_index] = value
                    self.container[value].append(coord)
                    self.randomise_object('rock',coord)
                elif value == 'desert':
                    self.biomes[row_index][col_index] = value
                    self.container[value].append(coord)
                    self.randomise_object('cactus',coord)
                else:
                    if not self.nearby_water(grid, row_index, col_index):
                        self.biomes[row_index][col_index] = value
                        self.container[value].append(coord)
                        self.randomise_object('tree',coord)
                    else:
                        self.biomes[row_index][col_index] = self.nearby_water(grid, row_index, col_index)
                        self.container[self.nearby_water(grid, row_index, col_index)].append(coord)
                        
    def randomise_object(self,object,coord):
        chance = object_chance[object]
        if r(chance[0],chance[1]) == 1:
            self.container[object].append(coord)
        
    def biome_output(self,temp,rainfall):
        if temp <= 10 and rainfall <= 10:
            return 'water'
        elif 12<temp <=20 and 12<rainfall <= 20:
            return 'forest'
        elif 16<temp <=30 and 16<rainfall <= 30:
            return 'rainforest'
        elif 22<temp<=40 and 22<rainfall <= 40:
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
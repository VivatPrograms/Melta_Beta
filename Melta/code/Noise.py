from perlin import Perlin
import random
from random import randint as r
from Settings import *
random.seed(1)
class PerlinNoise:
    def __init__(self):
        self.noise = Perlin(r(0,1000))
        self.container = {'water':[],'forest':[],'rainforest':[],'plains':[],'savanna':[],'desert':[],'tree':[],'rock':[],'enemy':[]}
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
                    self.biomes[row_index][col_index] = 'water'
                    self.container['water'].append(coord)
                    if r(0, 10) == 1:
                        self.container['rock'].append(coord)
                    elif r(0, 50) == 1:
                        self.container['enemy'].append(coord)
                elif value == 'forest':
                    self.biomes[row_index][col_index] = 'forest'
                    self.container['forest'].append(coord)
                    if r(0, 10) == 1:
                        self.container['tree'].append(coord)
                    elif r(0, 50) == 1:
                        self.container['enemy'].append(coord)
                elif value == 'rainforest':
                    self.biomes[row_index][col_index] = 'rainforest'
                    self.container['rainforest'].append(coord)
                    if r(0, 10) == 1:
                        self.container['tree'].append(coord)
                    elif r(0, 50) == 1:
                        self.container['enemy'].append(coord)
                elif value == 'plains':
                    self.biomes[row_index][col_index] = 'plains'
                    self.container['plains'].append(coord)
                    if r(0, 10) == 1:
                        self.container['tree'].append(coord)
                    elif r(0, 50) == 1:
                        self.container['enemy'].append(coord)
                elif value == 'savanna':
                    self.biomes[row_index][col_index] = 'savanna'
                    self.container['savanna'].append(coord)
                    if r(0, 10) == 1:
                        self.container['tree'].append(coord)
                    elif r(0, 50) == 1:
                        self.container['enemy'].append(coord)
                elif value == 'desert':
                    self.biomes[row_index][col_index] = 'desert'
                    self.container['desert'].append(coord)
                    if r(0, 10) == 1:
                        self.container['tree'].append(coord)
                    elif r(0, 50) == 1:
                        self.container['enemy'].append(coord)
    def biome_output(self,temp,rainfall):
        if temp <= 10 and rainfall <= 10:
            return 'water'
        elif 0<temp <=15 and 0<rainfall <= 15:
            return 'rainforest'
        elif 15<temp <=30 and 15<rainfall <= 30:
            return 'forest'
        elif 30<temp<=45 and 30<rainfall <= 45:
            return 'savanna'
        elif 45<temp<=100 and 45<rainfall <= 100:
            return 'desert'
        elif 45<temp<=50 and 0<rainfall <= 100:
            return 'desert'
        else:
            return 'plains'
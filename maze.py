import pygame
from constants import TILE_SIZE, OFFSET_Y, GREEN

class Maze:
    def __init__(self, file_path, tile_images):
        self.levels = []
        self.grid = []
        self.current_level_index = 0
        self.tile_images = tile_images  # Store the tile images
        self.load_all_levels(file_path)
        self.load_level(0)

    def load_all_levels(self, file_path):
        with open(file_path, 'r') as file:
            level = []
            for line in file:
                line = line.strip()
                if not line or line.startswith("---"):
                    if level:
                        self.levels.append(level)
                        level = []
                else:
                    level.append([int(cell) for cell in line.split()])
            if level:
                self.levels.append(level)

    def load_level(self, index):
        self.current_level_index = index
        self.grid = self.levels[index]

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:  # Wall
                    screen.blit(self.tile_images[0], (x * TILE_SIZE, y * TILE_SIZE + OFFSET_Y))
                elif cell == 2:  # Goal
                    pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE + OFFSET_Y, TILE_SIZE, TILE_SIZE))

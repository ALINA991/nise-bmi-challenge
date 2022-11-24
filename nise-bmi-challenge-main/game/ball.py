# %%
import os
import pygame as pg
from settings import SQUARE_SIZE, OFFSET_X, OFFSET_Y, MATERIALS_DIR


class Ball():

    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.radius = SQUARE_SIZE - self.PADDING

        self.surf = pg.image.load(os.path.join(MATERIALS_DIR, 'ball.png')).convert_alpha()
        self.surf = pg.transform.scale(self.surf, (self.radius, self.radius))

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = OFFSET_X + SQUARE_SIZE * self.col + SQUARE_SIZE / 2
        self.y = OFFSET_Y + SQUARE_SIZE * self.row + SQUARE_SIZE / 2
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def draw(self, window):
        window.blit(self.surf, self.rect)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    
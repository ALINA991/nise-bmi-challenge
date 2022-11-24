# %%
import pygame as pg
from settings import SQUARE_SIZE, BLACK, OFFSET_X, OFFSET_Y


class Player():

    PADDING = 10
    OUTLINE = 3

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        self.x = 0
        self.y = 0
        self.calc_pos()

        self.edge_len = SQUARE_SIZE // 2 - self.PADDING

    def calc_pos(self):
        self.x = OFFSET_X + SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = OFFSET_Y + SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, window):
        pg.draw.polygon(window, BLACK,
                        ((self.x - self.edge_len - self.OUTLINE, self.y + self.edge_len + self.OUTLINE - 1),
                         (self.x + self.edge_len + self.OUTLINE, self.y + self.edge_len + self.OUTLINE - 1),
                         (self.x, self.y - self.edge_len - self.OUTLINE)))
        pg.draw.polygon(window, self.color,
                        ((self.x - self.edge_len, self.y + self.edge_len),
                         (self.x + self.edge_len, self.y + self.edge_len),
                         (self.x, self.y - self.edge_len)))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

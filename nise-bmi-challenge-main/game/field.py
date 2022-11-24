# %%
import os
import pygame as pg
from settings import BG_GREEN, LIGHT_GREEN, DARK_GREEN, BLUE, RED, ROWS, COLS, SQUARE_SIZE, OFFSET_X, OFFSET_Y, MATERIALS_DIR
from ball import Ball
from player import Player
from numpy.random import randint
from shared_memory_dict import SharedMemoryDict



# %%
class Field():

    def __init__(self):
        self.field = []
        self.turn = 0
        self.ball = None
        self.player = None
        self.smd = SharedMemoryDict(name='msg', size=1024)
        self.smd["ball_x"] = None
        self.smd["ball_y"] = None
        self.smd["player_x"] = None
        self.smd["player_y"] = None
        self.smd["emg_trigger"] = None
        self.smd["move_direction"] = 0
        self.smd["pull_ball"] = False



        self.initialize_field()

    def draw_squares(self, window):
        window.fill(BG_GREEN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pg.draw.rect(window, DARK_GREEN,
                             (OFFSET_X + col * SQUARE_SIZE, OFFSET_Y + row * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))
            for col in range(row % 2 - 1, COLS, 2):
                if col >= 0:
                    pg.draw.rect(window, LIGHT_GREEN,
                                (OFFSET_X + col * SQUARE_SIZE, OFFSET_Y + row * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE))

    def reset_ball_and_player(self):
        self.field[self.ball.row][self.ball.col] = 0
        ball_row  = ROWS-2
        ball_col = randint(COLS)
        self.ball = Ball(ball_row, ball_col) # create new ball

        self.player.row = 0
        self.player.col= randint(COLS)
        
        self.field[self.ball.row][self.ball.col] = self.ball
        self.field[self.player.row][self.player.col] = self.player

        self.smd['ball_x'] = self.ball.col
        self.smd['ball_y'] = self.ball.row
        self.smd['player_x'] = self.player.col
        self.smd['player_y'] = self.player.row

    def draw_goal(self, window):
        center_x = OFFSET_X + (COLS / 2) * SQUARE_SIZE

        goal_surf = pg.image.load(os.path.join(MATERIALS_DIR, 'goal_box.png')).convert_alpha()
        goal_surf = pg.transform.scale(goal_surf, (2*SQUARE_SIZE, 1.5*SQUARE_SIZE))
        goal_rect = goal_surf.get_rect(midbottom=(center_x, OFFSET_Y+20))
        window.blit(goal_surf, goal_rect)

    def initialize_field(self):
        ball_row = ROWS - 2
        ball_col = randint(COLS)

        player_row = 0
        player_col = randint(COLS)

        for row in range(ROWS):
            self.field.append([])
            for _ in range(COLS):                
                self.field[row].append(0)

        self.ball = Ball(ball_row, ball_col)
        self.player = Player(player_row, player_col, BLUE)

        self.field[ball_row][ball_col] = self.ball
        self.field[player_row][player_col] = self.player

        self.smd['ball_x'] = self.ball.col
        self.smd['ball_y'] = self.ball.row
        self.smd['player_x'] = self.player.col
        self.smd['player_y'] = self.player.row

    def get_piece(self, row, col):
        return self.field[row][col]

    def get_player(self):
        return self.player

    def get_ball(self):
        return self.ball

    def draw(self, window):
        self.draw_squares(window)
        self.draw_goal(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.field[row][col]
                if piece != 0:
                    piece.draw(window)

    def move(self, piece, row, col):
        tmp_1 = self.field[row][col]
        tmp_2 = self.field[piece.row][piece.col]

        self.field[piece.row][piece.col] = tmp_1
        self.field[row][col] = tmp_2

        piece.move(row, col)

    def is_at_the_edge(self, piece):
        if (piece.row in [0, ROWS-1]) or (piece.col in [0, COLS-1]):
            if (piece.row == 0) and (piece.col in [COLS/2 - 1, COLS/2]):
                return False
            return True
    
        return False

    def get_valid_moves(self, player):
        moves = set()
    
        ball_adjacent = False

        row = player.row
        col = player.col

        left = col - 1
        right = col + 1
        up = row - 1
        down = row + 1

        if left >= 0:
            moves.add((row, left))
            if up >= 0:
                moves.add((up, left))
            if down < ROWS:
                moves.add((down, left))

        if right < COLS:
            moves.add((row, right))
            if up >= 0:
                moves.add((up, right))
            if down < ROWS:
                moves.add((down, right))

        if up >= 0:
            moves.add((up, col))

        if down < ROWS:
            moves.add((down, col))

        tmp_copy = moves.copy()

        for move in tmp_copy:
            row, col = move
            if self.get_piece(row, col) != 0:
                moves.remove(move)
                ball_adjacent = True

        return moves, ball_adjacent


# %%
import pygame as pg
from settings import WHITE, SQUARE_SIZE, ROWS, COLS, FIELD_WIDTH, OFFSET_X, OFFSET_Y
from field import Field
from player import Player
from ball import Ball
from shared_memory_dict import SharedMemoryDict



# %%
class Game():

    def __init__(self, window):
        self.window = window
        self.field = Field()
        self.selected = None
        self.ball_adjacent = None
        self.valid_moves = set()
        self.pull = False
        self.score = 0
        self.font = pg.font.Font(pg.font.get_default_font(), 30)


    def reset(self):
        self.field = Field()
        self.selected = None
        self.valid_moves = set()
        self.pull = False
        self.field.initialize_field()

    def update(self):
        self.field.draw(self.window)
        self.show_score(self.window)
        self.show_pull(self.window)
        pg.display.update()

    def select(self, row, col):
        # If a piece is already selected
        if self.selected:
            # Try moving the piece to the target box
            result = self._move(row, col)
            # If the piece cannot be moved
            if not result:
                # Check if the target box has a ball in it
                if isinstance(self.field.get_piece(row, col),
                              Ball) and self.ball_adjacent:
                    # If the ball is to be shot
                    if not self.pull:
                        self._shoot(row, col)
                    # If the ball is to be pulled
                    else:
                        self._pull(row, col)
                # If the target box is empty
                else:
                    # Reset selection
                    self.selected = None
                    self.select(row, col)
                    self.valid_moves = set()

        # If a piece is not selected
        else:
            # Get the piece on the target box
            piece = self.field.get_piece(row, col)

            # If the selected piece is a player
            if isinstance(piece, Player):
                # Select the player
                self.selected = piece
                # Get valid moves for the player
                self.valid_moves, self.ball_adjacent = self.field.get_valid_moves(
                    piece)
                return True

        return False

    def _move(self, row, col):
        # Get the piece on the target box
        piece = self.field.get_piece(row, col)

        # If a player is selected AND
        # If the target box is empty AND
        # If the target box is in valid moves
        if (self.selected) and (piece == 0) and ((row, col)
                                                 in self.valid_moves):
            # Move the selected piece to the target box
            self.field.move(self.selected, row, col)
            # Reset selection
            self.selected = None
            self.valid_moves = set()
        else:
            return False

        return True

    def _shoot(self, row, col, step=2):
        # Get the piece on the target box
        piece = self.field.get_piece(row, col)

        # If the player is selected AND
        # If the target box has a ball in it
        if (self.selected) and (isinstance(piece, Ball)):

            # Calculate the vector from the ball to the player
            new_row = step * (piece.row - self.selected.row)
            new_col = step * (piece.col - self.selected.col)

            # If the vector is diagonal AND
            # If the ball is at the edge
            if (new_row != 0) and (new_col !=
                                   0) and (self.field.is_at_the_edge(piece)):
                pass
            else:
                # Calculate the new position for the ball
                new_row += piece.row
                new_col += piece.col

                print(new_row, new_col)

                if (new_row in [-1, -2]) and (new_col in [COLS/2 - 1, COLS/2 + 1]):
                    pass

                else:
                    # Enforce field limits on the new position
                    new_row = max(0, new_row)
                    new_row = min(new_row, COLS - 1)
                    new_col = max(0, new_col)
                    new_col = min(new_col, ROWS - 1)

                # Move the ball to the target box
                self.field.move(piece, new_row, new_col)

            # Reset selection
            self.selected = None
            self.valid_moves = set()

    def _pull(self, row, col, step=2):
        # Get the piece on the target box
        piece = self.field.get_piece(row, col)

        # If the player is selected AND
        # If the target box has a ball in it
        if (self.selected) and (isinstance(piece, Ball)):

            # Calculate the vector from the ball to the player
            new_row = -step * (piece.row - self.selected.row)
            new_col = -step * (piece.col - self.selected.col)

            # Calculate the new position for the ball
            new_row += piece.row
            new_col += piece.col

            # Enforce field limits on the new position
            new_row = max(0, new_row)
            new_row = min(new_row, COLS - 1)
            new_col = max(0, new_col)
            new_col = min(new_col, ROWS - 1)

            # Move the ball to the target box
            self.field.move(piece, new_row, new_col)

            # Reset selection
            self.selected = None
            self.valid_moves = set()

    def move_player(self, key):
        player = self.field.player
        ball = self.field.ball

        row = player.row
        col = player.col

        # move player with IMU input

        # move player up
        if self.field.smd['move_direction'] == 1:
            self.field.move(player, max(0, row - 1), col)
            self.field.smd['move_direction'] = 0
         # move player down
        if self.field.smd['move_direction'] == 2:
            self.field.move(player, min(row + 1, ROWS - 1), col)
            self.field.smd['move_direction'] = 0
         # move player left
        if self.field.smd['move_direction'] == 3:
            self.field.move(player, row, max(0, col - 1))
            self.field.smd['move_direction'] = 0
        # move player right
        if self.field.smd['move_direction'] == 4:
            self.field.move(player, row, min(col + 1, COLS - 1))
            self.field.smd['move_direction'] = 0

        # Move the player according to key input
        if key == pg.K_w:
            self.field.move(player, max(0, row - 1), col)
        if key == pg.K_s:
            self.field.move(player, min(row + 1, ROWS - 1), col)
        if key == pg.K_a:
            self.field.move(player, row, max(0, col - 1))
        if key == pg.K_d:
            self.field.move(player, row, min(col + 1, COLS - 1))

        # If the player moves on top of the ball
        if (player.row == ball.row) and (player.col == ball.col):
            # Move the player back to its original place
            self.field.move(player, row, col)

    def shoot_ball(self, step=2):
        player = self.field.player
        ball = self.field.ball

        self.valid_moves, self.ball_adjacent = self.field.get_valid_moves(
            player)

        if self.ball_adjacent:
            # Calculate the vector from the ball to the player
            new_row = step * (ball.row - player.row)
            new_col = step * (ball.col - player.col)

            # If the vector is diagonal AND
            # If the ball is at the edge
            if (new_row != 0) and (new_col !=
                                   0) and (self.field.is_at_the_edge(ball)):
                pass
            else:
                # Calculate the new position for the ball
                new_row += ball.row
                new_col += ball.col

                if new_row == -2 and (new_col in [COLS/2-2, COLS/2-1, COLS/2, COLS/2+1]):
                    if new_col < COLS/2-1:
                        new_col = int(COLS/2-1)
                    if new_col > COLS/2:
                        new_col = int(COLS/2)
                    new_row = -1

                    self.register_goal()

                elif new_row == -1 and (new_col in [COLS/2-1, COLS/2]):
                    self.register_goal()

                else:
                    # Enforce field limits on the new position
                    new_row = max(0, new_row)
                    new_row = min(new_row, COLS - 1)
                    new_col = max(0, new_col)
                    new_col = min(new_col, ROWS - 1)

                # Move the ball to the target box
                self.field.move(ball, new_row, new_col)
                # self.reset()

    def pull_ball(self, step=2):
        player = self.field.player
        ball = self.field.ball

        self.valid_moves, self.ball_adjacent = self.field.get_valid_moves(
            player)

        if self.ball_adjacent:
            # Calculate the vector from the ball to the player
            new_row = -step * (ball.row - player.row)
            new_col = -step * (ball.col - player.col)

            # Calculate the new position for the ball
            new_row += ball.row
            new_col += ball.col

            if (new_row in [-1, -2]) and (new_col in [COLS/2-1, COLS/2]):
                new_row = -1
                self.register_goal()

            else:
                # Enforce field limits on the new position
                new_row = max(0, new_row)
                new_row = min(new_row, COLS - 1)
                new_col = max(0, new_col)
                new_col = min(new_col, ROWS - 1)

            # Move the ball to the target box
            self.field.move(ball, new_row, new_col)

    def switch_action(self):
        self.pull = not self.pull
        self.field.smd["pull_ball"] = self.pull

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pg.draw.circle(self.window, WHITE,
                           (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
    
    def show_score(self, window):
        msg_score = self.font.render(f'Score: {self.score}', False, WHITE)
        x = FIELD_WIDTH + OFFSET_X
        y = OFFSET_Y - SQUARE_SIZE / 2
        msg_score_rect = msg_score.get_rect(midright=(x, y))
        window.blit(msg_score, msg_score_rect)

    def show_pull(self, window):
        msg_pull = self.font.render(f'Pull: {self.pull}', False, WHITE)
        x = FIELD_WIDTH + OFFSET_X
        y = OFFSET_Y - SQUARE_SIZE
        msg_pull_rect = msg_pull.get_rect(midright=(x, y))
        window.blit(msg_pull, msg_pull_rect)

    def register_goal(self):
        self.score += 1
        self.field.reset_ball_and_player()
        # self.reset()

# %%

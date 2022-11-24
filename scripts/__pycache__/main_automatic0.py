

import pygame as pg
from game.settings import WINDOW_WIDTH, WINDOW_HEIGHT, GREY, SQUARE_SIZE, OFFSET_X, OFFSET_Y
from game import Game
from shared_memory_dict import SharedMemoryDict
# %%
FRAME_RATE = 60

# smd = SharedMemoryDict(name='msg', size=1024)

pg.init()

# Create the window
game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_window.fill(GREY)

# Set the window caption
pg.display.set_caption('Football Game')


def get_row_col_from_mouse(pos):
    x, y = pos
    x -= OFFSET_X
    y -= OFFSET_Y
    row = int(y // SQUARE_SIZE)
    col = int(x // SQUARE_SIZE)
    return row, col

def main():

    window_open = True
    clock = pg.time.Clock()
    game = Game(game_window)

    while window_open:
        clock.tick(FRAME_RATE)

        detection = game.field.smd['emg_trigger']
        game.pull = game.field.smd['pull_ball']
        #print(detection)
        if detection:
            if game.pull:
                game.pull_ball()
            else:
                game.shoot_ball()

        game.field.smd['ball_x'] = game.field.ball.col
        game.field.smd['ball_y'] = game.field.ball.row

        # move with IMU input
        if game.field.smd['move_direction'] is not 0:
            game.move_player(game.field.smd['move_direction'])



        game.field.smd['player_x'] = game.field.player.col
        game.field.smd['player_y'] = game.field.player.row

        game.update()

    pg.quit()


def play(pos_player, pos_ball, pos_goal): # define main function ? 

    if pos_ball[0] <= pos_goal[0]: direction = 1 # includes middle line
    else: direction = -1

    if pos_player[1] == pos_ball[1]: # check that first to eliminate problems with border cases later
        scenario3(pos_player, pos_ball, pos_goal, direction)
                    # step = direction assures this is a valid interval when pos_player > pos_goal
    elif pos_ball[1] in range(pos_player[1] ,pos_goal[1], step=direction ): # if ball beween player and goal
        scenario1(pos_player, pos_ball, pos_goal, direction)                # only if first case not satisfied so no 
                                                                            # problem if == pos player
    elif pos_player[1] in range(pos_ball[1], pos_goal[1], step = direction) or pos_goal[1] in range(pos_ball[1], pos_player[1], step = direction):
        scenario2(pos_player, pos_ball, pos_goal, direction )
    return
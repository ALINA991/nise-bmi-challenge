# %%
import pygame as pg
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, GREY, SQUARE_SIZE, OFFSET_X, OFFSET_Y
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


# %%
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
                game.field.smd['emg_trigger'] = 0
            else:
                game.shoot_ball()
                game.field.smd['emg_trigger'] = 0

        game.field.smd['ball_x'] = game.field.ball.col
        game.field.smd['ball_y'] = game.field.ball.row

        # move with IMU input
        if game.field.smd['move_direction'] is not 0:
            game.move_player(game.field.smd['move_direction'])


        # Get all the current events
        for event in pg.event.get():
            # If the window is closed
            if event.type == pg.QUIT:
                window_open = False

            # If a key is pressed
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    window_open = False

                elif event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                    game.move_player(event.key)

                elif event.key == pg.K_q:
                    game.switch_action()

                elif event.key == pg.K_e:
                    if game.pull:
                        game.pull_ball()
                    else:
                        game.shoot_ball()

            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            # position of player is updated only when an event occurs
            game.field.smd['player_x'] = game.field.player.col
            game.field.smd['player_y'] = game.field.player.row

        game.update()

    pg.quit()


# %%
main()
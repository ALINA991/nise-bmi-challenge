import numpy as np
import time
#from vibratingpattern import Vibrate


###### 
##### !!!! check for ball beeing on the border of field : 
##### need to pull in any scenario
#vib = Vibrate()

# get input differently : just defined that way to not get error
def shoot(smd):
    print('shoot')
    

def go_up(smd): # get shared memory as input 
    #smd['move_direction'] = 1
    smd['action_to_int'] = 1
    print('go up')
    time.sleep(0.5)

def go_down(smd): 
    #smd['move_direction'] = 2
    smd["action_to_int"] = 2
    #vib.auomatic_mode(smd['action_to_int'])
    print('go down')
    time.sleep(0.5)


def sideways(smd, direction): # set direction = 0 for right                          #           = 1 for left 
    #smd["move_direction"] = 3 + direction 
    smd["action_to_int"] = 3 + direction 
    #vib.auomatic_mode(smd['action_to_int'])
    print('sideways', smd['action_to_int'])
    time.sleep(0.5)


def shoot_and_run(smd): # add pos_player 
    # question : define for all drections of only up ? 
    smd['emg_trigger'] = 1
    smd['action_to_int'] = 0
    print(smd['action_to_int'])
    #vib.auomatic_mode(smd['action_to_int'])
    time.sleep(0.5)
    go_up(smd)
    go_up(smd)
    smd['emg_trigger'] = 0

def position_behind_ball(smd, direction):
    go_down(smd)
    sideways(smd, direction)
    #assert pos_player == (smd['ball_y'] - 1, smd['ball_x']) # redo error handling 
def pull(smd):
    print('pull')
    #smd['pull_ball'] = True
    #smd['emg_trigger'] = 1
    time.sleep(0.5)
    #smd['pull_ball'] = False
    #smd['action_to_int'] = 9
    print('pull')
    #vib.auomatic_mode(smd['action_to_int'])

def bring_ball_to_middle(smd, direction):
    while smd['ball_x'] <= 3 or smd['ball_x'] >= 6:

        smd['emg_trigger'] = 1
        smd['action_to_int'] = 0
        #vib.auomatic_mode(smd['action_to_int'])
        print(smd['action_to_int'])

        sideways(smd, direction)
        smd['emg_trigger'] = 0
        sideways(smd, direction)

    
def score(smd):
    while smd['ball_y'] > 0 :
        shoot_and_run(smd)
    go_up(smd)
    shoot_and_run(smd)
    #shoot_and_run(smd)


def scenario1(smd, direction): # ball between player and goal
    print('Scenario 1')
    while smd['player_y'] <  smd['ball_y']:
        go_down(smd)
        print(direction)

    print('distance' ,np.abs(smd['player_x'] - smd['ball_x']))
    while not np.abs(smd['player_x'] - smd['ball_x']) == 1:
        print('distance' ,np.abs(smd['player_x'] - smd['ball_x']))
        print('go', direction)
        sideways(smd, direction)
    
    bring_ball_to_middle(smd, direction)
    sideways(smd, direction)
    sideways(smd, direction)
    position_behind_ball(smd, direction)
    score(smd)



def scenario2(smd, direction): #player between ball and goal
    print('Scenario 2')
    while not smd['player_y'] == smd['ball_y']:                # or goal between player and ball
        go_down(smd)
        print('down')
    print(np.abs(smd['player_x'] - smd['ball_x']) == 1)
    while not(np.abs(smd['player_x'] - smd['ball_x']) == 1) :
        print(np.abs(smd['player_x'] - smd['ball_x']) == 1)
        if direction:
            sideways(smd, 0)
            print('sideways' ,direction)
        else:
            sideways(smd, 1)
            print('sideways' ,direction)
    print('try pull sc2')
    pull(smd)
    bring_ball_to_middle(smd, direction)
    position_behind_ball(smd, direction)
    score(smd)




def scenario3(smd, direction): #Player and ball aligned
    print('scenario 3')
    while not smd['player_y'] == smd['ball_y'] - 1:
        go_down(smd)
        print('Down')
    sideways(smd, direction)
    print(direction)
    go_down(smd)
    pull(smd)
    bring_ball_to_middle(smd, direction)
    position_behind_ball(smd, direction)
    #smd['pull_ball'] = True
    score(smd)

def scenario4(smd): #Player and ball aligned
    print('Scenario 4')
    while not smd['player_y'] == smd['ball_y'] - 1:
        go_down(smd)
    print('try pull')
    pull(smd)

    score(smd)


def scenario4_bis(smd, direction):
    while not smd['player_y'] == smd['ball_y'] - 1:
        go_down(smd)
    if direction:
        sideways(smd, 0)
    else:
        sideways(smd,1)
    position_behind_ball(smd, direction)
    shoot_and_run(smd)


def scenario0(smd, direction):
    while not smd['player_y'] == smd['ball_y'] - 1:
        go_down(smd)
    
    while not(np.abs(smd['player_x'] - smd['ball_x']) ==0) :
        print(np.abs(smd['player_x'] - smd['ball_x']) == 0)
        if direction:
            sideways(smd, 0)
            print('sideways' ,direction)
        else:
            sideways(smd, 1)
            print('sideways' ,direction)
        
    pull(smd)

    if not smd['ball_x'] == 4 or smd['ball_x'] == 5:
        if direction:
            sideways(smd, 0)
            print('sideways' ,direction)
        else:
            sideways(smd, 1)
            print('sideways' ,direction)
    
        go_up(smd)
        bring_ball_to_middle(smd, direction)
        position_behind_ball(smd,direction)
    score(smd)

    










def play(pos_player, smd, pos_goal): # define main function ? 

    if smd['ball_y'] <= pos_goal[0]: direction = 0 # includes middle line
    else: direction = 1

    if smd['player_x'] == smd['ball_x']: # check that first to eliminate problems with border cases later
        scenario3(pos_player, smd, pos_goal, direction)
                    # step = direction assures this is a valid interval when pos_player > pos_goal
    elif smd['ball_x'] in range(smd['player_x'] ,pos_goal[1], step=direction ): # if ball beween player and goal
        scenario1(pos_player, smd, pos_goal, direction)                # only if first case not satisfied so no 
                                                                            # problem if == pos player
    elif smd['player_x'] in range(smd['ball_x'], pos_goal[1], step = direction) or pos_goal[1] in range(smd['ball_x'], smd['player_x'], step = direction):
        scenario2(pos_player, smd, pos_goal, direction )
    return


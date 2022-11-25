import numpy as np
import time




# get input differently : just defined that way to not get error

def go_up(smd): # get shared memory as input 
    #smd['move_direction'] = 1
    smd['action_to_int'] = 1
    print(smd['action_to_int'])
    #print('go up')
    time.sleep(0.5)

def go_down(smd): 
    #smd['move_direction'] = 2
    smd["action_to_int"] = 2
    print(smd['action_to_int'])
    #vib.auomatic_mode(smd['action_to_int'])
    #print('go down')
    time.sleep(0.5)


def sideways(smd, direction): # set direction = 0 for right                          #           = 1 for left 
    #smd["move_direction"] = 3 + direction 
    smd["action_to_int"] = 3 + direction 
    #vib.auomatic_mode(smd['action_to_int'])
    print(smd['action_to_int'])
    time.sleep(0.5)

def pull(smd):
    #smd['pull_ball'] = True
    #smd['emg_trigger'] = 1
    time.sleep(0.5)
    #smd['pull_ball'] = False
    smd['action_to_int'] = 9
    print(smd['action_to_int'])
    #vib.auomatic_mode(smd['action_to_int'])

def shoot(smd):
    smd['action_to_int'] = 0
    print(smd['action_to_int'])
    


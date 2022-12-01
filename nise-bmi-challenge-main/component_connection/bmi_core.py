# %%
#import serial
import numpy as np
from matplotlib.gridspec import SubplotSpec, GridSpec
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
import socket
import importlib

import test_algo_vib as tav
importlib.reload(tav)
from vibratingpattern import Vibrate

# UDP network
UDP_IP = "192.168.4.1"
UDP_PORT = 9999
MESSAGE = "000_000_000_000"  
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)
   
vib = Vibrate()
sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

# shared memory for EMG and ball and player positions
smd = SharedMemoryDict(name='msg', size=1024)
smd["ball_x"] = 0
smd["ball_y"] = 0
smd["player_x"] = 0
smd["player_y"] = 0
smd["emg_trigger"] = None
smd["move_direction"] = 0
smd["pull_ball"] = False
smd["action_to_int"] = None


number_vibros = 4
intensity_array = [0,0,0,0]

#port = serial.Serial('COM10', baudrate=512000) # Windows
# port = serial.Serial('/dev/ttyUSB0')  # Linux


counter = 0
vib = Vibrate()

def send_array_udp(intensity): #multiplicate all values in vib array with 255 and make them feelable!
        '''
        Send intensity array through UDP to ESP32 with vibromotors
        '''
        number_vibros = len(intensity)
        line = ''
        j = 0
        dash_or_no_dash = False
        while j < number_vibros: # go through all vibros
            scaled_intensity = int(intensity[j]/9*255) #scaled to fit 8-bit transport
            if scaled_intensity > 255: 
                scaled_intensity = 255
            new_string_element = str(scaled_intensity) 
            if dash_or_no_dash == True: 
                line = line + '_' 
            else: 
                dash_or_no_dash = True

            if (len(new_string_element) == 3):
                line = line + new_string_element
            
            elif (len(new_string_element) == 2):
                line = line + '0' + new_string_element
            
            elif (len(new_string_element) == 1):
                line = line + '00' + new_string_element
            
            elif (len(new_string_element) == 0):
                line = line + '000'
            j += 1
        line = line + '\n'
        # send through UDP
        print(line.encode())
        sock.sendto(line.encode(), (UDP_IP, UDP_PORT))
        j = 0
        time.sleep(0.75)  # Has to be greater than message execute time 





while True:

    

    ball_goal_aligned_x = smd['ball_x'] == 4 or smd['ball_x'] == 5 
    ball_player_aligned_x = smd['ball_x'] == smd['player_x']

    ball_goal_player_aligned = ball_goal_aligned_x and ball_player_aligned_x 
    score_position = ball_goal_player_aligned and smd['player_y'] > smd['ball_y']
    shoot_to_score_position = smd['player_y'] == smd['ball_y'] + 1

    action_position_x = np.abs(smd['player_x'] - smd['ball_x']) == 1

    ball_right = smd['ball_x'] >= 5
    ball_player_aligned_y = smd['ball_y'] == smd['player_y']
    
    pull_position_x = (smd["player_x"] > smd["ball_x"] and not ball_right) or (smd["player_x"] < smd["ball_x"] and ball_right)

    pull_position_y = smd["player_y"] +1 == smd["ball_y"]
    player_below_ball = smd['player_y'] > smd['ball_y']

    ball_on_edge = smd['ball_y'] == 9


    if not score_position: # if not positions from top: goal, ball, player 
        if not ball_on_edge: # handle edge case when cannot go belwo ball 

            if not ball_goal_aligned_x: # if ball and goal not aligned 
                if not ball_player_aligned_x: # if ball and player are not in same column

                    if not ball_player_aligned_y: # ball is not in same row as player

                        if not player_below_ball:
                            tav.go_down(smd)
                        else:
                            tav.go_up(smd)
                    else: 
                        if not action_position_x:
                            direction = int(smd['ball_x'] > smd['player_x'])  # 0 if go left, 1 if go right
                            tav.sideways(smd, direction)
                        else:
                            if not pull_position_x:
                                tav.shoot(smd)
                            else:
                                tav.pull(smd)
                        # align ball and goal 
                else: # move sideways into field
                    direction = int(not ball_right)
                    tav.sideways(smd, direction)
            else: # aligned on x axis 

                if not player_below_ball:
                    if not pull_position_y:
                        tav.go_down(smd)
                    else:
                        tav.pull(smd)
                else:
                    direction = int(smd['ball_x'] > smd['player_x'])  # 0 if go left, 1 if go right
                    tav.sideways(smd, direction)
            # position behind ball 

        else: # if the ball is on the lower edge of field
            if not ball_player_aligned_x:  # bring player to same column
                direction = int(smd['ball_x'] > smd['player_x']) 
                tav.sideways(smd, direction)
            else: # on same colums -> bring to ball 
                if not pull_position_y:
                    tav.go_down(smd)
                else:
                    tav.pull(smd)

    else: # shoot and run until goal
            if not shoot_to_score_position:
                tav.go_up(smd)
            else:
                tav.shoot(smd)
            


    '''


    # Get the message from ESP32 with IMU and EMG
    #.readline()

    # Get current ball and player positions from shared memory
    if counter % 10 == 0:
        # print ball and player position
        
        print(f"Ball:\t{smd['ball_x'],smd['ball_y']}\tPlayer:\t{smd['player_x'], smd['player_y']}")

        '''

  
    
    
    # Send feedback intensities to ESP32 with vibrotactile motors

    send_array_udp(vib.automatic_mode(smd['action_to_int']))
    


    counter += 1
        

### Possibly that emg trigger doesn't get reset quick enough so the player shoot twice
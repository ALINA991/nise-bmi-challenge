# %%
# RUN 
# /home/almo/anaconda3/envs/semg/bin/python /media/almo/Windows-SSD/Users/Thien/Documents/MSNE/WS22_NISE/BMI_Code/NISE/nise-bmi-challenge/component_connection/bmi_core.py
import serial
import numpy as np
from matplotlib.gridspec import SubplotSpec, GridSpec
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
import socket

### Import Team Specific code 
# import sys
# from pathlib import Path
# current_path = Path(__file__).parent.resolve() 
# gamedir = current_path.parent
# # print(one_up)
# sys.path.append(str(gamedir))
# # print(sys.path)
# from decode_encode.vibratingpattern import Vibrate
from vibratingpattern import Vibrate


# UDP network   
UDP_IP = "192.168.4.1"
UDP_PORT = 9999
MESSAGE = "000_000_000_000"  
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)
   
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
# 0: kick, up : 1, down, left, right,  9: pull
number_vibros = 4
# intensity_array = [5,5,5,5]

# Also for getting information 
# port = serial.Serial('COM6', baudrate=115200) # Windows
# port = serial.Serial('/dev/ttyUSB0')  # Linux
vibrate = Vibrate()

counter = 0

def send_array_udp(intensity, number_vibros): #multiplicate all values in vib array with 255 and make them feelable!
        '''
        Send intensity array through UDP to ESP32 with vibromotors
        '''
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
        # print(f'The line that it is sending {line}')
        # send through UDP
        print(line.encode())
        sock.sendto(line.encode(), (UDP_IP, UDP_PORT))
        j = 0
        time.sleep(0.5)


while True:
    # Get the message from ESP32 with IMU and EMG
    # It waits for message so dont do this unless we have connection 
    # msg = port.readline()
    # Get current ball and player positions from shared memory
    # if counter % 10 == 0:
        # print ball and player position
        # print(f"Ball:\t{smd['ball_x'], smd['ball_y']}\tPlayer:\t{smd['player_x'], smd['player_y']}")

    new_msg = vibrate.run_maual_perception(player_pos=[smd['player_x'], smd['player_y']], 
        ball_pos=[smd['ball_x'], smd['ball_y']])


    # if counter % 100000 == 0:   # SLOW the print out down
    #     # print(f'distance away from ball {distance_to_ball}')
    # # Send feedback intensities to ESP32 with vibrotactile motors
    #     for i in range(6):
    #         if counter % 1000 == 0:
    #             print(new_msg[i,:])
    #             send_array_udp(new_msg[i,:], number_vibros)
    #             counter += 1


    message = [0,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6]
    send_array_udp(message, number_vibros=16)
    # send_array_udp(new_msg[0,:], number_vibros)



    # send_array_udp(intensity_array, number_vibros)
    # counter += 1
        


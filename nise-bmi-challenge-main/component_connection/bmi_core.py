# %%
#import serial
import numpy as np
from matplotlib.gridspec import SubplotSpec, GridSpec
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
import socket
import importlib

import test_algo as ta
importlib.reload(ta)

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
smd["action_to_int"] = None


number_vibros = 4
intensity_array = [0,0,0,0]

#port = serial.Serial('COM10', baudrate=512000) # Windows
# port = serial.Serial('/dev/ttyUSB0')  # Linux


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

        # send through UDP
        sock.sendto(line.encode(), (UDP_IP, UDP_PORT))
        j = 0
        #time.sleep(0.5)

time.sleep(0.5)




while True:


    
    if smd['ball_x'] >=  5 or (smd['ball_x'] == 4 and smd['player_x'] >= smd['ball_x']): 
        direction = 0  
        direction1 = -1
        print(1)
    
    elif smd['ball_x'] <= 4 or (smd['ball_x'] == 5 and smd["player_x"] <= smd['ball_x']): 
        direction = 1
        direction1 = 1
        print(0)

    # Get the message from ESP32 with IMU and EMG
    #.readline()

    # Get current ball and player positions from shared memory
    if counter % 10 == 0:
        # print ball and player position
        
        print(f"Ball:\t{smd['ball_x'],smd['ball_y']}\tPlayer:\t{smd['player_x'], smd['player_y']}")
        print(smd['action_to_int'])

        if smd['ball_y'] == 9:
            ta.scenario0(smd, direction)

        if (smd["player_x"] < smd["ball_x"] and smd["ball_x"] <= 5)  or  (smd["player_x"] > smd["ball_x"] and smd["ball_x"]  >= 4 and not (smd['ball_x'] == 0 or smd['ball_x'] == 9)):
            ta.scenario1(smd, direction)

        elif smd["player_x"] == smd["ball_x"] :
            if smd["ball_x"] == 4 or smd["ball_x"] == 5:
                ta.scenario4(smd)
            else:
                ta.scenario3(smd, direction)
    
        else:
            ta.scenario2(smd, direction)
    
    
    # Send feedback intensities to ESP32 with vibrotactile motors

    send_array_udp(intensity_array, number_vibros)
    


    counter += 1
        
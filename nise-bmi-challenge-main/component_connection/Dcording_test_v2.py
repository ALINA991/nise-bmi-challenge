# %%  source pyt3/bin/activate
import serial
import numpy as np
from matplotlib.gridspec import SubplotSpec, GridSpec
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
import socket
import sys
# import termplotlib as tpl
import scipy as sp

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
smd["emg_triggertoaction"] = {"kick":0, "up": 1, "down" : 2, "right": 3, "left" : 4, "pull": 9}

number_vibros = 4
intensity_array = [0,0,0,0]

# port = serial.Serial('COM9', baudrate=512000) # Windows
# port = serial.Serial('/dev/cu.usbserial-0285F948')  # Linux
port = serial.Serial(port='/dev/cu.usbserial-0285F948', baudrate=500000)
# set.port = 
# serial.baudrate = 500000
# serial.open()

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


msg_vec = []
filtered_vec = []

# fig = plt.figure()
# plt.axis([0, 500, 0, 1])

while True:
    acc_x_vec = []
    pitch_mean = 0
    roll_mean = 0

    trial = 0
    detect = 0
    counter = 0
    # smallar than 1 sec
    while counter< 300:#True:
        # Get the message from ESP32 with IMU and EMG
        msg = port.readline()   #PROBLEMMP
        msg = str(msg)
        msg = msg.lstrip("b'")
        msg = msg.rstrip("\\r\\n'")
        msg = msg.split("\\t")
        #print(msg)

        gyro_x = float(msg[0])
        gyro_y = float(msg[1])
        gyro_z = float(msg[2])
        acc_x = float(msg[3])    #push (1 negative, 2 pos) and pull (1 pos, 2 neg) .  th: 20
        acc_y = float(msg[4])
        acc_z = float(msg[5])
        mag_x = float(msg[6])
        mag_y = float(msg[7])
        mag_z = float(msg[8])
        pitch = float(msg[9])   # // pitch:   positive left, negative right   th 50
        roll = float(msg[10])   #  //roll:    up negative, back positive   th 70
        rms = float(msg[11])

        acc_x_vec.append(acc_x) 
        pitch_mean = pitch + pitch_mean
        roll_mean = roll + roll_mean
        # print(type(gyro_x))

        # print(str(counter)+'          '+msg)
        # msg = float(msg)
        

        # msg_vec.append(msg)

        # plt.show()
        # plt.scatter(counter,msg)

        # plt.show(block='Flase')       
        # plt.close('all') 

        # # Get current ball and player positions from shared memory
        # if counter % 10 == 0:
        #     # print ball and player position
        # # print(f"Ball:\t{smd['ball_x'], smd['ball_y']}\tPlayer:\t{smd['player_x'], smd['player_y']}")
        #     # for cutoff in [.03, .05, .1]:
        #     #     b, a = sp.signal.butter(3, cutoff)
        #     #     filtered = sp.signal.filtfilt(b, a, data)
        #     #     filtered_vec.append(filtered)
        #     # plt.plot(filtered_vec)
        #     # plt.show()

        # # Send feedback intensities to ESP32 with vibrotactile motors
        # send_array_udp(intensity_array, number_vibros)
        counter += 1

    print(acc_x_vec)
    def gyrox_fun(acc_x_vec, way):
        period = 100
        action = 100
        if way == 1:
            for ii in range(len(acc_x_vec)):
                if acc_x_vec[ii] > 20:
                    if trial < period:
                        trial += 1
                        if acc_x_vec[ii+trial] < -20:
                            action = 9
                        else:
                            action = 100
        
        elif way == 2:
            max_val = max(acc_x_vec)

            min_val = min(acc_x_vec)
            acc_x_vec = np.array(acc_x_vec)
            min_pos = acc_x_vec.argmin()
            max_pos = acc_x_vec.argmax()
            if max_val > 20 and min_val < -20: #and abs(min_pos-max_pos)<:
                print("mi_pos",min_pos)
                if min_pos < max_pos:

                    
                    action = 0
                else:
                    
                    action = 9
        return action

                    
    pitch_mean = pitch_mean/counter
    roll_mean = roll_mean/counter


    action = gyrox_fun(acc_x_vec, 2)

    if pitch_mean > 50:
        action = 4
    elif pitch_mean < -50:
        action = 3

    if roll_mean > 60:
        action = 2
    elif roll_mean < -60:
        action = 1



    print("action"+str(action))

    # np.save('test2', msg_vec)

    # plt.figure()
    # plt.plot(np.linspace(1,len(msg_vec)-1,len(msg_vec)),msg_vec)
    # plt.xlim((10,len(msg_vec)-1))
    # plt.savefig('fig_2')
    #print('holaaaaaa')
    cc =+1
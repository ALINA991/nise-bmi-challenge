# %%  source pyt3/bin/activate
import serial
import numpy as np
import scipy as sp
from matplotlib.gridspec import SubplotSpec, GridSpec
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
import socket
import sys
# import termplotlib as tpl


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
# smd["emg_triggertoaction"] = {"kick":0, "up": 1, "down" : 2, "right": 3, "left" : 4, "pull": 9}

number_vibros = 4
intensity_array = [0,0,0,0]

# port = serial.Serial('COM9', baudrate=512000) # Windows
# port = serial.Serial(port='/dev/cu.usbserial-0285F948', baudrate=500000)
port = serial.Serial(port='/dev/ttyUSB1', baudrate=500000)

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

# fig = plt.figure()
# plt.axis([0, 500, 0, 1])

msg_vec = []
filtered_vec = []
detect_vec = []
acc_x_vec = []
trial = 0
counter = 0
th_acc = 20
th_pitch = 50
th_roll = 50
interval = 50
acc_x_interval = 100
acc_z_interval = 100
detect_acc_x = 0
detect_acc_z = 0
detect_pitch = 0
detect_roll = 0
acc_x_action = 0
acc_z_action = 9
pitch_action = [3,4]
roll_action = [2,1]
kick_triger_x = 100    #kick=1, pull = 0
kick_triger_z = 100    #kick=1, pull = 0



def movement_command(direction, threshold, interval, detect, action):
    if direction > threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[0]
            # smd["emg_triggertoaction"] = action[0]
            print(action[0])
            detect = 0

    elif direction < -threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[1]
            # smd["emg_triggertoaction"] = action[1]
            print(action[1])
            detect = 0
    else:
        detect = 0
    return detect

def acc_x_command(direction, threshold, interval, detect, action):
    if abs(direction) > threshold and detect == 0:
            smd["emg_trigger"] = 1
            smd['pull_ball'] = True
            print(action)
            time.sleep(0.5)
        #     smd["emg_trigger"] = 1
        #     smd['pull_ball'] = False
            detect = 1
    if detect>=1 and detect < interval: 
        detect += 1
    if detect == interval:
        detect = 0
    return detect
        
def acc_z_command(direction, threshold, interval, detect, action):
    if abs(direction) > threshold and detect == 0:
            # smd["emg_trigger"] = 1
            # smd['pull_ball'] = True
            smd["emg_trigger"] = 1
            smd['pull_ball'] = False
            print(action)
            time.sleep(0.5)
            detect = 1
    if detect>=1 and detect < interval: 
        detect += 1
    if detect == interval:
        detect = 0
    return detect

# def emg_command(emg, threshold, window_size, action):
    # c =0
    # count = []
    # while c < window_size:
    #     count.append(emg)
    # baseline = np.mean(count)
    # max_value = abs(max(count)-baseline)
    # min_value = abs(min(count)-baseline)
    # band = max(max_value,min_value)
    # if emg > baseline + band or emg <  baseline - band:
    #     while c < window_size:
    #         count.append(emg)
    # baseline2 = np.mean(count)
    # if baseline2 - baseline > thr:
    #     action
    # else:
    #     baseline = baseline2

window_size = 1
threshold = 20
freezing_time = 200
isit = 0
hh = 0
freeze = 0
refer_point = 0

def emg_command(emg, threshold, window_size, action, refer_point,hh, isit, freeze, freezing_time):
    # c =0
    
    hh += 1
    #print(emg - refer_point/hh - threshold)
    if freeze == 0:
        refer_point += emg

        if emg > refer_point/hh + threshold:
            isit +=1
        #print("isit", isit)
        #print("window sie", window_size)
        if isit == window_size:
            # print("jfgdhgkjdhgkthuuy")
            smd["emg_trigger"] = 1
            smd['pull_ball'] = False
            print(action)
            freeze += 1
    elif freeze< freezing_time and freeze > 0:
        freeze += 1
    else:
        freeze = 0
        refer_point = 0
        hh = 0
        isit = 0

    return freeze, hh, refer_point, isit


    # if emg > threshold and detect == 0:
    #         # smd["emg_trigger"] = 1
    #         # smd['pull_ball'] = True
    #         smd["emg_trigger"] = 1
    #         smd['pull_ball'] = False
    #         print(action)
    #         time.sleep(0.5)
    #         detect = 1
    # if detect>=1 and detect < interval: 
    #     detect += 1
    # if detect == interval:
    #     detect = 0
    # return detect
    
    
    # if direction > threshold and detect==0:
    #     kick_triger = 1    #kick
    #     detect += 1   #initiation and start to recording
    # if direction < -threshold and detect==0:
    #     kick_triger = 0    #pull
    #     detect += 1   #initiation and start to recording
    

        # print("we are here")
        # if  direction < -threshold and kick_triger==1:
        #     smd["emg_trigger"] = 1
        #     smd['pull_ball'] = True
        #     # smd["move_direction"] = action[0]
        #     time.sleep(1)
        #     smd['pull_ball'] = False
        #     print(action[0])
        #     detect = 0
        #     kick_triger = 100
        #     # time.sleep(1)
        # elif direction > threshold and kick_triger==0:
        #     smd["emg_trigger"] = 1
        #     smd['pull_ball'] = False
        #     time.sleep(1)
        #     print(action[1])
        #     detect = 0

        #     kick_triger = 100
            # time.sleep(1)




emg_data = []

while True:
    # smallar than 1 sec
    # while counter<300:
    # Get the message from ESP32 with IMU and EMG
    # print("working")

    try : 
        # print("attempt to read message")
        msg = port.readline()   #PROBLEMMP
        # msg1 = msg.decode('utf-8')    #trans into str
        msg = str(msg)
        msg = msg.lstrip("b'")
        msg = msg.rstrip("\\r\\n'")
        msg = msg.split("\\t")

        # gyro_x = float(msg[0])
        # gyro_y = float(msg[1])
        # gyro_z = float(msg[2])
        acc_x = float(msg[3])  # Excustion push (1 negative, 2 pos) and pull (1 pos, 2 neg) .  th: 20
        # print("attempt to read acc")
        # acc_y = float(msg[4])
        acc_z = float(msg[5])  #switch 
        # mag_x = float(msg[6])
        # mag_y = float(msg[7])
        # mag_z = float(msg[8])
        pitch = float(msg[9])   # // pitch:   positive left, negative right   th 50
        roll = float(msg[10])   #  //roll:    up negative, back positive   th 70
        rms = float(msg[11])
        # print("attempt to read emg data ")
        emg_data.append(rms)
        # acc_data.append(acc_x)
        # acc_x_vec.append(acc_x) 
        detect_pitch = movement_command(pitch, th_pitch, interval, detect_pitch, pitch_action)
        detect_roll = movement_command(roll, th_roll, interval, detect_roll, roll_action)
        detect_acc_x = acc_x_command(acc_x, th_acc, interval, detect_acc_x, acc_x_action)
        # detect_acc_z = acc_z_command(acc_z, th_acc, interval, detect_acc_z, acc_z_action)
        freeze, hh, refer_point, isit = emg_command(rms, threshold, window_size, acc_z_action, refer_point,hh, isit, freeze, freezing_time)

        # print(kick_triger)
        # print(kick_triger)
        # msg_vec.append(msg)
        # plt.show()
        # plt.scatter(counter,msg)

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
    except Exception :
        print("message corrupted")
        continue
    counter += 1
    
    # np.save('test2', msg_vec)
    # plt.figure()
    # plt.plot(np.linspace(1,len(msg_vec)-1,len(msg_vec)),msg_vec)
    # plt.xlim((10,len(msg_vec)-1))
    # plt.savefig('fig_2')
    #print('holaaaaaa')
    # cc =+1

# plt.figure()
# plt.plot(range(len(emg_data)),emg_data)
# plt.show()
# plt.figure()
# #plt.plot(np.linspace(0,len(acc_data)-1,len(acc_data)), acc_data)
# plt.plot(acc_data)
# plt.show()
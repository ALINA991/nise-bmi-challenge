# %%  source pyt3/bin/activate
import serial
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
from scipy import signal

###THRESHOLD FOR DETECTION 
EMG_TRHESHOLD = 200


# shared memory for EMG and ball and player positions
smd = SharedMemoryDict(name='msg', size=1024)
smd["ball_x"] = 0
smd["ball_y"] = 0
smd["player_x"] = 0
smd["player_y"] = 0
smd["emg_trigger"] = None
# port = serial.Serial(port='/dev/cu.usbserial-0285F948', baudrate=500000)
port = serial.Serial(port='/dev/ttyUSB0', baudrate=500000)
counter = 0
b, a = signal.butter(8, [60,90], 'bandpass', analog=False, fs=1000)
detect_kick = 0
detect_pull = 0
detect_pitch = 0
detect_roll = 0
emg_data = []

### Thien's experiments 
experiment_counter = 0 



def movement_command(msg, threshold, interval, detect, action):
    global experiment_counter
    if msg > threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[0]
            print(action[0])
            experiment_counter += 1
            detect = 0

    elif msg < -threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[1]
            print(action[1])
            experiment_counter += 1
            detect = 0
    else:
        detect = 0
    return detect

def execution_command(msg, threshold, interval, detect, action):
    global experiment_counter
    if abs(msg) > threshold and detect == 0:
        smd["emg_trigger"] = 1
        if action == 0:
            smd['pull_ball'] = True
        elif action == 9:
            smd['pull_ball'] = False
        print(action)
        experiment_counter += 1
        time.sleep(0.5)
        detect = 1
    if detect>=1 and detect < interval: 
        detect += 1
    if detect == interval:
        detect = 0
    return detect


if __name__ == '__main__':
    while 1: ## counter<2000:
        # Get the message from ESP32 with IMU and EMG
        msg = port.readline()   #PROBLEMMP
        msg = msg.decode('utf-8')    #trans into str
        msg = msg.split()
        try:
            # action_type = "up": 1, "down" : 2, "right": 3, "left" : 4, "kick":0, "pull": 9
            #roll = "up" or "down"; pitch = "right" or "left"; acc_x = "kick"; rms = "pull"

            acc_z = float(msg[4])
            pitch = float(msg[8])
            roll = float(msg[9])
            rms = float(msg[10])
        except : continue
        # if counter==0:
        #     z = signal.lfilter_zi(b, a) * rms
        # frms, z = signal.lfilter(b, a, [rms], zi=z)      #filtering ems signal using bandpass filter (with coefficient array a, b)
        frms = rms
        # print(f'Filter RMS data {frms}')
        detect_roll = movement_command(msg = roll, threshold = 15, interval = 30, detect = detect_roll, action = [2,1])
        detect_pitch = movement_command(msg = pitch, threshold = 15, interval = 30, detect = detect_pitch, action = [3,4])
        detect_pull = execution_command(msg = acc_z, threshold = 15, interval = 100, detect = detect_pull, action = 0)
        detect_kick = execution_command(msg = frms, threshold = EMG_TRHESHOLD, interval = 150, detect = detect_kick, action = 9)
        # emg_data.append(frms)
        print(experiment_counter)
        

        counter += 1
    plt.figure()
    plt.plot(range(len(emg_data)),emg_data)
    plt.show()
 
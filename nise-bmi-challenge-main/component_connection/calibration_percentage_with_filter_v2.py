# %%  source pyt3/bin/activate
import serial
import numpy as np
import matplotlib.pyplot as plt
from shared_memory_dict import SharedMemoryDict
import time
import socket
from scipy import signal

# # UDP network
# UDP_IP = "192.168.4.1"
# UDP_PORT = 9999
# MESSAGE = "000_000_000_000"  
# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
# print("message: %s" % MESSAGE)
   
# sock = socket.socket(socket.AF_INET, # Internet
#                         socket.SOCK_DGRAM) # UDP

# shared memory for EMG and ball and player positions
smd = SharedMemoryDict(name='msg', size=1024)
smd["ball_x"] = 0
smd["ball_y"] = 0
smd["player_x"] = 0
smd["player_y"] = 0
smd["emg_trigger"] = None
# port = serial.Serial(port='/dev/cu.usbserial-0285F948', baudrate=500000)
port = serial.Serial(port='/dev/ttyUSB0', baudrate=500000)

def movement_command(msg, threshold, interval, detect, action):
    if msg > threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[0]
            print(action[0])
            detect = 0

    elif msg < -threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[1]
            print(action[1])
            detect = 0
    else:
        detect = 0
    return detect

def execution_command(msg, threshold, interval, detect, action):
    if abs(msg) > threshold and detect == 0:
        smd["emg_trigger"] = 1
        if action == 0:
            smd['pull_ball'] = True
        elif action == 9:
            smd['pull_ball'] = False
        print(action)
        time.sleep(0.5)
        detect = 1
    if detect>=1 and detect < interval: 
        detect += 1
    if detect == interval:
        detect = 0
    return detect


def cali(which, time0, trials):
    counter = 0
    b, a = signal.butter(8, [60,90], 'bandpass', analog=False, fs=1000)
    detect_kick = 0
    detect_pull = 0
    detect_pitch = 0
    detect_roll = 0
    
    all_acc_x_vec = np.zeros((trials,time0))
    all_pitch_vec = np.zeros((trials,time0))
    all_roll_vec = np.zeros((trials,time0))
    all_emg_vec = np.zeros((trials,time0))
    
    to_get_thr_max = np.zeros((trials,4))
    to_get_thr_min = np.zeros((trials,4))
    
    plt.figure()
    fig, axs = plt.subplots(2, 2,sharex=True)
    
    window_size = 1
    threshold = 20
    freezing_time = 200
    isit = 0
    hh = 0
    freeze = 0
    refer_point = 0
    b, a = signal.butter(8, [60,90], 'bandpass', analog=False, fs=1000)
    for ii in range(trials):

        acc_x_vec = []
        pitch_vec = []
        roll_vec = []
        emg_vec = []
        counter = 0
        print('trial',ii)
        while counter<time0:
            try:
                # Get the message from ESP32 with IMU and EMG
                msg = port.readline()   #PROBLEMMP
                msg = msg.decode('utf-8')    #trans into str
                msg = msg.split()

                # action_type = "up": 1, "down" : 2, "right": 3, "left" : 4, "kick":0, "pull": 9
                #roll = "up" or "down"; pitch = "right" or "left"; acc_x = "kick"; rms = "pull"
                acc_x = float(msg[2])
                pitch = float(msg[8])
                roll = float(msg[9])
                rms = float(msg[10])
                
                if counter==0:
                    z = signal.lfilter_zi(b, a) * rms
                frms, z = signal.lfilter(b, a, [rms], zi=z)      #filtering ems signal using bandpass filter (with coefficient array a, b)
                
                detect_roll = movement_command(msg = roll, threshold = 20, interval = 50, detect = detect_roll, action = [2,1])
                detect_pitch = movement_command(msg = pitch, threshold = 20, interval = 50, detect = detect_pitch, action = [3,4])
                detect_pull = execution_command(msg = acc_x, threshold = 20, interval = 50, detect = detect_pull, action = 0)
                detect_kick = execution_command(msg = frms, threshold = 3, interval = 200, detect = detect_kick, action = 9)
        
                counter += 1
                emg_vec.append(frms)
                acc_x_vec.append(acc_x)
                pitch_vec.append(pitch)
                roll_vec.append(roll)
            except Exception:
                print('oh no')
                continue
        
        all_acc_x_vec[ii,:] = np.array(acc_x_vec)  
        all_pitch_vec[ii,:] = np.array(pitch_vec)
        all_roll_vec[ii,:] = np.array(roll_vec)
        all_emg_vec[ii,:] = np.array(emg_vec)
        
        to_get_thr_max[ii,:] = [max(acc_x_vec),max(all_emg_vec),max(pitch_vec),max(roll_vec)]   
        to_get_thr_min[ii,:] = [min(acc_x_vec),max(all_emg_vec),min(pitch_vec),min(roll_vec)]   

        titles = ['Acceleration x','EMG', 'Pitch', 'Roll']
        

    for kk in range(trials-1):     
        axs[0,0].plot(np.linspace(0,time0-1,time0), all_acc_x_vec[kk+1,:], label='Calibration data')
        axs[0,0].set_title(titles[0])
    
        axs[0,1].plot(np.linspace(0,time0-1,time0), all_emg_vec[kk+1,:], label='Calibration data')
        axs[0,1].set_title(titles[1])
    
        axs[1,0].plot(np.linspace(0,time0-1,time0), all_pitch_vec[kk+1,:], label='Calibration data')
        axs[1,0].set_title(titles[2])
        
        axs[1,1].plot(np.linspace(0,time0-1,time0), all_roll_vec[kk+1,:], label='Calibration data')
        axs[1,1].set_title(titles[3])
        
        
    titles = ['Acceleration x','EMG', 'Pitch', 'Roll']
    
    fig.suptitle(titles[which])
    fig.supylabel('Calibration data')
    fig.supxlabel('Time')
    plt.show(block=True)
    fig.savefig(titles[which]+'__calibration_data.png', format="png",dpi=1200)

    titles = ['Acceleration x','EMG', 'Pitch', 'Roll']
    
    thr_max = np.median(to_get_thr_max, axis = 0)
    thr_min = np.median(to_get_thr_min, axis = 0)
    
    thr_max_abs = np.zeros(4)
    print('np.shape(thr_max)',np.shape(thr_max))
    print('thr_max',thr_max)

    plt.figure()
    for jj in range(len(thr_max)):
        plt.scatter(jj,max(abs(thr_max[jj]), abs(thr_min[jj])), label=titles[jj])
        thr_max_abs[jj] = max(abs(thr_max[jj]), abs(thr_min[jj]))

    plt.ylabel('Median of the maximum absolute value of the calibration data')
    titles = ['Acc. x','EMG', 'Pitch', 'Roll']
    labels = titles
    plt.xticks(range(4), labels, rotation='vertical')

    
    plt.title('Movement: '+titles[which])
    plt.savefig(titles[which]+'__median_max_abs_cal_data.png',  format="png", dpi = 1200)
    plt.show(block=True)   
    
    return thr_max_abs

def cali_pipeline(time0, trials):
    
    all_thr_max_abs = np.zeros((4,4))
    titles = ['Acc. x','EMG', 'Pitch', 'Roll']
    titles2 = ['Acceleration x calibration','EMG calibration', 'Pitch calibration', 'Roll calibration']

    
    for kk in range(4):
        print(titles[kk]+' Calibration')
        
        thr_max_abs = cali(kk, time0, trials)
        all_thr_max_abs[kk,:] = thr_max_abs
        
    plt.figure()
    for ll in range(4):
        plt.scatter(range(4),all_thr_max_abs[ll,:],label=titles2[ll])
    plt.legend()   
    plt.title('Calibration data')
    labels = titles
    plt.xticks(range(4), labels, rotation='vertical')
    plt.show(block=True)  
    plt.savefig('all_cali_median_max_abs_cal_data.png',format="png", dpi = 1200)
    
    print('all_thr_max_abs',all_thr_max_abs)
    return all_thr_max_abs
    
cali_pipeline(600, 11)



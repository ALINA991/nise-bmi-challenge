#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:24:46 2022

@author: maria
"""
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
smd["emg_triggertoaction"] = {"kick":0, "up": 1, "down" : 2, "right": 3, "left" : 4, "pull": 9}

number_vibros = 4
intensity_array = [0,0,0,0]

# port = serial.Serial('COM9', baudrate=512000) # Windows
# port = serial.Serial(port='/dev/cu.usbserial-0285F948', baudrate=500000)
port = serial.Serial(port="/dev/ttyUSB0", baudrate=500000)
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

        sock.sendto(line.encode(), (UDP_IP, UDP_PORT))
        j = 0





def movement_command(direction, threshold, interval, detect, action):
    if direction > threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[0]
            print(action[0])
            detect = 0

    elif direction < -threshold:
        detect += 1
        if detect > interval:
            smd["move_direction"] = action[1]
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
            detect = 1
    if detect>=1 and detect < interval: 
        detect += 1
    if detect == interval:
        detect = 0
    return detect
        
def acc_z_command(direction, threshold, interval, detect, action):
    if abs(direction) > threshold and detect == 0:
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

    
def emg_command(emg, threshold, window_size, action, refer_point,hh, isit, freeze, freezing_time):
    hh += 1
    if freeze == 0:
        refer_point += emg

        if emg > refer_point/hh + threshold:
            isit +=1
        if isit == window_size:
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





def cali(which, time0, trials):
    msg_vec = []
    filtered_vec = []
    detect_vec = []
    

    
    trial = 0
    counter = 0
    th_acc = 20
    th_pitch = 50
    th_roll = 60
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
    
    all_acc_x_vec = np.zeros((trials,time0))
    all_acc_z_vec = np.zeros((trials,time0))
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
    
    for ii in range(trials):

        acc_x_vec = []
        acc_z_vec = []
        pitch_vec = []
        roll_vec = []
        emg_vec = []
        counter = 0
        print('trial',ii)
        while counter<time0:
            try:

                msg = port.readline()   

                msg = str(msg)
                msg = msg.lstrip("b'")
                msg = msg.rstrip("\\r\\n'")
                msg = msg.split("\\t")
            
                acc_x = float(msg[3])  
                acc_z = float(msg[5])  
                pitch = float(msg[9])   
                roll = float(msg[10])  
                rms = float(msg[11])
                
                emg_vec.append(rms)
                acc_x_vec.append(acc_x)
                acc_z_vec.append(acc_z)
                pitch_vec.append(pitch)
                roll_vec.append(roll)
                
                
                detect_pitch = movement_command(pitch, th_pitch, interval, detect_pitch, pitch_action)
                detect_roll = movement_command(roll, th_roll, interval, detect_roll, roll_action)
                detect_acc_x = acc_x_command(acc_x, th_acc, interval, detect_acc_x, acc_x_action)
                detect_acc_z = acc_z_command(acc_z, th_acc, interval, detect_acc_z, acc_z_action)
                freeze, hh, refer_point, isit = emg_command(rms, threshold, window_size, acc_z_action, refer_point,hh, isit, freeze, freezing_time)
        
                counter += 1
            except Exception:
                print('oh no')
                continue
        
        all_acc_x_vec[ii,:] = np.array(acc_x_vec)  
        all_acc_z_vec[ii,:] = np.array(acc_z_vec)  
        all_pitch_vec[ii,:] = np.array(pitch_vec) 
        all_roll_vec[ii,:] = np.array(roll_vec) 
        all_emg_vec[ii,:] = np.array(emg_vec) 
        
        to_get_thr_max[ii,:] = [max(acc_x_vec) ,max(acc_z_vec),max(pitch_vec),max(roll_vec)]   
        to_get_thr_min[ii,:] = [min(acc_x_vec) ,min(acc_z_vec),min(pitch_vec),min(roll_vec)]   
        
        
        everything0=[acc_x_vec, emg_vec, pitch_vec, roll_vec]
        
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



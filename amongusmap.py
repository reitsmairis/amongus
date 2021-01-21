import cv2
import numpy as np
import matplotlib.pyplot as plt

# Info sheet with abbreviations and color codes.
# =============================================================================
# UE: Upper Engine
# LE: Lower Engine
# R: Reactor
# MB: MedBay
# S: Security
# E: Electrical
# C: Cafetaria
# Ad: Admin
# GbS: Gang boven Shields
# W: Weapons
# N: Navigation
# 
# HardWalls, cannot see or pass through
# Red
# 
# SoftWalls, can see through, not pass through
# Yellow
# 
# Vents; 
# UE-R Oranje
# LE-R Lichtgroen
# MB-S-E Groen
# C-GbS-Ad Hemselblauw
# W-N Blauw
# N-S Donkerblauw
#
# Short Tasks;
# Calibrate Distributer
# Chart Course
# Clean O2 Filter
# Divert Power (2 parts, one option and seven options)
# Stabilize Steering
# Unlock Manifolds
# Upload Data (2 parts, five options and one option)
# Prime Shields 
#
# Common tasks
#
# =============================================================================

HEIGHT = 137

def coordinates_walls_vents(image):
    """
    Function which requires an image with set colors to be interpertered
    Returns multiple lists of the coordinates for, in order;
    (0) Hard walls (red), (1) Soft walls (yellow), (2-7) Vent combi's locations
    (8) walkable surfaces
    """
    
    # BGR collors of objects relevant
    chardwall = [0,0,255] 
    csoftwall = [0,255,255]
    cvent_UE_R = [0,192,255]
    cvent_LE_R = [80,208,146]
    cvent_MB_S_E = [80,176,0]
    cvent_C_GbS_Ad = [240,176,0]
    cvent_W_N = [192,112,0]
    cvent_N_S = [96,32,0]
    cwalkable = [255,255,255]
    
    # The wall (red)
    X,Y = np.where(np.all(img==chardwall,axis=2))
    hardwall = np.column_stack((Y,X))
    
    # Impassable objects
    X,Y = np.where(np.all(img==csoftwall,axis=2))
    softwall = np.column_stack((Y,X))
    
    
    # Different vents
    X,Y = np.where(np.all(img==cvent_UE_R,axis=2))
    # Y = HEIGHT - Y
    vent_UE_R = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cvent_LE_R,axis=2))
    # Y = HEIGHT - Y
    vent_LE_R = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cvent_MB_S_E,axis=2))
    # Y = HEIGHT - Y
    vent_MB_S_E = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cvent_C_GbS_Ad,axis=2))
    # Y = HEIGHT - Y
    vent_C_GbS_Ad = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cvent_W_N,axis=2))
    # Y = HEIGHT - Y
    vent_W_N = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cvent_N_S,axis=2))
    # Y = HEIGHT - Y
    vent_N_S = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cwalkable,axis=2))
    # Y = HEIGHT - Y
    walkable = np.column_stack((Y,X))
    
    return hardwall, softwall, vent_UE_R, vent_LE_R, vent_MB_S_E, vent_C_GbS_Ad, vent_W_N, vent_N_S, walkable

def coordinates_short_tasks(image):
    """
    Function which requires an image with set colors to be interpertered
    Returns multiple lists of the coordinates for short tasks, in order;
    [0] calibrate_distributer, 
    [1] chart_course, 
    [2] clean_o2_filter, 
    [3][0] first part of divert_power, [3][1] second part of divert_power,
    [4] stabelize_steering
    [5] unlock_manifolds
    [6][0] first part of upload_data, [6][1] second part of upload data
    [7] prime_shields
    """
    
    
    # BGR colors of short tasks
    ccalibrate_distributer = [201,174,255]
    cchart_course = [202,174,255]
    cclean_o2_filter = [203,174,255]
    cdivert_power_1 = [204,174,255]
    cdivert_power_2 = [205,174,255]
    cstabelize_steering =  [206,174,255]
    cunlock_manifolds = [207,174,255]
    cupload_data_1 = [208,174,255]
    cupload_data_2 = [209,174,255]
    cprime_shields = [210,174,255]

    X,Y = np.where(np.all(img==ccalibrate_distributer,axis=2))
    calibrate_distributer = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cchart_course,axis=2))
    chart_course = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cclean_o2_filter,axis=2))
    clean_o2_filter = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cdivert_power_1,axis=2))
    divert_power_1 = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cdivert_power_2,axis=2))
    divert_power_2 = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cstabelize_steering,axis=2))
    stabelize_steering = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cunlock_manifolds,axis=2))
    unlock_manifolds = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cupload_data_1,axis=2))
    upload_data_1 = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cupload_data_2,axis=2))
    upload_data_2 = np.column_stack((Y,X))
    
    X,Y = np.where(np.all(img==cprime_shields,axis=2))
    prime_shields = np.column_stack((Y,X))

    return calibrate_distributer, chart_course, clean_o2_filter, [divert_power_1, divert_power_2], stabelize_steering, unlock_manifolds, [upload_data_1, upload_data_2], prime_shields  




# Get Image (put in your own filepath)
img = cv2.imread('C:/Users/bramm/Desktop/amongusmapmetvents2_shorttasks.png')

hardwalls = coordinates_walls_vents(img)[0]
obstructions = coordinates_walls_vents(img)[1]

vents = []
for i in range(2,8):
    vents.append(coordinates_walls_vents(img)[i])
    
shorttasks = []
for i in range(0,8):
    shorttasks.append(coordinates_short_tasks(img)[i])


np.save('hardwalls.npy', hardwalls)
np.save('obstructions.npy', obstructions)
np.save('vents.npy', vents)
np.save('shorttasks.npy', shorttasks)

import cv2
import numpy as np
import matplotlib.pyplot as plt


# Info sheet met afkortingen en wat welke kleur is op de afbeelding.
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
# =============================================================================

def coordinates(image):
    "Function which requires an image with set colors to be interpertered"
    "Returns multiple lists of the coordinates for, in order; "
    "(1) Hard walls (red), (2) Soft walls (yellow), (3-8) Vent combi's locations"
    "(9) walkable surfaces"
    
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
    

    # Get X and Y coordinates of all objects
    
    # The wall (red)
    X,Y = np.where(np.all(img==chardwall,axis=2))
    hardwall = np.column_stack((X,Y))
    
    # Impassable objects
    X,Y = np.where(np.all(img==csoftwall,axis=2))
    softwall = np.column_stack((X,Y))
    
    # Different vents
    X,Y = np.where(np.all(img==cvent_UE_R,axis=2))
    vent_UE_R = np.column_stack((X,Y))
    
    X,Y = np.where(np.all(img==cvent_LE_R,axis=2))
    vent_LE_R = np.column_stack((X,Y))
    
    X,Y = np.where(np.all(img==cvent_MB_S_E,axis=2))
    vent_MB_S_E = np.column_stack((X,Y))
    
    X,Y = np.where(np.all(img==cvent_C_GbS_Ad,axis=2))
    vent_C_GbS_Ad = np.column_stack((X,Y))
    
    X,Y = np.where(np.all(img==cvent_W_N,axis=2))
    vent_W_N = np.column_stack((X,Y))
    
    X,Y = np.where(np.all(img==cvent_N_S,axis=2))
    vent_N_S = np.column_stack((X,Y))
    
    X,Y = np.where(np.all(img==cwalkable,axis=2))
    walkable = np.column_stack((X,Y))
    
    
    return hardwall, softwall, vent_UE_R, vent_LE_R, vent_MB_S_E, vent_C_GbS_Ad, vent_W_N, vent_N_S, walkable


# Get Image (put in ur own filepath)
img = cv2.imread(r'C:\Users\bramm\Pictures\amongusmapmetvents.png')

hardwalls = coordinates(img)[0]
softwalls = coordinates(img)[1]


 


    

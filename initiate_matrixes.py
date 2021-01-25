#!/usr/bin/env python
# coding: utf-8

# In[13]:


import cv2
import numpy as np

#trust matrix does not change within a game, sus matrix does
#sus matrix starts with 1 - trust


#initiate matrixes should be run 1 time to create the very first set of matrixes in an iterated game, use update after that
def initiate_matrixes(number_players):
    trust = np.full((number_players,number_players), 0.5)
    
    for player in range(number_players):
        trust[player, player] = 1
    
    sus = 1 - trust
    
    np.save('social_matrixes/trust_0.npy', trust)
    np.save('social_matrixes/sus_0.npy', sus)

#this is done after each game
def update_trust(run, trust_matrix):
    run += 1
    trust = trust_matrix
    
    np.save(f'social_matrixes/trust_{run}.npy', trust)

#this is done within the game
def update_sus(run, game_finished, sus_matrix, person_1, person_2):
    sus = sus_matrix
    
    
    if game_finished:
        run += 1
        np.save(f'social_matrixes/sus_{run}.npy', sus)
        return
    
    return sus


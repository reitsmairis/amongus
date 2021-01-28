# !/usr/bin/env python
# coding: utf-8

# In[13]:

import numpy as np

# trust matrix does not change within a game, sus matrix does
# sus matrix starts with 1 - trust


# initiate matrices should be run 1 time to create the very first set of matrices in an iterated game, use update after that
def initiate_matrices(number_players):
    trust = np.full((number_players,number_players), 0.5)
    
    for player in range(number_players):
        trust[player, player] = 1
    
    sus = 1 - trust
    
    np.save('social_matrices/trust_0.npy', trust)

#this is done after each game
def update_trust(run, trust_matrix):
    run += 1
    trust = trust_matrix
    
    np.save(f'social_matrices/trust_{run}.npy', trust)

#this is done within the game and after the game to save the matrix
def update_sus(run, game_finished, sus_matrix, person_1, person_2):
    
    #kill changes sus score to 1
    if kill:
        
        return 1
    
    #vent changes sus score to 1
    if vent:
        
        return 1
    
    #changes sus score -0.01
    if walk:
        
        return -0.01
    
    #changes sus score -0.05
    if task:
        
        return -0.05
    
    if game_finished:
        run += 1
        np.save(f'social_matrices/sus_{run}.npy', sus_matrix)
        return
    
    return sus


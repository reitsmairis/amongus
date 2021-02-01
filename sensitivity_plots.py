import numpy as np
import matplotlib.pyplot as plt

# Set sensitivity values
samples_per_run = 32
amount_of_runs = 5
amount_of_strategies = 4

# Define sigma 3, 4, 5 and gamma 1, 2
social_list = [[0,-0.025,-0.05,-0.1,-0.2], [0,-0.005,-0.01,-0.02,-0.04], [0,0.00025,0.0005,0.001,0.002], [0,0.02,0.04,0.06,0.08], [0,-0.01,-0.02,-0.03,-0.04]]
social_value = ["Sigma 3","Sigma 4","Sigma 5","Gamma 1","Gamma 2"]
path = ["32x1 (32 groups with 1 game)", "1x32 (1 group with 32 games)"]

for iteration in path:
    if iteration == "32x1 (32 groups with 1 game)":
        title = "no iteration"
    else:
        title = "32 iterations"
        
    for l in range(len(social_list)):
        sigma_list = social_list[l]
        variable = social_value[l]
        
        for k in range(amount_of_strategies):
            strat1_win_list= []
            strat1_error_list = []
            
            for i in sigma_list:
                prev_value = 0
                win_list = []
                
                for j in range(samples_per_run, amount_of_runs*samples_per_run + samples_per_run ,samples_per_run):
                    tot_wins = np.load(f"C:/Users/bramm/Desktop/ABM Results/{variable}/{iteration}/win_matrices/win_matrix_{i}_{j}.npy")
                    act_win = tot_wins[k][1] - prev_value
                    prev_value = tot_wins[k][1]
                    win_list.append(act_win)
                 
                avg_wins_strat_1 = (amount_of_strategies/samples_per_run)*np.mean(win_list) 
                error_winst_strat_1 = (amount_of_strategies/samples_per_run)*np.std(win_list)/np.sqrt(amount_of_runs)
                
                strat1_win_list.append(avg_wins_strat_1)
                strat1_error_list.append(error_winst_strat_1)
                
            plt.plot(sigma_list, strat1_win_list, label = f"strat {k+1}")
            plt.fill_between(sigma_list, np.array(strat1_win_list) + np.array(strat1_error_list), np.array(strat1_win_list) - np.array(strat1_error_list), alpha = 0.2)
        
        
        plt.xlabel(f"Value of {variable}")
        plt.ylabel("Average wins")
        plt.title(f"Average winrate for the imposter for {variable}, with {title}")
        plt.ylim(0,0.6)
        plt.xlim(max(sigma_list), min(sigma_list))
        plt.legend()
        plt.show()

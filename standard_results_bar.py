import numpy as np
import matplotlib.pyplot as plt

# Set sensitivity values
samples_per_run = 32
amount_of_runs = 5
amount_of_strategies = 4
strat1_win_list= []
strat1_error_list = []

# Define the standard sigma 3, 4, 5 and gamma 1, 2
social_list = [[-0.1], [-0.01], [0.0005], [0.04], [-0.02]]
social_value = ["Sigma 3","Sigma 4","Sigma 5","Gamma 1","Gamma 2"]
path = ["32x1 (32 groups with 1 game)", "1x32 (1 group with 32 games)"]
strat_names = ["Aggressive/Active", "Aggressive/Passive", "Careful/Active", "Careful/Passive"]

for iteration in path:
    if iteration == "32x1 (32 groups with 1 game)":
        title = "no iteration"
        multiplyer = 1
    else:
        title = "32 iterations"
        multiplyer = 2
        
        
    for k in range(amount_of_strategies):
        win_list = []
        label_name = strat_names[k]
        
        for l in range(len(social_list)):
            sigma_list = social_list[l]
            variable = social_value[l]
        
            for i in sigma_list:
                                
                final_results = amount_of_runs*samples_per_run
                tot_wins = np.load(f"C:/Users/bramm/Desktop/ABM Results/{variable}/{iteration}/win_matrices/win_matrix_{i}_{final_results}.npy")
                act_win = tot_wins[k][1]
                win_list.append(act_win/(8*4))
                 
                
        strat1_win_list.append(np.mean(win_list))
        strat1_error_list.append(np.std(win_list)/(np.sqrt(5)))
     
        
# Transfrom for nice plotting
strats_final = []
error_final = []

for i in range(4):
    strats_final.append([strat1_win_list[i],strat1_win_list[i+4]])
    error_final.append([strat1_error_list[i],strat1_error_list[i+4]])
    
    

        
# Plot the bar
fig, ax = plt.subplots(1,1)

x_ticks_labels = strat_names

ax.grid(axis="y", linestyle = "-", zorder =0)
ax.bar(np.array([0.5,2,3.5,5]), strat1_win_list[0:4], align = "center", width = 0.5, yerr = strat1_error_list[0:4], label = "1 Iteration", ecolor='black', capsize=5, zorder = 3)
ax.bar(np.array([1,2.5,4,5.5]), strat1_win_list[4:8], align = "center", width = 0.5, yerr = strat1_error_list[4:8], label = "32 Iterations", ecolor='black', capsize=5, zorder = 3)

ax.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True) # labels along the bottom edge are off

plt.xlabel("Strategy")
plt.ylabel("Average winrate")
plt.title("Average winrate for the imposter standard settings")

ax.set_xticks([0.75, 2.25, 3.75, 5.25])

# Set ticks labels for x-axis
ax.set_xticklabels(x_ticks_labels, rotation=0, fontsize=8.5)

plt.ylim(0,0.51)
plt.xlim(0,6)
plt.legend()
plt.savefig("winrates", dpi = 500)
plt.show()

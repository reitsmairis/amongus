import numpy as np
import matplotlib.pyplot as plt

# Set sensitivity values
samples_per_run = 32
amount_of_runs = 5
amount_of_strategies = 4

# Define sigma 3, 4, 5 and gamma 1, 2
social_list = [[-0.1], [-0.01], [0.0005], [0.04], [-0.02]]
social_value = ["Sigma 3","Sigma 4","Sigma 5","Gamma 1","Gamma 2"]
strat_names = ["Aggressive/Active", "Aggressive/Passive", "Careful/Active", "Careful/Passive"]
path = ["32x1 (32 groups with 1 game)", "1x32 (1 group with 32 games)"]

for iteration in path:
    if iteration == "32x1 (32 groups with 1 game)":
        title = "no iteration"
    else:
        title = "32 iterations"

    trust_list2 = []
        
    for l in range(len(social_list)):
        sigma_list = social_list[l]
        variable = social_value[l]
        
        for k in range(amount_of_strategies):
            strat1_win_list= []
            strat1_error_list = []
            
            for i in sigma_list:
                prev_value = 0
                
                for q in range(0,amount_of_runs):
                    counter = 0
                    trust_list2.append(np.array([0.5,0.5,0.5,0.5,0.5]))
                    for j in range(samples_per_run*q+1, (q+1)*samples_per_run):
                        
                        counter +=1
                        trust = np.load(f"C:/Users/bramm/Desktop/ABM Results/{variable}/{iteration}/social_matrices/trust_{i}_{j}.npy")
                        act_trust = trust[0]
                        trust_list2.append(act_trust)
             
trust_AA = [[] for _ in range(samples_per_run)]
trust_AP = [[] for _ in range(samples_per_run)]
trust_CA = [[] for _ in range(samples_per_run)]
trust_CP = [[] for _ in range(samples_per_run)]                
             
for j in range(samples_per_run):
    for i in range(100):   
       index = i*samples_per_run + j
       trust_AA[j].append(trust_list2[index][0])
       trust_AP[j].append(trust_list2[index][1])
       trust_CA[j].append(trust_list2[index][2])
       trust_CP[j].append(trust_list2[index][3])

aa_final = [np.mean(trust_AA[i]) for i in range(32)]
aa_error = [1.96*np.std(trust_AA[i])/np.sqrt(100) for i in range(32)]

ap_final = [np.mean(trust_AP[i]) for i in range(32)]
ap_error = [1.96*np.std(trust_AP[i])/np.sqrt(100) for i in range(32)]

ca_final = [np.mean(trust_CA[i]) for i in range(32)]
ca_error = [1.96*np.std(trust_CA[i])/np.sqrt(100) for i in range(32)]

cp_final = [np.mean(trust_CP[i]) for i in range(32)]
cp_error = [1.96*np.std(trust_CP[i])/np.sqrt(100) for i in range(32)]
                            

plt.figure(1)  
plt.plot(range(32), aa_final, label = "Aggressive/Active")
plt.fill_between(range(32), np.array(aa_final) + np.array(aa_error), np.array(aa_final) - np.array(aa_error), alpha = 0.2)

plt.plot(range(32), ap_final, label = "Aggressive/Passive")
plt.fill_between(range(32), np.array(ap_final) + np.array(ap_error), np.array(ap_final) - np.array(ap_error), alpha = 0.2)

plt.plot(range(32), ca_final, label = "Careful/Active")
plt.fill_between(range(32), np.array(ca_final) + np.array(ca_error), np.array(ca_final) - np.array(ca_error), alpha = 0.2)

plt.plot(range(32), cp_final, label = "Careful/Passive")
plt.fill_between(range(32), np.array(cp_final) + np.array(cp_error), np.array(cp_final) - np.array(cp_error), alpha = 0.2)


plt.xlabel("Iteration")
plt.ylabel("Average trust score")
plt.title("Mean trust score")
plt.ylim(0.4,0.7)
plt.xlim(0,31)
plt.legend()
plt.savefig("Trust", dpi = 500)
plt.show()      
 

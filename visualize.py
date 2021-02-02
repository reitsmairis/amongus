#####################################
# if bresenham is not installed yet:
#import pip
#pip.main(['install', 'bresenham'])
#####################################

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

# Import the implemented classes
import IPython
import os
import sys

# Change stdout so we can ignore most prints etc.
orig_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

IPython.get_ipython().magic("run amongus_model.py")
sys.stdout = orig_stdout

# You can change this to whatever you want. Make sure to make the different types
# of agents distinguishable
def agent_portrayal(agent):
    if type(agent) == Crewmate:
        portrayal = {"Shape": "the_skeld\sprites\crewmate.png",
                    "Layer": 1,
                    "scale": 7}
        
    elif type(agent) == Imposter:
        portrayal = {"Shape": "the_skeld\sprites\imposter.png",
                    "Layer": 1,
                    "scale": 7}
        
    elif type(agent) == Wall:
        portrayal = {"Shape": "rect",
                    "Color": "black",
                    "Filled": "true",
                    "Layer": 1,
                    "w": 1,
                    "h": 1}
        
    elif type(agent) == Obstruction:
        portrayal = {"Shape": "rect",
                "Color": "gray",
                "Filled": "true",
                "Layer": 1,
                "w": 1,
                "h": 1}
        
    elif type(agent) == Vent:
        portrayal = {"Shape": "rect",
            "Color": "green",
            "Filled": "true",
            "Layer": 1,
            "scale": 2,
            "w": 1,
            "h": 1}
        
    elif type(agent) == ShortTask:
        portrayal = {"Shape": "rect",
            "Color": "orange",
            "Filled": "true",
            "Layer": 1,
            "scale": 2,
            "w": 1,
            "h": 1}
        
    elif type(agent) == CommonTask:
        portrayal = {"Shape": "rect",
            "Color": "blue",
            "Filled": "true",
            "Layer": 1,
            "scale": 2,
            "w": 1,
            "h": 1}
        
    elif type(agent) == Dead_crewmate:
        portrayal =  {"Shape": "the_skeld\sprites\dead.png",
            "Layer": 1,
            "scale": 4}
    
    return portrayal

# Iniate grid with right pixels
grid = CanvasGrid(agent_portrayal, 242, 138, 1815, 1035)

# fixed_parameters
starting_positions = [(130, 100), (121, 107), (139, 108), 
(130, 114), (123, 103), (137, 103), (136,112), (124,112)]

# varied parameters
number_of_crewmates = 4
num_tasks_crewmate = 4
injob_time = (70, 100)
impostor_cooldown = 214 # in-game value == 214
impostor_vents = True
just_killed_cooldown = 5
n_iterated_games = 1

# sus matrix parameters
sus_kill = np.inf
sus_vent = np.inf
sus_task = -.05
sus_group = -.01
sus_default = .0005

# trust parameters
gamma1 = 0.04
gamma2 = -0.02

# Create the server, and pass the grid and the graph
server = ModularServer(AmongUs,
                       [grid],
                       "AmongUs", 
                       {'map_name': 'the_skeld', 
                        'n_crew': 5,
                        'starting_positions': starting_positions,
                        'num_tasks_crewmate': num_tasks_crewmate,
                        'injob_time': injob_time,
                        'impostor_cooldown': impostor_cooldown,
                        'impostor_vents': impostor_vents,
                        'just_killed_cooldown': just_killed_cooldown,
                        'sus_kill': sus_kill,
                        'sus_vent': sus_vent,
                        'sus_task': sus_task,
                        'sus_group': sus_group,
                        'sus_default': sus_default,
                        'gamma1': gamma1,
                        'gamma2': gamma2,
                        'n_iterated_games': n_iterated_games
                        
                       }
                      )

server.port = 8527

server.launch()

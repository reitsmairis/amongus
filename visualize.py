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
IPython.get_ipython().magic("run amongus_model.ipynb")
sys.stdout = orig_stdout

# You can change this to whatever you want. Make sure to make the different types
# of agents distinguishable
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "green" if type(agent) is Crewmate else "green",
                 "Filled": "true",
                 "Layer": 1,
                 "r": .5}
    return portrayal

# Create a grid of 114 by 114 cells, and display it as 570 by 570 pixels
# grid = CanvasGrid(agent_portrayal, 114, 114, 570, 570)
grid = CanvasGrid(agent_portrayal, 60, 60, 500, 500)

# Create the server, and pass the grid and the graph
server = ModularServer(AmongUs,
                       [grid],
                       "AmongUs", 
                       {'map': 'map', 
                       'n_crew': 100,
                       'n_impo': 0})

server.port = 8522

server.launch()

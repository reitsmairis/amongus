from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import numpy as np
import pickle

from peripheral_functions.a_star_pathfinding import a_star

def euclidean(pos_a, pos_b):
    return ((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)**.5

class Crewmate(Agent):
    def __init__(self, unique_id, model, init_pos):
        super().__init__(unique_id, model)
        self.pos = init_pos
        self.path = []
        self.goallist = []
        self.injob = 0
        self.num_tasks = self.model.num_tasks_crewmate
        self.injob_time = self.model.injob_time
        self.index = self.model.index_agent
        self.make_tasks()
        self.done = False
        
    def make_tasks(self):
        short_tasks = self.model.short_tasks
        common_tasks = self.model.common_tasks
        
        # set 4 random tasks for Crewmate to execute (can still be same task multiple times)
        self.goallist = random.sample(list(short_tasks), self.num_tasks)
        
        # Import the common tasks
        self.goallist.append(common_tasks[0])
        self.fix_wires_tasks = [random.choice(common_tasks[1])]
        
        self.goallist.append([self.fix_wires_tasks[0][0]])
        
        # if it is a task with multiple locations/second part, replace by one of the coordinates from the first list 
        self.goallist = [[random.choice(self.goallist[index][0])] if len(x)>1 else x for index,x in enumerate(self.goallist)]
        
        # Turn list into list of tuples
        self.goallist = [tuple(self.goallist[index][0]) for index,y in enumerate(self.goallist)]
        
    def find_path(self):
              
        # Find shortest path and go to that task
        length1 = np.inf
        
        for t in self.goallist:
            path, length2 = a_star(self.pos, t, self.model.grid)
            
            if length2 < length1:
                length1 = length2
                shortest_path = path

        self.path = self.path + shortest_path
        
        
    def detect_agents(self):
        
        # Create empty list for agents
        agents_detected = []
        visible_area = self.model.vision_dict[self.pos]
        
        # Check all the visible cells
        for pos in visible_area:
            agents_on_tile = self.model.grid.get_neighbors(pos=pos, moore=True, radius=0, include_center=True)
            
            # If there's another player, append it to the detected list
            for agent in agents_on_tile:
                if type(agent) == Crewmate or type(agent) == Impostor:
                    agents_detected.append(agent)
                
                # If dead agent found, start voting prodecure
                if type(agent) == Dead_crewmate:
                    for dead_crewmate in self.model.dead_crewmates:
                        self.model.grid.remove_agent(dead_crewmate)
                        self.model.dead_crewmates.remove(dead_crewmate)
                    self.model.vote_off()
                    
        return agents_detected
    
    def die(self):
        self.model.new_agent(Dead_crewmate, self.pos)
        # automatically finishes tasks
        if not self.done:
            self.model.crew_done += 1
            self.model.tasks_counter += len(self.goallist)
            self.done = True
        self.model.remove_agent(self)
        # change sus score of dead agent to 0
        self.model.dead_players.append(self.index)

    def step(self):
        if self.path == []:
            if self.pos in self.goallist:
                self.goallist.remove(self.pos)
                self.injob = random.randint(self.injob_time[0], self.injob_time[1])
                self.model.tasks_counter += 1
                
            # if Task was task 3, add second part of task 3 to the task list
            if self.pos == tuple(self.model.short_tasks[3][0][0]):
                self.goallist.append(tuple(random.choice(self.model.short_tasks[3][1])))
            
            # if Task was task 6, add second part of task 6 to the task list
            elif self.pos in self.model.short_tasks[6][0]:
                self.goallist.append(tuple(self.model.short_tasks[6][1][0]))
                
            # if Task was common task Fix Wires, append next one
            elif self.pos in np.array(self.fix_wires_tasks):
                for i in range(2):
                    if self.pos == tuple(self.fix_wires_tasks[0][i]):
                        self.goallist.append(tuple(self.fix_wires_tasks[0][i+1]))
                        
            # if all tasks are done, go to middle and run around
            if len(self.goallist) == 0:
                self.goallist = [(130, 100), (121, 107), (139, 108),(130, 114)]
                if not self.done:
                    self.model.crew_done += 1
                    self.done = True
                
            self.find_path()

        elif self.path != []:
            # if crewmate is on cooldown for doing a job, don't move
            if self.injob > 0:
                self.injob -= 1
            else:
                self.model.grid.move_agent(self, self.path.pop()) 

        # find and loop over all detected impostors and crewmates in vision radius
        task_list = [(101, 55), (237,83), (167,85), (83, 58), (170,18), 
                     (197,42), (239,75), (7, 88), (149, 63), (158, 18), 
                     (78, 58), (177, 20), (168, 52), (125, 50), (91, 55), 
                     (140, 63), (47, 73), (220, 77), (106, 132)]
        agents_detected = self.detect_agents()
        for agent in agents_detected:
            if type(agent) == Impostor and agent.just_killed > 0:
                self.model.sus_matrix[self.index, agent.index] += self.model.sus_kill
                
            if agent.pos in self.model.vents:
                self.model.sus_matrix[self.index, agent.index] += self.model.sus_vent
                
            if agent.pos in task_list:
                self.model.sus_matrix[self.index, agent.index] += self.model.sus_task
            
            else:
                self.model.sus_matrix[self.index, agent.index] += self.model.sus_group
            
class Impostor(Agent):
    def __init__(self, unique_id, model, init_pos):
        super().__init__(unique_id, model)
        self.pos = init_pos
        self.vents_enabled = self.model.impostor_vents
        # tactic can be active or passive
        self.tactic = self.model.impostor_tactic
        # behavior can be careful or agressive
        self.behavior = self.model.impostor_behavior
        self.cooldown = self.model.impostor_cooldown
        self.just_killed = 0
        self.index = self.model.index_agent
        # impostor needs initial goal
        self.goals = [random.choice(self.model.all_tasks).pos]
        self.find_path()

    def find_path(self):
        if len(self.goals) == 0:
            # select random task as goal
            self.goals = [random.choice(self.model.all_tasks).pos]
        
        else:
            goal = self.goals.pop()
            best_path, best_score = a_star(self.pos, goal, self.model.grid)

            if self.vents_enabled:
                for vent in self.model.vents:
                    vent_in = vent.pos_a
                    vent_out = vent.pos_b
                    guess_vent_path = euclidean(self.pos, vent_in) + euclidean(vent_out, goal)

                    if guess_vent_path < best_score:
                        vent_path_in, vent_score_in = a_star(self.pos, vent_in, self.model.grid)
                        vent_path_out, vent_score_out = a_star(vent_out, goal, self.model.grid)
                        vent_path = vent_path_out + vent_path_in
                        vent_score = vent_score_in + vent_score_out
    
                        if vent_score < best_score:
                            best_score = vent_score
                            best_path = vent_path

            self.path = best_path

    def detect_crewmates(self):
        crewmates_detected = []
        visible_area = self.model.vision_dict[self.pos]
        for pos in visible_area:
            agents_on_tile = self.model.grid.get_neighbors(pos=pos, moore=True, radius=0, include_center=True)
            for agent in agents_on_tile:
                if type(agent) == Crewmate:
                    crewmates_detected.append(agent)
        return crewmates_detected

    def step(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            
        if self.just_killed > 0:
            self.just_killed -= 1
            
        if self.path == []:
            if self.tactic == 'active':
                self.find_path()
            elif self.tactic == 'passive' and self.just_killed > 0:
                self.find_path()

        crewmates_detected = self.detect_crewmates()

        for crewmate in crewmates_detected:
            if self.cooldown == 0 and euclidean(crewmate.pos, self.pos) <= 6:
                # kill a crewmate immediately
                if self.behavior == 'aggressive':
                    crewmate.die()
                    self.cooldown = self.model.impostor_cooldown
                    self.just_killed = self.model.just_killed_cooldown

                # wait a couple of steps before killing
                elif self.behavior == 'careful':
                    self.waiting_countdown = 5
                    self.behavior = 'waiting'
                elif self.behavior == 'waiting':
                    if self.waiting_countdown > 0:
                        self.waiting_countdown -= 1
                    else:
                        # only kill if there is 1 crewmate in sight
                        if len(self.detect_crewmates()) == 1:
                            crewmate.die()
                            self.cooldown = self.model.impostor_cooldown
                            self.just_killed = self.model.just_killed_cooldown
                            self.behavior = 'careful'
                        else:
                            self.behavior = 'careful'
                
        if self.path != []:
            self.model.grid.move_agent(self, self.path.pop())   
                       
class Dead_crewmate(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
    
class Wall(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class Obstruction(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class Vent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos_a = pos
        self.pos_b = self.model.vents_dict[pos]

class ShortTask(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        
class CommonTask(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random
import numpy as np
import pickle
from IPython.display import clear_output

from agents import *

class AmongUs(Model):
    def __init__(self, map_name, n_crew, starting_positions, 
    num_tasks_crewmate=4, injob_time=(70,100), impostor_cooldown=214, impostor_vents=True,
    just_killed_cooldown=5, sus_kill=np.inf, sus_vent=np.inf, sus_task=-.1, sus_group=-.01,
    sus_default=.0005, gamma1= 0.04, gamma2= -0.02,n_iterated_games = 1, var_name='', 
    data_path='generated_data/unsorted'):
        super().__init__()
               
        # changable parameters
        self.injob_time = injob_time
        self.num_tasks_crewmate = num_tasks_crewmate
        self.starting_positions = starting_positions
        self.impostor_tactic = None
        self.impostor_behavior = None
        self.impostor_cooldown = impostor_cooldown
        self.impostor_vents = impostor_vents
        self.just_killed_cooldown = just_killed_cooldown
        self.n_iterated_games = n_iterated_games
        
        # changable sus matrix parameters
        self.sus_kill = sus_kill
        self.sus_vent = sus_vent
        self.sus_task = sus_task
        self.sus_group = sus_group
        self.sus_default = sus_default
        
        #changable trust matrix parameters
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        
        # reset to 0 every game for indexing which agent is which in social matrices
        self.index_agent = 0
        
        # generate grid
        self.height = 138
        self.width = 242
        self.grid = MultiGrid(self.width, self.height, torus=True)

        # generate map
        self.generate_map(map_name)
        
        # generate tasks
        self.generate_tasks(map_name)
        
        # load vision dict for impostors
        self.vision_dict = np.load('the_skeld/vision_dict.pkl', allow_pickle=True)
        
        # create schedulers for agents
        self.schedule_Crewmate = RandomActivation(self)
        self.schedule_Impostor = RandomActivation(self)
        
        # initialize agents
        self.n_crew = n_crew
        self.n_impo = 1
        self.n_run = 0
        self.dead_players = []
        self.tasks_counter = 0
        self.crew_done = 0
        self.dead_crewmates = []
        self.respawn_players()
        
        # Generate trust and sus matrix
        n_players = n_crew + self.n_impo
        self.sus_matrix = np.full((n_players, n_players), .5)
        self.trust_list = np.load(f'{data_path}/social_matrices/trust_0.npy', allow_pickle=True)
        self.data_path = data_path
        self.var_name = var_name
        
    def generate_map(self, map_name):
        hard_walls = np.load(f'{map_name}/hardwalls.npy')
        vents = np.load(f'{map_name}/vents.npy', allow_pickle=True)
        obstructions = np.load(f'{map_name}/obstructions.npy', allow_pickle=True)
        
        for coord in hard_walls:
            self.new_agent(Wall, tuple(coord))

        self.vents_dict = {}
        self.vents = []

        for connection in vents:
            connection = connection.tolist()
            self.vents_dict[tuple(connection[0])] = tuple(connection[1])
            self.vents_dict[tuple(connection[1])] = tuple(connection[0]) 
            
            if len(connection) == 3:
                self.vents_dict[tuple(connection[0])] = tuple(connection[2])
                self.vents_dict[tuple(connection[1])] = tuple(connection[2])
                self.vents_dict[tuple(connection[2])] = tuple(connection[0])
                self.vents_dict[tuple(connection[2])] = tuple(connection[1])
            
        for coord in self.vents_dict:
            self.new_agent(Vent, tuple(coord))
        
        for coord in obstructions:
            self.new_agent(Obstruction, tuple(coord))
    
    def generate_tasks(self, map_name):
        # load the image + coordinates of the short tasks and common tasks
        short_tasks = np.load(f'{map_name}/shorttasks.npy', allow_pickle=True)
        common_tasks = np.load(f'{map_name}/commontasks.npy', allow_pickle=True)
        
        self.short_tasks = short_tasks
        self.s_tasks = []
        
        self.common_tasks = common_tasks
        self.c_tasks = []

        self.all_tasks = []

        # load all the short_tasks into the map (all possible task locations), first create tuples
        for i in range(len(short_tasks)):
            if i == 3:
                self.new_agent(ShortTask, tuple(short_tasks[i][0][0]))
                for parttwo in range(8):
                    self.new_agent(ShortTask, tuple(short_tasks[i][1][parttwo]))
            elif i == 6:
                for partone in range(5):
                    self.new_agent(ShortTask, tuple(short_tasks[i][0][partone]))
                self.new_agent(ShortTask, tuple(short_tasks[i][1][0]))
        
            else:
                self.new_agent(ShortTask, tuple(short_tasks[i][0]))
        
        # Do the same for common tasks
        self.new_agent(CommonTask, tuple(common_tasks[0][0]))
        for i in range(len(common_tasks[1])):
            self.new_agent(CommonTask, tuple(common_tasks[1][i][0]))

    def respawn_players(self):
        for crewmate in self.schedule_Crewmate.agents:
            self.remove_agent(crewmate)
        for impostor in self.schedule_Impostor.agents:
            self.remove_agent(impostor)
            
        for dead_crewmate in self.dead_crewmates:
            self.grid.remove_agent(dead_crewmate)
            self.dead_crewmates.remove(dead_crewmate)    
        
        self.activated_agents = []     
        self.crew_done = 0
        
        # Assign agent to impostor
        impostor_index = self.n_run % 4
        
        if impostor_index == 0:
            self.impostor_tactic = 'active'
            self.impostor_behavior = 'aggressive'
        if impostor_index == 1:
            self.impostor_tactic = 'passive'
            self.impostor_behavior = 'aggressive'
        if impostor_index == 2:
            self.impostor_tactic = 'active'
            self.impostor_behavior = 'careful'
        if impostor_index == 3:
            self.impostor_tactic = 'passive'
            self.impostor_behavior = 'careful'
        
        
        for i in range(self.n_crew + self.n_impo):
            if i == impostor_index: 
                self.new_agent(Impostor, random.choice(self.starting_positions))
            else:
                self.new_agent(Crewmate, random.choice(self.starting_positions))

    def new_agent(self, agent_type, pos):
        '''
        Method that creates a new agent, and adds it to the correct scheduler.
        '''
        agent = agent_type(self.next_id(), self, pos)

        self.grid.place_agent(agent, pos)

        if agent_type == Crewmate or agent_type == Impostor:
            getattr(self, f'schedule_{agent_type.__name__}').add(agent)
            agent.injob_time = self.injob_time
            agent.num_tasks = self.num_tasks_crewmate
            self.activated_agents.append(agent)
            self.index_agent += 1
            
        if agent_type == Dead_crewmate:
            self.dead_crewmates.append(agent)
            
        if agent_type == Vent:
            self.vents.append(agent)
        
        if agent_type == ShortTask:
            self.s_tasks.append(agent)
            self.all_tasks.append(agent)
        
        if agent_type == CommonTask:
            self.c_tasks.append(agent)
            self.all_tasks.append(agent)
            
    def remove_agent(self, agent):
        '''
        Method that removes an agent from the grid and the correct scheduler.
        '''
        self.grid.remove_agent(agent)
        getattr(self, f'schedule_{type(agent).__name__}').remove(agent)
        
        
    def vote_off(self):
        '''
        Method that determines which player gets voted off. 
        Player with highest trust*sus score gets voted off, if difference is significant with number two value
        '''
        
        # Sus matrix; row (R) is what player R thinks of players (C1, C2, C3, C4, C5)
        for player in self.dead_players:
            self.sus_matrix[player,:] = -np.inf
            self.sus_matrix[:,player] = -np.inf
            
        for i in range(len(self.sus_matrix)):
            self.sus_matrix[i, i] = -np.inf
            
        # Create vote_matrix (value between 0 and 1)
        vote_matrix = self.sus_matrix.copy()
        for i in range(len(vote_matrix)):
            for j in range(len(vote_matrix[i])):
                vote_matrix[i][j] = .5 + .5*np.tanh(vote_matrix[i][j])
  
        # Check trust matrix and sus matrux to determine who gets voted off
        trust_list = self.trust_list
        trust_score = trust_list.copy()
        total_scores = trust_score @ vote_matrix
        
        # Determine who is voted out
        voted_out = random.choice(np.argwhere(total_scores[0] == np.amax(total_scores[0])))[0]
        self.dead_players.append(voted_out)
        
        # remove agent form game and activated agent list
        self.remove_agent(self.activated_agents[voted_out])
        
        # finish task of voted out agent
        if type(self.activated_agents[voted_out]) == Crewmate:
            if not self.activated_agents[voted_out].done:
                self.crew_done += 1
                self.activated_agents[voted_out].done = True
        
        # Change trust matrix depenending on correct choices, trust increases for correct sus, decreases for wrong sus (max with factor 0.05)
        for player_trust in range(len(self.trust_list[0])):
            
            vote_list = vote_matrix[player_trust]
            # Determine who the player voted for
            player_vote = np.argmax(vote_list, axis = 0)
            
             # Check if the vote was correct, lower or increase trust value accordingly
            if type(self.activated_agents[player_vote]) == Impostor:
                self.trust_list[0][player_trust] += self.gamma1
                round(self.trust_list[0][player_trust], 3)
                
                if self.trust_list[0][player_trust] > 1:
                    self.trust_list[0][player_trust] = 1
                
            if type(self.activated_agents[player_vote]) == Crewmate:
                self.trust_list[0][player_trust] += self.gamma2
                round(self.trust_list[0][player_trust], 3)
                
                if self.trust_list[0][player_trust] < 0:
                    self.trust_list[0][player_trust] = 0
        
        # set players to base
        for i in range(len(self.activated_agents)):
            if i not in self.dead_players:
                self.activated_agents[i].path = [(130, 100)]
                for impostor in self.schedule_Impostor.agents:
                    impostor.cooldown = self.impostor_cooldown
                    impostor.just_killed = 0
        
        
    def step(self):
        '''
        Method that steps every agent. 
        
        Prevents applying step on new agents by creating a local list.
        '''

        self.schedule_Crewmate.step()
        self.schedule_Impostor.step()

        # update sus matrix every step
        self.sus_matrix += self.sus_default
        

    def play_match(self, iterations=0, match_num=0):
        '''
        Method that runs a single match.
        '''
        #reset to 0 every game for indexing which agent is which in social matrices
        self.index_agent = 0
        self.dead_players = []
        self.crew_done = 0
        self.tasks_counter = 0
        
        n_players = self.n_crew + self.n_impo
        self.sus_matrix = np.full((n_players, n_players), .5)
        #make sure the trust matrix is reset after 'new players' enter a game
        if self.n_run % self.n_iterated_games == 0:
            self.trust_list = np.load(f'{self.data_path}/social_matrices/trust_0.npy', allow_pickle=True)
        
        self.respawn_players()
        i = 1
        while len(self.schedule_Crewmate.agents) > self.n_impo and len(self.schedule_Impostor.agents) > 0 and self.crew_done != self.n_crew:
            print(f'Match: {match_num+1}/{iterations}')
            print(f' Step: {i}')
            clear_output(wait=True)
            i += 1
            self.step()
        
        print(f'Ended at iteration: {i}')
        print(f'Number of tasks completed: {self.tasks_counter}')
        print(f'Number of crewmates finished: {self.crew_done}')
        #save the trust matrix to be loaded later
        self.n_run += 1
        np.save(f'{self.data_path}/social_matrices/trust_{self.var_name}_{self.n_run}.npy', self.trust_list)
        
        # load previous wins
        self.win_matrix = np.load(f'{self.data_path}/win_matrices/win_matrix_{self.var_name}_{self.n_run - 1}.npy', allow_pickle=True)
        
        # crewmates win
        if len(self.schedule_Impostor.agents) == 0 or self.crew_done == self.n_crew:
            print('The crewmates won!')
            for player in self.activated_agents:
                if type(player) != Impostor:
                    self.win_matrix[player.index, 0] += 1
        
        # impostor wins
        else:
            print('The impostor won!')
            impostor = self.schedule_Impostor.agents[0]
            self.win_matrix[impostor.index, 1] += 1
        
        # add wins
        np.save(f'{self.data_path}/win_matrices/win_matrix_{self.var_name}_{self.n_run}.npy', self.win_matrix)
        
        
        # NEW save thins
        iteration_data = np.load(f'{self.data_path}/misc_data/iteration_data.npy', allow_pickle=True)
        iteration_data = np.append(iteration_data, i)
        np.save(f'{self.data_path}/misc_data/iteration_data.npy', iteration_data)

        tasks_data = np.load(f'{self.data_path}/misc_data/tasks_data.npy', allow_pickle=True)
        tasks_data = np.append(tasks_data, self.tasks_counter)
        np.save(f'{self.data_path}/misc_data/tasks_data.npy', tasks_data)

        crewmates_done_data = np.load(f'{self.data_path}/misc_data/crewmates_done_data.npy', allow_pickle=True)
        crewmates_done_data = np.append(crewmates_done_data, self.crew_done)
        np.save(f'{self.data_path}/misc_data/crewmates_done_data.npy', crewmates_done_data)

        win_data = np.load(f'{self.data_path}/misc_data/win_data.npy', allow_pickle=True)
        if len(self.schedule_Impostor.agents) == 0 or self.crew_done == self.n_crew:
            win_data = np.append(win_data, 0) 
        else:
            win_data = np.append(win_data, 1)
        np.save(f'{self.data_path}/misc_data/win_data.npy', win_data)

        dead_data = np.load(f'{self.data_path}/misc_data/dead_data.npy', allow_pickle=True)
        dead_data = np.append(dead_data, len(self.dead_players))
        np.save(f'{self.data_path}/misc_data/dead_data.npy', dead_data)
        
    def run(self, iterations):
        '''
        Method that runs multiple matches.
        '''
        for match_num in range(iterations):
            self.play_match(iterations, match_num)
            clear_output(wait=True)
def a_star(start, finish, grid):
    
    finished = False
    open_set = {start}
    closed_set = set()
    path = {}
    
    #function to calculate the distance between a node and the finish in order to calculate the costs
    def distance(node1, node2):
        x, y = node1
        x_finish, y_finish = node2
        dist = ((x - x_finish)**2 + (y - y_finish)**2)**.5
        return dist
    
    #this score is the absolute score from the start point up untill the current point
    score_tobegin = {}
    score_tobegin[start] = 0
    
    #guess scores scores the estimater score from a point to the finish
    guess_scores = {}
    guess_scores[start] = distance(start, finish)
    
    
    while open_set:
        
        guess = 1000000
        #the current node is the lowest scoring guess point, which is in the guess_scores
        for node in open_set:
            if guess_scores[node] < guess:
                guess = guess_scores[node]
                bestnode = node
        
        current_node = bestnode
        
        #find neighbors of current best node and check which step is the best improvement
        neighbors = grid.get_neighborhood(current_node, True, False, 1)
        
        open_set.remove(current_node)
        closed_set.add(current_node)
        for neighbor in neighbors:
            
            #first check of this step not an obstacle SO CHANGE THE FALSE STATEMENT TO CHECK FOR OBSTACLE
            if not grid.is_cell_empty(neighbor):
                if not neighbor == finish:
                    closed_set.add(neighbor)
                    continue
                
            #check if the step is in the closed list
            if neighbor in closed_set:
                continue
            
            #calculate the cost of travelling to the neighbor from the begin and estimate cost to the finish
            score_from_begin = score_tobegin[current_node] + 1
            score_to_finish = distance(neighbor, finish)
            total_score = score_from_begin + score_to_finish
            
            #check if the point is already int the open set, if so check if the path is slower, if so continue with another neighbor
            if neighbor in open_set:
                if score_tobegin[neighbor] < score_from_begin:
                    continue
                
            open_set.add(neighbor)
            score_tobegin[neighbor] = score_from_begin
            guess_scores[neighbor] = total_score
            path[neighbor] = current_node
            
            if neighbor == finish:
                open_set = {}
                final_score = total_score
                break
            
    final_path = [finish]
    current = finish
    while current != start:
        current = path[current]
        final_path.append(current)
    
    final_path.pop(-1)

    return final_path, final_score
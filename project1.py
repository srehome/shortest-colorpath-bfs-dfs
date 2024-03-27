#import deque to use as a stack or queue
from collections import deque

#create the colorgrid game board
grid_colors = [
    ["or", "or", "or", "wh"],
    ["pi", "or", "pu", "gr"],
    ["or", "pu", "pi", "bl"],
    ["wh", "pu", "pi", "gr"]
]

grid_colors2 = [
    ["or", "or", "or", "or", "or", "or", "or", "wh"],
    ["pi", "or", "pu", "gr", "pi", "or", "pu", "gr"],
    ["or", "pu", "bl", "bl", "or", "pu", "gr", "bl"],
    ["or", "pu", "pi", "gr", "bl", "pu", "pi", "gr"],
    ["or", "or", "or", "or", "pu", "or", "or", "gr"],
    ["gr", "gr", "pu", "pu", "or", "or", "pu", "gr"],
    ["gr", "pu", "gr", "gr", "or", "pu", "gr", "bl"],
    ["wh", "or", "or", "or", "gr", "gr", "pi", "gr"]
]

grid_colors3 = [
    ["or", "or", "or", "or", "or", "or", "or", "or", "or", "or", "or", "wh"],
    ["pi", "or", "pu", "gr", "pi", "or", "or", "gr", "bl", "pu", "pu", "gr"],
    ["or", "pu", "pu", "pu", "or", "pu", "pu", "pu", "pu", "gr", "gr", "bl"],
    ["or", "pu", "or", "bl", "pu", "pu", "pi", "pi", "pi", "gr", "gr", "gr"],
    ["or", "or", "pu", "or", "pu", "pu", "pi", "or", "or", "or", "gr", "gr"],
    ["gr", "pu", "or", "pi", "or", "or", "pu", "pu", "gr", "gr", "gr", "bl"],
    ["or", "pu", "or", "gr", "or", "or", "pi", "gr", "pu", "gr", "bl", "bl"],
    ["bl", "or", "pu", "or", "gr", "gr", "bl", "gr", "pu", "pu", "bl", "or"],
    ["wh", "or", "pu", "gr", "gr", "gr", "pi", "gr", "pu", "pu", "bl", "or"],
    ["or", "pu", "gr", "or", "pu", "gr", "gr", "gr", "pu", "pu", "bl", "or"],
    ["pu", "or", "gr", "or", "pu", "gr", "pi", "bl", "pu", "pu", "bl", "or"],
    ["wh", "gr", "or", "or", "gr", "gr", "pi", "bl", "pu", "pu", "bl", "or"],
]

grid_length = 8
start_state = (0, grid_length-1)  #top right
goal_state = (grid_length-1, 0)  #bottom left


def move(current_color, next_color):
    if current_color == 'wh' or next_color == 'wh': #lets it go from white (start/goal) to any color and vice versa
        return True
    else: #keeps it on the same color path
        return current_color == next_color

def get_neighbors(x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] #directions it can move
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_length and 0 <= ny < grid_length:         #if square is within the bounds of the grid
            neighbors.append((nx, ny))
    return neighbors

def in_frontier(queue, node):
    for item in queue:
        if item[0] == node:
            return True
    return False

def bfs(start, goal, grid_colors):
    start_color = grid_colors[start[0]][start[1]]   #should be white
    queue = deque([(start, [start], start_color)])  #add first item in queue (square coordinates, list of path coordinates, color)
    bfs_visited = set()                             #unordered set to check for visited squares

    paths = []

    while queue:                                        #while queue isn't empty
        node, bfs_path, current_color = queue.popleft() #remove the front node from queue
        bfs_visited.add(node)                           #add node coordinates to visited

        for neighbor in get_neighbors(*node):           #for every child-node of front-node
            next_color = grid_colors[neighbor[0]][neighbor[1]]                  #get color of neighbor
            #if not in visited, not in queue and color allowed
            if neighbor not in bfs_visited and not in_frontier(queue, neighbor) and move(current_color, next_color):
                if neighbor == goal:                                            #if child-node is goal
                    paths.append((current_color, bfs_path + [neighbor]))        #return path to goal
                else:
                    queue.append((neighbor, bfs_path + [neighbor], next_color))     #otherwise add child-node to queue

    return paths  #return paths

def dfs(start, goal, grid_colors):
    current_color = grid_colors[start[0]][start[1]]
    stack = deque([(start, [start], current_color)])
    visited = set()
    
    paths = []
    while stack:                                        #while stack isn't empty
        node, dfs_path, current_color = stack.pop()     #remove the top node from stack

        if node == goal:                                #if node is goal
            paths.append((grid_colors[dfs_path[1][0]][dfs_path[1][1]], dfs_path))       #add path to paths
            node, dfs_path, current_color = stack.pop()                                 #get next node to search other colors

        visited.add(node)                               #add node to visited
        for neighbor in get_neighbors(*node):           #expand the node
            next_color = grid_colors[neighbor[0]][neighbor[1]]          #get neighbor node color
            #check if not in visited, not on stack, and color allowed
            if neighbor not in visited and not in_frontier(stack, neighbor) and move(current_color, next_color):
                stack.append((neighbor, dfs_path + [neighbor], next_color))

    return paths    #return paths
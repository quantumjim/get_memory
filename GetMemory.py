# This package is made from the functions in the ASCII prototype of the game
# https://trinket.io/python3/cab3091236
# As well as an additional function to integrate WorldBuilder

import warnings
warnings.filterwarnings("ignore")

from qiskit import *
import copy
import random
from WorldBuilder import *


wall =     'w'
path =     'p'
player =   's'
money =    'm'
exit =     'e'


rho = 0.2
r = 7

def print_intro():
  
    print('\nWelcome to the labyrinth')
    print('\nYou are represented by the character '+player)
    print('\nThe exit is represented by '+exit)
    input('\nPress Enter to get started\n')
    
def print_outro(wealth):
  
    print('\n'*1001)
  
    print('\nYou have left the labyrinth. Time to calculate your score')
    print('\nScore from currency = 0 × wealth = 0')
    print('\nScore from life = 0 × (the lessons you learned along the way) = ?')

    
def print_maze ( maze, player_pos ):
    
    print('\n'*100)
    
    temp = copy.deepcopy(maze)
    
    temp[ tuple(player_pos) ] = player
    
    size = max(maze)
    for y in range(-1,size[1]+1):
        line = ''
        for x in range(-1,size[0]+1):
            line += temp[x,y]
        print(line)
        
        
def get_empties(maze,y=None):
  
    empties = []
    
    size = max(maze)
    if y is None:
        for y in range(-1,size[1]+1):
            for x in range(-1,size[0]+1):
                if maze[x,y] == path:
                    empties.append( [x,y] )
    else:
        empties = []
        for x in range(-1,size[0]+1):
            if maze[x,y]==path:
                empties.append( [x,y] )
    
    return empties
 

        
def generate_maze(L,k):
  
    shots = L[0]*L[1]
    
    result = execute(QuantumCircuit.from_qasm_str('include "qelib1.inc";qreg q[1];creg c[1];h q[0];measure q-> c;'),Aer.get_backend('qasm_simulator'),shots=shots,memory=True).result().get_memory()
    
    maze = {}
    
    for j in range(-1,k*L[0]+1):
        maze[j,-1] = wall
        maze[j,k*L[1]] = wall
    
    for j in range(-1,k*L[1]+1):
        maze[-1,j] = wall
        maze[k*L[0],j] = wall
    
    for y in range(L[1]):
        for x in range(L[0]):
            for xx in range(k):
                for yy in range(k):
                    w = ( result[ x*L[1] + y ]=='1' and xx==yy ) or ( result[ x*L[1] + y ]=='0' and xx==(k-1-yy) )
                    maze[k*x+xx,k*y+yy] = w*wall + path*(not w)
  
    empties = get_empties(maze)
    money_pos = random.choices( empties, k=int(rho*shots) )
    for pos in money_pos:
        maze[ tuple(pos) ] = money
  
    empties = get_empties(maze,y=k*L[1]-1)
    exit_pos = random.choice(empties)
    maze[ tuple(exit_pos) ] = exit
  
  
    return maze
        
def move ( m, player_pos, maze ):
    
    temp_pos = copy.deepcopy( player_pos )
    
    if m in ['t','T']:
        
        empties = get_empties(maze)
        
        choosing = True
        while choosing:
            temp_pos = random.choice(empties)
            if (temp_pos[0]<player_pos[0]+r) and (temp_pos[0]>player_pos[0]-r) and (temp_pos[1]<player_pos[1]+r) and (temp_pos[1]>player_pos[1]-r) :
                player_pos = temp_pos
                choosing = False
    else:   
        
        if m in ['w','W']:
            temp_pos[1] -= 1
        if m in ['s','S']:
            temp_pos[1] += 1
        if m in ['a','A']:
            temp_pos[0] -= 1
        if m in ['d','D']:
            temp_pos[0] += 1

        if maze[ tuple(temp_pos) ]!=wall:
            player_pos = temp_pos
        
    return player_pos


def make_world():
    # This ties together the above functions and functions from WorldBuilder using a fixed set of parameters to make a world
    # nothing returned, it's saved as heightmap.txt instead

    
    map_size = [270,270]
    period = [3,3]
    k = 15
    
    n = 10
    
    samples = 300
    
    
    start = time.time()
    
    L = get_L(n)
    Z = mountain_seed(L,[int(L[0]/2),int(L[1]/2)],10)
    Z, grid = quantum_tartan(Z,0.07)
    
    print('\nThe quantum result is now being expanded into',samples,'patterns...')
    starts = time.time()
    
    tartans = []
    for j in range(samples):
        randZ,_ =  shuffle_height(Z,grid)
        randZ = rotate_height(randZ,random.random())
        tartans.append( randZ )
    
    ends = time.time()
    print('Generation of',samples,'patterns took',int(ends-starts),'seconds')

    print('\nThe quantum patterns are now being compiled into a map...')

    Z = islands(map_size,period,tartans)
    maze = generate_maze( [int(map_size[0]/k),int(map_size[1]/k)], k )


    size = max(maze)

    for x in range(-1,size[0]+1):
        for y in range(-1,size[1]+1):
            if maze[x,y]=='w':
                for (xx,yy) in [(x,y),(x+1,y),(x,y+1),(x-1,y),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)]:
                    if (xx,yy) in Z:
                        if Z[xx,yy]>0:
                            Z[xx,yy] = -Z[xx,yy]


    with open('heightmap.txt','w') as file:
        file.write(str(Z))
        
        end = time.time()
        print('\nTotal map generation took',int(end-start),'seconds')
        print('\nAlmost there!')

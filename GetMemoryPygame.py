# This package is just one function, which ties together functions from WorldBuilder and GetMemoryPrototype using a fixed set of parameters to make a world
# nothing returned, it's saved as heightmap.txt instead

from WorldBuilder import *
from GetMemoryPrototype import *

def make_world():

    samples = 500

    start = time.time()
    
    n = 10
    L = get_L(n)
    Z = mountain_seed(L,[int(L[0]/2),int(L[1]/2)],10)
    Z, grid = quantum_tartan(Z,0.07)

    print('\nThe quantum result is now being expanded into',samples,'patterns...')
    starts = time.time()

    samples = 500
    tartans = []
    for j in range(samples):
        randZ,_ =  shuffle_height(Z,grid)
        randZ = rotate_height(randZ,random.random())
        tartans.append( randZ )

    ends = time.time()
    print('Generation of',samples,'patterns took',int(ends-starts),'seconds')

    print('\nThe quantum patterns are now being compiled into a map...')

    map_size = [514,514]
    period = [3,3]

    Z = islands(map_size,period,tartans)


    k = 16
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
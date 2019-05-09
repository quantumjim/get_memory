# This package is made from the functions in my article on making terrain maps with quantum computing
# https://medium.com/qiskit/creating-infinite-worlds-with-quantum-computing-5e998e6d21c2

from PIL import Image

try:
    from IPython.display import display
except:
    pass

import numpy as np

import random

from qiskit import *
import time

try:
    from opensimplex import OpenSimplex
except:
    pass

def height2image (Z, terrain=None ):
    # converts a heightmap z into a PIL image
    # for terrain=None, this is a black and white image with white for Z[x,y]=1 and black for Z[x,y]=0
    # otherwise, the values in terrain are used as thresholds between sea and beach, beach and grass, etc
   
    image = {}
    for pos in Z:
        if terrain:
            if abs(Z[pos])<terrain[0]:
                if Z[pos]>0:
                    image[pos] = (50,120,200)
                else:
                    image[pos] = (25,60,100)
            elif abs(Z[pos])<terrain[1]:
                if Z[pos]>=0:
                    image[pos] = (220,220,10)
                else:
                    image[pos] = (110,110,5)
            elif abs(Z[pos])<terrain[2]:
                if Z[pos]>=0:
                    image[pos] = (100,200,0)
                else:
                    image[pos] = (50,100,0)
            elif abs(Z[pos])<terrain[3]:
                if Z[pos]>=0:
                    image[pos] = (75,150,0)
                else:
                    image[pos] = (37,75,0)
            elif abs(Z[pos])<terrain[4]:
                if Z[pos]>=0:
                    image[pos] = (200,200,200)
                else:
                    image[pos] = (100,100,100)
            else:
                if Z[pos]>=0:
                    image[pos] = (255,255,255)
                else:
                    image[pos] = (127,127,127)
        else:
            z = int(255*Z[pos])
            image[pos] = (z,z,z)
            
    size = max(Z.keys())
    img = Image.new('RGB',[size[j]+1 for j in range(2)])  
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            img.load()[x,y] = image[x,y]
    return img

def plot_height (Z,terrain=[5/16,6/16,9/16,12/16,14/16],zoom=None):
    # display a heightmap as the above image
    # displayed image is a terrain map by default
    img = height2image(Z,terrain=terrain)
    if zoom:
        img = img.resize((zoom*img.size[0],zoom*img.size[0]), Image.ANTIALIAS)
    img.save('temp.png')
    display(Image.open('temp.png'))
    



def simplex(L,period):
    try:
        # create a heightmap for an L[0]xL[1] image using simplex noise
        gen = OpenSimplex(seed=random.randint(0,10**20))
        Z = {}
        for x in range(L[0]):
            for y in range(L[1]):
                xx = period[0]*(x/L[0]-0.5)
                yy = period[1]*(y/L[1]-0.5)
                Z[x,y] = gen.noise2d(xx,yy)/2 + 0.5
    except:
        print("\n**The opensimplex package isn't available, so the islands won't be as fancy as they could be**")
        Z = {}
        for x in range(L[0]):
            for y in range(L[1]):
                Z[x,y] = 1
    return Z

def get_L(n):
    # determine the size of the grid corresponding to n qubits
    Lx = int(2**np.ceil(n/2))
    Ly = int(2**np.floor(n/2))
    return [Lx,Ly]

def make_grid(n):
    # make a dictionary for which every point in the grid is assigned a unique n bit string
    # these are such that '0'*n is in the center, and each string neighbours only its neighbours on the hypercube
    
    [Lx,Ly] = get_L(n)

    strings = {}
    for y in range(Ly):
        for x in range(Lx):
            strings[(x,y)] = ''

    for (x,y) in strings:
        for j in range(n):
            if (j%2)==0:
                xx = np.floor(x/2**(j/2))
                strings[(x,y)] = str( int( ( xx + np.floor(xx/2) )%2 ) ) + strings[(x,y)]
            else:
                yy = np.floor(y/2**((j-1)/2))
                strings[(x,y)] = str( int( ( yy + np.floor(yy/2) )%2 ) ) + strings[(x,y)]

    center = '0'*n
    current_center = strings[ ( int(np.floor(Lx/2)),int(np.floor(Ly/2)) ) ]
    diff = ''
    for j in range(n):
        diff += '0'*(current_center[j]==center[j]) + '1'*(current_center[j]!=center[j])
    for (x,y) in strings:
            newstring = ''
            for j in range(n):
                newstring += strings[(x,y)][j]*(diff[j]=='0') + ('0'*(strings[(x,y)][j]=='1')+'1'*(strings[(x,y)][j]=='0'))*(diff[j]=='1')
            strings[(x,y)] = newstring
            
    grid = {}
    for y in range(Ly):
        for x in range(Lx):
            grid[strings[(x,y)]] = (x,y)
    
    return strings


def normalize_height(Z,nonzero=False):
    # scales heights so that the maximum is 1 and the minimum is 0
    maxZ = max(Z.values())
    minZ = min(Z.values())
    epsilon = 1/( max(Z)[0]*max(Z)[1] )**2
    for pos in Z:
        Z[pos] = (Z[pos]-minZ)/(maxZ-minZ)
        if nonzero:
            if Z[pos]==0:
                Z[pos] = epsilon 
    return Z

def counts2height(counts,grid,log=False):
    # set the height of a point to be the counts value of the corresponding bit string (or the logarithm) and normalize
    Z = {}
    for pos in grid:
        try:
            Z[pos] = counts[grid[pos]]
        except:
            Z[pos] = 0
    if log:
        for pos in Z:
            Z[pos] = max(Z[pos],1/len(grid)**2)
            Z[pos] = np.log( Z[pos] )/np.log(2)
    Z = normalize_height(Z)    
    return Z


def height2state(Z,grid):
    # converts a heightmap intp a quantum state
    N = len(grid)
    state = [0]*N

    for pos in Z:
        state[ int(grid[pos],2) ] = np.sqrt( Z[pos] ) # amplitude is square root of height value
    R = sum(np.absolute(state)**2)
    state = [amp / np.sqrt(R) for amp in state] # amplitudes are normalized
    return state


def state2counts (state,shots=None):
    N = len(state)
    n = int(np.log2(N))
    if shots is None:
        shots = N**2
    counts = {}
    for j in range(N):
        string = bin(j)[2:]
        string = '0'*(n-len(string)) + string
        counts[string] = np.absolute(state[j])**2 * shots # square amplitudes to get probabilities
    return counts


def flat_height(L):
    # create height map that is 0 everywhere
    Z ={}
    for x in range(L[0]):
        for y in range(L[1]):
            Z[x,y] = 0
    return Z

def mountain_seed(L,l,N):
    # create height map of size L with N random points within a box of size l in the middle
    Z = flat_height(L)
    xs = range( int( (L[0]-l[0])/2 ), int( (L[0]+l[0])/2 ) )
    ys = range( int( (L[1]-l[1])/2 ), int( (L[1]+l[1])/2 ) )
    for j in range(N):
        x = random.choice(xs)
        y = random.choice(ys)
        Z[x,y] = 1
        
    return Z

def quantum_tartan (seed,theta,grid=None,shots=1,log=True):
        
    n = int(np.log2( len(seed) ))
        
    if grid is None:
        grid = make_grid(n)

    state = height2state(seed,grid)

    q = QuantumRegister(n)
    qc = QuantumCircuit(q)
    qc.initialize(state,q)
    qc.ry(2*np.pi*theta,q)

    
    if shots>1:
        try:
            IBMQ.load_accounts()
            backend = IBMQ.get_backend('ibmq_16_melbourne')
        except:
            print('\nAn IBMQ account is required to use a real device\nSee https://github.com/Qiskit/qiskit-terra/blob/master/README.md')
    else:
        backend = Aer.get_backend('statevector_simulator')

    if shots>1:
        c = ClassicalRegister(n)
        qc.add_register(c)
        qc.measure(q,c)
    
    start = time.time()
    print('\nQuantum job initiated on '+str(backend.name())+'...')
    job = execute(qc, backend, shots=shots)
    end = time.time()
    print('Quantum job complete after',int(end-start),'seconds')
    

    if shots>1:
        counts = job.result().get_counts()
    else:
        counts = state2counts( job.result().get_statevector() )

    Z = counts2height(counts,grid,log=log)   

    return Z, grid


def shuffle_grid(grid):
    
    n = int( np.log(len(grid))/np.log(2) )
    
    order = [j for j in range(n)]
    random.shuffle(order)
    
    new_grid = {}
    for pos in grid:
        new_string = ''
        for j in order:
            new_string = grid[pos][j] + new_string
        new_grid[pos] = new_string
    
    return new_grid

def shuffle_height (Z,grid):
    
    new_grid = shuffle_grid(grid)
    new_Z = {}
    for pos in Z:
        string = grid[pos] 
        new_pos = list(new_grid.keys())[ list(new_grid.values()).index( string ) ]
        new_Z[new_pos] = Z[pos]
        
    return new_Z,new_grid


def rotate_height (Z,theta):
    # rotate height Z by angle theta
    L = list(max(Z))
    mid = [(L[j]+1)/2 for j in range(2)]
    
    Lr = [ int( 1.6*(L[j]+1) ) for j in range(2) ]
    midr = [Lr[j]/2 for j in range(2)]
    
    Zr = flat_height(Lr)
    
    for pos in Zr:
        
        d = [ pos[j]-midr[j] for j in range(2) ]
        
        x = int( d[0]*np.cos(theta*np.pi) + d[1]*np.sin(theta*np.pi) + mid[0] )
        y = int( -d[0]*np.sin(theta*np.pi) + d[1]*np.cos(theta*np.pi) + mid[1] )
        
        if (x,y) in Z:
            Zr[pos] = Z[x,y]
        else:
            Zr[pos] = 0
        
    return Zr


def islands(size,period,tartans):
    # height map of created by combining the quantum tartans of `tartans` using simplex noise defined by `period`
    Z = flat_height(size)
    
    Zs = simplex(size,period)
    
    tsize = max(tartans[0])
    
    for tartan in tartans:  
        unchosen = True
        while unchosen:
            x0 = random.choice(range(size[0]-tsize[0]))
            y0 = random.choice(range(size[1]-tsize[1]))
            if random.random()<Zs[x0,y0]:
                unchosen = False

        for (x,y) in tartan:
            if (x+x0,y+y0) in Z:
                Z[x+x0,y+y0] +=tartan[x,y]
                
    Z = normalize_height(Z,nonzero=True)

    return Z

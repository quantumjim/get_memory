from mcpi.minecraft import Minecraft
from mcpi import block
import random


def tree(x,z,y):
    
    for j in range(1,6):
        world.setBlock(x,z+j,y, block.WOOD.id)

    for xx in range(x-3,x+4):
        for yy in range(y-3,y+4):
            for zz in range(z+5,z+11):
                d = (xx-x)**2+(yy-y)**2+(zz-z-6)**2 + 0.1
                if d<8:# or random.random()<1/d:
                    world.setBlock(xx,zz,yy, block.LEAVES.id)

    '''for xx in range(x-3,x+4):
        for yy in range(y-3,y+4):
            for zz in range(z+5,z+11):
                if world.getBlock(xx,zz,yy) == block.LEAVES.id:
                    isolated = True
                    for (dx,dz,dy) in [(+1,0,0),(-1,0,0),(0,+1,0),(0,-1,0),(0,0,+1),(0,0,-1)]:
                        if world.getBlock(xx+dx,zz+dz,yy+dy) != block.AIR.id:
                             isolated = False
                    if isolated:
                        world.setBlock(xx,zz,yy, block.AIR.id)'''


world = Minecraft.create()


world.setBlocks(-132,-132,-132,132,132,132, block.AIR.id)
world.setBlocks(-134,0,-134,134,0,134,block.GLOWSTONE_BLOCK.id)


height = 8
depth = 8

levels = [5/16,6/16,9/16,12/16,14/16]

sea_level = depth+levels[0]*height+1

with open('heightmap.txt','r') as file:
    z = file.read()
z = eval(z)      

for (x,y) in z:

    X = x-144
    Y = y-144
    Z = depth + int( z[x,y]*height )+1

    z_eff = z[x,y]

    if z[x,y]>=0:
        if z_eff<levels[0]:
            world.setBlocks( X,1,Y, X,depth,Y, block.SANDSTONE.id )
            world.setBlocks( X,depth+1,Y, X,sea_level,Y, block.ICE.id )
        elif z_eff<levels[1]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            world.setBlock( X,Z+1,Y, block.SANDSTONE.id )
        elif z_eff<levels[2]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            world.setBlock( X,Z+1,Y, block.GRASS.id )
            if random.random()<0.025:
                tree(X,Z,Y)            
        elif z_eff<levels[3]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            world.setBlock( X,Z+1,Y, block.GRASS.id )
        elif z_eff<levels[4]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            if random.random()<1/3:
                world.setBlock( X,Z+1,Y, block.GRASS.id )
            else:
                world.setBlock( X,Z+1,Y, block.STONE.id )
        else:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            if z[x,y]<1:
                if random.random()<1/2:
                    world.setBlock( X,Z+1,Y, block.BEDROCK.id )
                else:
                    world.setBlock( X,Z+1,Y, block.STONE.id )
            else:
                world.setBlock( X,Z+1,Y, block.GLOWSTONE_BLOCK.id )
    else:
        world.setBlocks( X,1,Y, X,depth+1,Y, block.WATER_STATIONARY.id )

        

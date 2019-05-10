from mcpi.minecraft import Minecraft
from mcpi import block
import random

world = Minecraft.create()


world.setBlocks(-132,-132,-132,132,132,132, block.AIR.id)
world.setBlocks(-134,0,-134,134,0,134,block.BEDROCK.id)


height = 12
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
            world.setBlocks( X,sea_level+1,Y, X,132,Y, block.AIR.id )
        elif z_eff<levels[1]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            world.setBlock( X,Z+1,Y, block.SANDSTONE.id )
            world.setBlocks( X,Z+2,Y, X,132,Y, block.AIR.id )
        elif z_eff<levels[2]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            if random.random()<1.0:
                world.setBlock( X,Z+1,Y, block.GRASS.id )
            else:
                world.setBlock( X,Z+1,Y, block.STONE.id )
            world.setBlocks( X,Z+2,Y, X,132,Y, block.AIR.id )
        elif z_eff<levels[3]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            if random.random()<2/3:
                world.setBlock( X,Z+1,Y, block.GRASS.id )
            else:
                world.setBlock( X,Z+1,Y, block.STONE.id )
            world.setBlocks( X,Z+2,Y, X,132,Y, block.AIR.id )
        elif z_eff<levels[4]:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            if random.random()<1/3:
                world.setBlock( X,Z+1,Y, block.GRASS.id )
            else:
                world.setBlock( X,Z+1,Y, block.STONE.id )
            world.setBlocks( X,Z+2,Y, X,132,Y, block.AIR.id )
        else:
            world.setBlocks( X,1,Y, X,Z,Y, block.STONE.id )
            if z[x,y]<1:
                if random.random()<1/2:
                    world.setBlock( X,Z+1,Y, block.BEDROCK.id )
                else:
                    world.setBlock( X,Z+1,Y, block.STONE.id )
            else:
                world.setBlock( X,Z+1,Y, block.GLOWSTONE_BLOCK.id )
            world.setBlocks( X,Z+2,Y, X,132,Y,block.AIR.id )
    else:
        world.setBlocks( X,1,Y, X,depth+1,Y, block.WATER_STATIONARY.id )
        world.setBlocks( X,depth+2,Y, X,132,Y,block.AIR.id )

        

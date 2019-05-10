from GetMemory import *

make_world()

with open('heightmap.txt','r') as file:
    Z = eval( file.read() )

img = height2image(Z,terrain=[2/16,3/16,5/16,10/16,12/16])
img.save('map.png')

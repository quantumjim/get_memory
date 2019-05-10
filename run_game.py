import pygame
from WorldBuilder import *
from GetMemory import *
import random


pygame.init()

try:
    pygame.joystick.init()
    num_joysticks = pygame.joystick.get_count()
    if num_joysticks > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
except:
    pass


print('\n'*100)
print('''██╗      ██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗          
██║     ██╔═══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝          
██║     ██║   ██║███████║██║  ██║██║██╔██╗ ██║██║  ███╗         
██║     ██║   ██║██╔══██║██║  ██║██║██║╚██╗██║██║   ██║         
███████╗╚██████╔╝██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝██╗██╗██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝\n\n''')

while True:
    
    # open current map

    with open('heightmap.txt','r') as file:
        Z = eval( file.read() )

    img = height2image(Z,terrain=[2/16,3/16,5/16,10/16,12/16])
    img.save('map.png')



    # choose positions

    heights = list( Z.values() )
    exit_pos = list(Z.keys())[heights.index( max( heights ) )]

    choosing = True
    xs = range( int(max(Z)[0]/3), int(2*max(Z)[0]/3) )
    ys = range( int(max(Z)[1]/3), int(2*max(Z)[1]/3) )
    while choosing:
        x = random.choice(xs)
        y = random.choice(ys)
        if Z[x,y]>0 and Z[x,y]<12/16:
            player_pos = [x,y]
            choosing = False

    empties = []
    for pos in Z:
        if Z[pos]>0 and pos!=player_pos and pos!=exit_pos:
            empties.append(pos)
    moneys = random.choices(empties,k=40)

    
    # game loop
    


    width=512
    height=512

    zoom = 4
    
    d = 3

    clock_rate=20

    size = (width, height)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption(".get_memory()")

    clock = pygame.time.Clock()

    background = pygame.image.load("map.png").convert()
    map_height = background.get_height()
    map_width = background.get_height()

    background = pygame.transform.scale(background, (zoom*map_width, zoom*map_height))
    player = pygame.image.load("player.png").convert_alpha()
    exit = pygame.image.load("exit.png").convert_alpha()
    money = pygame.image.load("money.png").convert_alpha()
    bigexit = pygame.transform.scale(exit, (width, height))

    pos = [width/2-player_pos[0]*zoom,height/2-player_pos[1]*zoom]
    dx = 0
    dy = 0

    print('\n'*100)
    print('Welcome to')
    print('''    ██████╗ ███████╗████████╗     ███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ ██╗██╗ 
   ██╔════╝ ██╔════╝╚══██╔══╝     ████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗╚██╗ ██╔╝██╔╝╚██╗
   ██║  ███╗█████╗     ██║        ██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝ ╚████╔╝ ██║  ██║
   ██║   ██║██╔══╝     ██║        ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗  ╚██╔╝  ██║  ██║
██╗╚██████╔╝███████╗   ██║███████╗██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ╚██╗██╔╝
╚═╝ ╚═════╝ ╚══════╝   ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═╝╚═╝ ''')
    print('A game for Ludum Dare 44')
    print('\n'*5)
    print('\nYou are solar powered drone, exploring an island.')
    print('\nThe clouds seem to create a labyrinth of shadows, which you should take care to avoid.')
    print('\nTo move, press q, w, a or s.')
    print('\nTo teleport to a random location nearby, press the space bar.')
    print('\nTo end your journey, find the exit at the top of the tallest mountain (or just press p).')
    print('\nThe aim of the game is to figure out the aim of the game.')
    print('\nHave fun!\n')
    
    reallygameover=False
    gameover = False
    wealth = 0
    joystick_hat = (0,0)
    while(reallygameover==False):
        
        if gameover:
            reallygameover=True
            
        try:
            new_joystick_hat = joystick.get_hat(0)
        except:
            new_joystick_hat = (0,0)
            
        if new_joystick_hat!=joystick_hat:
            joystick_hat = new_joystick_hat
            dx = -d*joystick_hat[0]
            dy = d*joystick_hat[1]
            joystick_hat = new_joystick_hat     
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                dx = 0
                dy = 0
                if event.key == pygame.K_q:
                    dx = +d
                    dy = +d
                if event.key == pygame.K_w:
                    dx = -d
                    dy = +d
                if event.key == pygame.K_a:
                    dx = +d
                    dy = -d
                if event.key == pygame.K_s:
                    dx = -d
                    dy = -d
                if event.key == pygame.K_SPACE:
                    choosing = True
                    while choosing:
                        dx = (map_width/10)*2*(random.random()-0.5)
                        dy = (map_height/10)*2*(random.random()-0.5)
                        (x,y) = ( int(player_pos[0]-dx/zoom),int(player_pos[1]-dy/zoom) )
                        if (x,y) in Z:
                            if Z[x,y]>0:
                                choosing = False
                    wealth = max(0,wealth-1)
                    print( "\nTeleportation costs $1 (it's free if you don't have that much)")
                    print( 'You now have $'+str(wealth)+'\n' )
                if event.key == pygame.K_p:
                    gameover = True
                    
            if event.type == pygame.KEYUP:
                dx = 0
                dy = 0  
   

        (x,y) = ( int(player_pos[0]-dx/zoom),int(player_pos[1]-dy/zoom) )
        if (x,y) in Z:
            if Z[x,y]>0:
                pos[0] += dx
                pos[1] += dy
                player_pos[0] -= dx/zoom
                player_pos[1] -= dy/zoom
            elif joystick_hat == (0,0):
                pos[0] -= dx
                pos[1] -= dy
                player_pos[0] += dx/zoom
                player_pos[1] += dy/zoom

        (X,Y) = ( int(player_pos[0]),int(player_pos[1]) )

        close = []
        for jx in range(-2,3):
            for jy in range(-2,3):
                close.append( (X+jx,Y+jy) )

        for temp_pos in close:
            if temp_pos in moneys:
                moneys.remove(temp_pos)
                wealth += 10
                print( '\nYou picked up $10')
                print( 'You now have $'+str(wealth)+'\n' )

        if exit_pos in close:
            gameover = True       
                
        if gameover:
            screen.blit(bigexit, [0,0] )
        else:
            screen.blit(background, pos)
            screen.blit(exit, [pos[0]+zoom*exit_pos[0]-12,pos[1]+zoom*exit_pos[1]-12] )
            for (x,y) in moneys:
                screen.blit(money, [pos[0]+zoom*x-12,pos[1]+zoom*y-12] )
            screen.blit(player, [width/2-12,height/2-12] )
            

        pygame.display.flip()
        clock.tick(clock_rate)


    

    
            
    print('\n'*100)
    print(''' ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝''')
    print('\n'*5)
    print('\nYou have left the island.')
    print('\nDid you collect all the items?')
    print('\nWell done if you did, but we have no reward for you.')
    print('\nDid you try to maximize your wealth?')
    print("\nYou must have developed an interesting strategy if you did, but there's no reward for it.")
    print('\nDid you just enjoy the journey?')
    print("\nI hope just wandering around wasn't too boring.")
    print('\n\nThe point of the game was to explore whether you need in-game currency to bring meaning to your in-game life')
    print('\nExtrapolating the results to real life is done at your own risk.')
          
    print("\n\nThe island was generated by running a quantum program using Qiskit.")
    print('\nThis is an open-source framework for programming quantum computers in Python. See qiskit.org for more info.')
    input("\n\nPress Enter (here in the terminal) to run a new quantum program and generate a new island.\n")
    print('\n'*100)
    print('''██╗      ██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗          
██║     ██╔═══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝          
██║     ██║   ██║███████║██║  ██║██║██╔██╗ ██║██║  ███╗         
██║     ██║   ██║██╔══██║██║  ██║██║██║╚██╗██║██║   ██║         
███████╗╚██████╔╝██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝██╗██╗██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝''')
    print('\n'*5)
    print('The island generation procedure is now beginning. The whole process should take less than 30 seconds.\n')
    make_world()

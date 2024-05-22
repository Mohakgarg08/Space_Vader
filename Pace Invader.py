import pygame


pygame.init()


W = 20
H = 10
TILE = 45
GAME_RES = W * TILE, H * TILE
screen = pygame.display.set_mode(GAME_RES)

# https://stackoverflow.com/questions/68567945/what-is-the-easiest-way-to-make-a-triangles
screen.fill((0, 0, 0))


x = 200
y = 200
width = 20
height = 20
vel = 5  # Velocity


run= True
while run:
    pygame.time.delay(35)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    # Move left
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    # Move right
    if keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel
    screen.fill((0, 0, 0))
    tr = pygame.draw.polygon(screen, (255,0,0), ((x,y),(x+150,y),(x+75,y-200)))
    pygame.display.update()

   
#class Player():



#sites so far (will add more later)
#https://www.youtube.com/watch?v=7kGNs5R-AM8
#https://data-flair.training/blogs/python-tetris-game-pygame/
#https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
#https://www.mygreatlearning.com/blog/python-main/
#https://www.geeksforgeeks.org/python-drawing-different-shapes-on-pygame-window/ 

#SCHEDULE:

#first make the box in which the program will start/appear
# MAKE THE SHAPES
#- use the matrix idea of making one and then making designs within that
#- program each shape so that there are rotations of each (me and akansh do 3 separate and then the final one will do together in class)
#- program so that the shape can move right left up down (each of us remember)
#- make boundaries for it
#Use the random module to then start making the shapes appear on the screen at random
#Code so that if a row has 10 in the row then it disappears and it gives 10 points to the user
#add a quit button, a timer of 30 seconds per shape, a background
#the end

#this code from the W to the clock.tick() is from the youtube link https://www.youtube.com/watch?v=7kGNs5R-AM8 
#W = 10
#H = 20
#TILE = 45
#GAME_RES = W * TILE, H * TILE

#def main(): #setting up the main loop of the game
 #   global screen, clock #modifying both the screen and the clock  
  #  pygame.init() #pygame.init() = this is something that initializes all of the imported PyGame modules 
   # screen = pygame.display.set_mode(GAME_RES) #set_mode = this is a function that specifies the size of the screen  
   # clock = pygame.time.Clock() #.Clock = this is used to get the current processing time 

    #while True:
     #   draw_grid() #drawing the grid
      #  for event in pygame.event.get(): #.get = returns a value from the dictionary 
       #     if event.type == pygame.QUIT:
        #        pygame.quit() #exit() = terminates the program
         #       quit()
        #pygame.display.flip() #.flip = reverses the elements of the array or the display
        #clock.tick(60) #we went until here and copy-pasted from the youtube 

#def draw_grid(): 
#    screen.fill(pygame.Color('black'))
    #for x in range(0, W * TILE, TILE): #iterating for the horizontal position 
        #for y in range(0, H * TILE, TILE): #iterating for the vertical position 
          #  rect = pygame.Rect(x, y, TILE, TILE) 
         #   pygame.draw.rect(screen, pygame.Color('blue'), rect, 1) #.fill = this is filling in the color of the shape

#Shapes
#This is our starting - we used the sites above to help guide us, the youtube link uses coordinates, and the website uses a matrix pattern
#we decided to do matrix as well (not copying promise!!)
#starting for shaping our shapes - Hajrah made this matrix design - got this from the youtube link - Hajrah's part
#matrixDesignForShapes = [
   # [[0, 1, 2, 3]],  #we start at 0 because since this is a grid we count it
   # [[4, 5, 6, 7]],  #we are doing columns of 4 because in the tetris game, where we are basing off our game logic from, since we are doing a tetris inspired idea,
   # [[8, 9, 10, 11]],  #all the shapes include 4 squares just mismatches, so that's why we are doing 4 by 4 because we want 4 rows and columns (will make sense later on when we design each shape)
   # [[12, 13, 14, 15]]  #4 by 4
#]

#Shape I & Shape J & Shape T - Akansh
#shapes_I_J_T = [
 #              [[ 13, 9, 5, 1], [ 7, 6, 5, 4]], #I shape
  #             [[10, 6, 2, 1], [9, 5, 6, 7], [11, 10, 6, 2], [3, 5, 6, 7]], #J shape
  #             [[[6, 5, 4, 1], [9, 5, 1, 4], [9, 6, 5, 4], [9, 5, 1, 6]]], #T shape 
 #              ]

#Shape S & Shape Z & Shape L - Hajrah
#shapes_S_Z_L = [
 #   [[1, 2, 4, 5], [1, 5, 6, 10]], #S shape
 #   [[], []], #Z shape
 #   [[], []]  #L shape
#]

#if __name__ == "__main__":
  #  main()
    
#Displaying and rotating the shapes

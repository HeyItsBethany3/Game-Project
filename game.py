#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snowman can move left or right. Press enter to start the game.
Get points and health by collecting snowflakes. Health runs out over time. 
Snowman dies if it hits the branches or melts (does not have enough health)
"""
from PPlay.window import Window
from PPlay.gameimage import GameImage
from scorer import Scorer
from highscoremanager import ScoreManager

import pygame
import os
game_state = 2  # in menu

# Set display
background = GameImage('sprite/scenario/scenarionew.gif')
menu_bg = GameImage('sprite/scenario/start.png')
start_button = GameImage('sprite/scenario/button.png')
game_over = GameImage('sprite/scenario/GAMEOVER.png')


# Define screen variables
sWidth = 512 # screen width
sHeight = 512 # screen height

window = Window(sWidth, sHeight)
window.set_title('SnowMan')

score_manager = ScoreManager() # Stores high score
scorer = Scorer(window) # Calculates score
record_checked = False

# Define tree variables
TreeWidth = 60
TreeStartWidth = (sWidth-TreeWidth)//2 # left coordinate where tree starts

# Define branch variables
branchWidth = TreeWidth*3 
branchHeight = sHeight//40 

# Define snowman variables
snowmanDist = 140   # Distance from tree
snowmanY = 2*sHeight//3 + 36  # Distance from screen top to top of snowman  
radFlake = 10 # Snowflake radius 


 

class Branches:
    
    changeY = 4 # How quickly branch moves down vertically
    
    tree_types = ('sprite/branches/right1.png',
                       'sprite/branches/left.png',
                       'sprite/branches/00.png')

    
    def __init__(self,y, pos):
        self.y = y # height from top of screen
        self.pos = pos # left or right of tree (or middle)
        if pos == "left":
            self.type = 1
        elif pos == "right":
            self.type = 0
        else:
            self.type = 2
            
        self.texture = GameImage(self.tree_types[self.type])
        if pos == "left":
            self.texture.set_position(0, self.y)
        elif pos == "right":
            self.texture.set_position(0, self.y)
        else:
            self.texture.set_position(0, self.y)
        
    def set_position(self, x, y):
        # Change position
        self.texture.set_position(x, y)

    def paint(self):
        
        self.texture.set_position(0, self.y)
        # If branch has position left, draw to left of tree
        self.texture.draw()
            
    def move(self, snowmanPos):
        global bgColour,treeColour, game_state
        
        
        newY = self.y + self.changeY
        # lower bound for branch y value
        lowerBound = newY + branchHeight
        
        if lowerBound > snowmanY and snowmanPos == self.pos:  
            # New branch would be in snowmans space
            game_state = 0 #game over
           
            
        elif (lowerBound > sHeight):
            # Branch starts at top of screen again
            self.y = -50  # change to 64?
            self.paint()
        else:
            # Branch moves down visually 
            self.y += self.changeY 
            self.paint()
            
        
class Snowman:
    sprites = (GameImage('sprite/snowman/1.png', 0, snowmanY),
                        GameImage('sprite/snowman/4.png', 0, snowmanY))
    
    height = sprites[0].get_height()
    
    # Snowman position is left or right of tree (always has same y coordinate)
    def __init__(self, pos):
        self.pos = pos # left or right 
    
    def paint(self):
        # Draws snowman on correct side of tree
        global screen
        if self.pos == "left":
            self.sprites[0].draw()
            
        else:
            self.sprites[1].draw()
            
            
class Snowflake:
    
    changeY = 4 
    
    def __init__(self, y, pos):
        self.pos = pos # left or right 
        self.y = y # y coordinates
    
    def paint(self,colour):
        # Draws snowflake on correct side of tree
        global screen
        if self.pos == "left":
            pygame.draw.circle(screen,colour,(TreeStartWidth-snowmanDist,self.y),radFlake)
        else:
            pygame.draw.circle(screen,colour,(TreeStartWidth+snowmanDist+TreeWidth,self.y),radFlake)
            
    def move(self, snowmanPos):
        global bgColour, flakeColour, points
        
        
        # Hide current snowflake
        #self.paint(bgColour)
    
        newY = self.y + self.changeY
        # lower bound for branch y value
        lowerBound = newY + branchHeight
        
        if lowerBound > snowmanY  and snowmanPos == self.pos: 
            # New flake be in snowmans space
            scorer.snowflake_calc() # gain points and health by catching snowflakes           
            self.y = 0
            self.paint(flakeColour)
                      
        elif (lowerBound > sHeight):
            # snowflake starts at top of screen again
            self.y = 0 
            self.paint(flakeColour)
        else:
            # Snowflake moves down  
            self.y += self.changeY
            self.paint(flakeColour)
            


# Main code

# Initialise pygame and draw screen
pygame.init()
screen = pygame.display.set_mode((sWidth, sHeight))

# Specify colours
bgColour = pygame.Color("white")
treeColour = pygame.Color("green")
snowmanColour = pygame.Color("red")
flakeColour = pygame.Color("blue")

# Colour the background
#screen.fill(bgColour)
#background.draw()

# Create branches
fromTop = 20 # Distance initially from top of screen
branch1 = Branches(fromTop, "left")
branch2 = Branches(fromTop+150, "right")
branch3 = Branches(fromTop+320, "left")
snowman = Snowman("right")


# Create snowflakes
flake1 = Snowflake(50, "left")
flake2 = Snowflake(250, "left")
flake3 = Snowflake(400, "right")
flake4 = Snowflake(230, "right")
flake5 = Snowflake(120, "right")
flake6 = Snowflake(20, "right")

# Make default tree
treeHeight = GameImage('sprite/branches/00.png').get_height()
treeWidth = GameImage('sprite/branches/00.png').get_width()
# treeWidth is 512, treeHeight is 64

# Create tree (default background)
tree = []

for i in range(sHeight*2):
    if (i+1)%treeHeight==0:
        tree.append(Branches(i+1-(2*treeHeight), "middle"))
    

    
def paintEverything():
    background.draw()

    snowman.paint()
    
    for item in tree:
        item.paint()
        
    branch1.paint()
    branch2.paint()
    branch3.paint()
    
    
    flake1.paint(flakeColour)
    flake2.paint(flakeColour)
    flake3.paint(flakeColour)
    flake4.paint(flakeColour)
    flake5.paint(flakeColour)
    flake6.paint(flakeColour)
    
    pygame.display.flip()
    
    
def moveEverything():
    
    for item in tree:
        item.move(snowman.pos)
    
    
    # Move branches  
    branch1.move(snowman.pos)
    branch2.move(snowman.pos)
    branch3.move(snowman.pos)

        
    # Move snowflakes
    flake1.move(snowman.pos)
    flake2.move(snowman.pos)
    flake3.move(snowman.pos)
    flake4.move(snowman.pos)
    flake5.move(snowman.pos)
    flake6.move(snowman.pos)
    pygame.display.flip()
    


# Sets the speed of program
clock = pygame.time.Clock()
clock.tick(40)
counter = 1 # time counter

while True:
    
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        # Can close game at any time 
        break
    
    
    elif game_state == 1:
        # Game in progress
        
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            snowman.pos = "left"
        
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                snowman.pos = "right"
            
        # Update background
        paintEverything()
    
        
        # Branches and snowflakes move faster over time
        if counter%1000 == 0:
            Branches.changeY += 2
            Snowflake.changeY += 2
        counter += 1
        
        # Move branches and snowflakes
        moveEverything()
        
        if counter%10 == 0:
            # Lose health but gain points over time
            scorer.add_points()
            scorer.update() 
            
        scorer.draw()
        
        if not scorer.snowie_alive():
            game_state = 0 # Game over
            
        # Shows any changes made
        pygame.display.flip()
        
        
    elif game_state == 2:
        background.draw()
        menu_bg.draw()
        start_button.draw()
        window.draw_text(str(score_manager.get_records()), 512 - 56, 274, color=(20, 200, 50), font_file='font.TTF', size=30)
        pygame.display.flip()
       
        
        
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            # Enter to start game
            game_state = 1 
            counter = 1 # time starts now 
            
            # Initial graphics
            paintEverything()
            scorer.draw()
            
    elif game_state == 0:
        # Game over
        
        # Calculate high score
        if not record_checked:
            if scorer.get_points() > score_manager.get_records():
                score_manager.set_new_record(scorer.get_points())
            record_checked = True
            
        background.draw()
        game_over.draw()
        
        # Show high scores on game over screen
        window.draw_text(str(score_manager.get_records()), 260, 205, color=(20, 200, 50), font_file='font.TTF',
                         size=30)#highest records
        window.draw_text(str(scorer.get_points()), 260, 240, color=(20, 200, 50), font_file='font.TTF',
                         size=30)#last score
        
        
        
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            #start game again
            game_state = 1 
            counter = 1 # time starts now 
            
            # Re-initialise objects
            fromTop = 20 # Distance initially from top of screen
            branch1 = Branches(fromTop, "left")
            branch2 = Branches(fromTop+150, "right")
            branch3 = Branches(fromTop+320, "left")
            snowman = Snowman("right")

            # Create snowflakes
            flake1 = Snowflake(50, "left")
            flake2 = Snowflake(250, "left")
            flake3 = Snowflake(400, "right")
            flake4 = Snowflake(230, "right")
            flake5 = Snowflake(120, "right")
            flake6 = Snowflake(20, "right")
            
            paintEverything()
            
            scorer = Scorer(window)
            record_checked = False
            scorer.draw()
        
        pygame.display.flip()
        
       
    

pygame.quit()  # Stops program
os._exit(0)  # Stops program for mac OS users

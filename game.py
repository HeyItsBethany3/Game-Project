#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creates initial tree with branches. Snowman can be placed on left or right of 
tree. Game stops if snowman hits branches. Click to start the game.
"""
import pygame
import os
start = False

# Define screen variables
sWidth = 1400 # screen width
sHeight = 700 # screen height

# Define tree variables
TreeWidth = 60
TreeStartWidth = (sWidth-TreeWidth)//2 # left coordinate where tree starts

# Define branch variables
branchWidth = TreeWidth*3 
branchHeight = sHeight//40 

# Define snowman variables
snowmanDist = 70   # Distance from tree
snowmanY = 7*sHeight//8   # Distance from screen top to centre of snowman  
rad = 15  # Snowman radius 
radFlake = 10 # Snowflake radius 

# Keep score
points = 0
 

class Branches:
    
    changeY = 4 # How quickly branch moves down vertically
    
    def __init__(self,y, pos):
        self.y = y # height from top of screen
        self.pos = pos # left or right of tree

    def paint(self,colour):
        global screen
        
        # If branch has position left, draw to left of tree
        if self.pos == "left":
            pygame.draw.rect(screen, colour, \
                             pygame.Rect(TreeStartWidth-branchWidth,self.y,branchWidth,branchHeight))
            
        # If branch has position right, draw to right of tree
        else:
            pygame.draw.rect(screen, colour, \
                             pygame.Rect(TreeStartWidth+TreeWidth,self.y,branchWidth,branchHeight))
            
            
    def move(self, snowmanPos):
        global bgColour,treeColour
        
        if not start:
            return
        
        # Hide current branch
        self.paint(bgColour)
        newY = self.y + self.changeY
        # lower bound for branch y value
        lowerBound = newY + branchHeight
        
        if lowerBound < snowmanY+rad and lowerBound > snowmanY-rad and \
        snowmanPos == self.pos: 
            # New branch would be in snowmans space
            # Display game over
            while True:
                    # Infinite loop until we close screen
                    e = pygame.event.poll()
                    if e.type == pygame.QUIT:
                        break
            pygame.quit()  
            os._exit(0)
        
                      
        elif (lowerBound > sHeight):
            # Branch starts at top of screen again
            self.y = 0 
            self.paint(treeColour)
        else:
            # Branch moves down visually 
            self.y += self.changeY
            self.paint(treeColour)
            
        
class Snowman:
    
    # Snowman position is left or right of tree (always has same y coordinate)
    def __init__(self, pos):
        self.pos = pos # left or right 
    
    def paint(self,colour):
        # Draws snowman on correct side of tree
        global screen
        if self.pos == "left":
            pygame.draw.circle(screen,colour,(TreeStartWidth-snowmanDist,snowmanY),rad)
        else:
            pygame.draw.circle(screen,colour,(TreeStartWidth+snowmanDist+TreeWidth,snowmanY),rad)
            
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
        
        if not start:
            return
        
        # Hide current snowflake
        self.paint(bgColour)
        newY = self.y + self.changeY
        # lower bound for branch y value
        lowerBound = newY + branchHeight
        
        if lowerBound < snowmanY+rad and lowerBound > snowmanY-rad and \
        snowmanPos == self.pos: 
            # New flake be in snowmans space
            points += 1                
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
screen.fill(bgColour)

# Draw the tree
pygame.draw.rect(screen, treeColour, pygame.Rect(TreeStartWidth,0,TreeWidth,sHeight))

# Draw braches
fromTop = 20 # Distance initially from top of screen
branch1 = Branches(fromTop, "left")
branch1.paint(treeColour)

branch2 = Branches(fromTop+200, "right")
branch2.paint(treeColour)

branch3 = Branches(fromTop+400, "left")
branch3.paint(treeColour)

# Draw snowman
snowman = Snowman("right")
snowman.paint(snowmanColour)

# Create snowflakes
flake1 = Snowflake(200, "left")
flake1.paint(flakeColour)

flake2 = Snowflake(450, "left")
flake2.paint(flakeColour)

flake3 = Snowflake(300, "right")
flake3.paint(flakeColour)

flake4 = Snowflake(390, "right")
flake4.paint(flakeColour)

flake5 = Snowflake(120, "right")
flake5.paint(flakeColour)

flake6 = Snowflake(20, "right")
flake6.paint(flakeColour)

# Sets the speed of program
clock = pygame.time.Clock()
clock.tick(40)
counter = 1 # time counter

while True:
    
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        # Can close game at any time
        
        break
    elif e.type == pygame.MOUSEBUTTONDOWN :
        # Click to start game
        start = True
        counter = 1 # time starts now 
        
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        snowman.paint(bgColour)
        snowman.pos = "left"
        snowman.paint(snowmanColour)
        
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        snowman.paint(bgColour)
        snowman.pos = "right"
        snowman.paint(snowmanColour)

    # Shows any changes made
    pygame.display.flip()
    
    # Branches and snowflakes move faster over time
    if counter%1000 == 0:
        Branches.changeY += 2
        Snowflake.changeY += 2
    counter += 1
    
    
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

print("You have {} points!".format(points))
pygame.quit()  # Stops program
os._exit(0)  # Stops program for mac OS users

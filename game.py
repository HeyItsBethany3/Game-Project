#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creates initial tree with branches 
"""
import pygame
import os

# global variables
width = 1400
height = 700
TreeWidth = 60
TreeStartWidth = (width-TreeWidth)//2
direction = 10
branchWidth = TreeWidth*3
branchHeight = height//40
snowmanDist = 20   #Distance from tree
snowmanY = 7*height//8   # Position from top of centre of snowman  
rad = 10  # Snowman radius 

class Branches:
    
    def __init__(self,x,changeX, pos):
        self.x = x #height from top 
        self.changeX = changeX
        self.pos = pos # left or right

    def show(self,colour):
        global screen
        if self.pos == "left":
            pygame.draw.rect(screen, colour, \
                             pygame.Rect(TreeStartWidth-branchWidth,self.x,branchWidth,branchHeight))
        elif self.pos == "right":
            pygame.draw.rect(screen, colour, \
                             pygame.Rect(TreeStartWidth+TreeWidth,self.x,branchWidth,branchHeight))
        else:
            pass # Error has occurred
            
            
    def update(self, snowmanPos):
        global bgColor,fgColor
        
        self.show(bgColor)
        newX = self.x + self.changeX 
        
        if newX < snowmanY+rad and newX > snowmanY-rad: # Branch is in snowmans space
            if snowmanPos == self.pos:
                # display game over
                while True:
                    e = pygame.event.poll()
                    if e.type == pygame.QUIT:
                        break
                pygame.quit()  
                os._exit(0)
                    
            
        elif newX + branchHeight >= height:
            self.x = 0
        else:
            self.x += self.changeX
            self.show(fgColor)
            
        

class Snowman:
    

    #  snowman is either left or right - always has same y coordinates
    def __init__(self, pos):
        self.pos = pos
    
    def show(self,colour):
        global screen
        if self.pos == "left":
            pygame.draw.circle(screen,colour, (TreeStartWidth-snowmanDist,snowmanY),rad)
        elif self.pos == "right":
            pygame.draw.circle(screen,colour, (TreeStartWidth+snowmanDist+TreeWidth,snowmanY),rad)
        else:
            pass
        
        

# we start drawing our scenario:

pygame.init()

screen = pygame.display.set_mode((width, height))

bgColor = pygame.Color("white")
fgColor = pygame.Color("green")
snowmanColor = pygame.Color("red")

# filling the background
screen.fill(bgColor)

# draw the tree
pygame.draw.rect(screen, fgColor, pygame.Rect(TreeStartWidth,0,TreeWidth,height))

# draw braches
fromTop = 20
branch1 = Branches(fromTop, 10, "left")
branch1.show(fgColor)

branch2 = Branches(fromTop+200, 10, "right")
branch2.show(fgColor)

branch3 = Branches(fromTop+400, 10, "left")
branch3.show(fgColor)

# draw snowman
snowman = Snowman("right")
#snowman.show(snowmanColor)

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    # visualise the changes you just made
    pygame.display.flip()
    
    # update branches
    
    branch1.update(snowman.pos)
    branch2.update(snowman.pos)
    branch3.update(snowman.pos)
    
    #inputKey = pygame.key.get_mods()
    #rightKey = pygame.key.name(pygame.K_RIGHT)
    #if pygame.key.get_focused():
        #if pygame.key.name() == "K_LEFT" and snowman.pos=="right":
         #   snowman = Snowman("left")
         #   snowman.show(snowmanColor)
        
       # if pygame.key.name() == "K_RIGHT" and snowman.pos=="left":
         #   snowman = Snowman("right")
          #  snowman.show(snowmanColor)


pygame.quit()  # for the rest of you.
os._exit(0)  # just for MacOs users

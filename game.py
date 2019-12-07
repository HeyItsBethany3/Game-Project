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
from random import randint

import pygame
import os
game_state = 2  # in menu

# Set display
background = GameImage('sprite/scenario/scenarionew.png')
menu_bg = GameImage('sprite/scenario/newbkg.png')
game_over = GameImage('sprite/scenario/GameOver1.png')
button = GameImage('sprite/scenario/button1.png', 0, -140)


# Define screen variables
sWidth = 512 # screen width
sHeight = 512 # screen height

window = Window(sWidth, sHeight)
window.set_title('Snowman')

score_manager = ScoreManager() # Stores high score
scorer = Scorer(window) # Calculates score
record_checked = False

# Define tree variables
TreeWidth = 60
TreeStartWidth = (sWidth-TreeWidth)//2 # left coordinate where tree starts

# Define branch variables
branchHeight = 64

# Define snowman variables
snowmanDist = 140   # Distance from tree
snowmanY = 2*sHeight//3 + 36  # Distance from screen top to top of snowman
radFlake = 10 # Snowflake radius

#flakeHeight = 150


class Branches:

    changeY = 6 # How quickly branch moves down vertically
    direction = "up"

    tree_types = ('sprite/branches/right.png',
                  'sprite/branches/left.png',
                  'sprite/branches/middle.png')
    endOfScreen = False

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
        self.texture.set_position(0, self.y)

    def set_position(self, x, y):
        # Change position
        self.texture.set_position(x, y)

    def paint(self):
        self.set_position(0,self.y)
        self.texture.draw()

    def move(self, snowmanPos):
        global game_state


        newY = self.y + self.changeY
        
        # lower bound for branch y value
        lowerBound = newY + branchHeight
        upperBound = newY - branchHeight
        
    
        if  upperBound < snowmanY < lowerBound  and snowmanPos == self.pos:
            # New branch would be in snowmans space
                game_state = 0 #game over

            

        elif (newY > sHeight):
            # Branch starts at top of screen again
            self.y = -50  # change to 64?
            self.paint()
            self.endOfScreen = True
        else:
            # Branch moves down visually
            self.y += self.changeY
            self.paint()


class Snowman:
    
    sprites = (GameImage('sprite/snowman/snowmanLeft.png',  45, snowmanY),
               GameImage('sprite/snowman/snowmanRight.png', -45, snowmanY),
               GameImage('sprite/snowman/meltyLeft.png',    45, snowmanY),
               GameImage('sprite/snowman/meltyRight.png',   -45, snowmanY))

    

    # Snowman position is left or right of tree (always has same y coordinate)
    def __init__(self, pos):
        self.pos = pos # left or right
    

    def paint(self):
        # Draws snowman on correct side of tree
        
        if self.pos == "left":
            self.type = self.sprites[0]
            self.sprites[0].draw()

        else:
            self.sprites[1].draw()


class Snowflake:

    flakeImage = ('sprite/scenario/flakeL.png', 'sprite/scenario/flakeR.png')
    
    endOfScreen = False
    
    changeY = 6

    def __init__(self, y, pos):
        self.pos = pos # left or right
        self.y = y # y coordinates
        
        if pos == "left":
            self.type = 0
        else:
            self.type = 1

        self.texture = GameImage(self.flakeImage[self.type])
        self.set_position()
        
    def set_position(self):
        # Change position
        if self.pos == "left":
            self.texture.set_position(50, self.y)
        else:
            self.texture.set_position(-50, self.y)

    def paint(self):
        
        self.set_position()
        self.texture.draw()  


    def move(self, snowmanPos):
        
        
        newY = self.y + self.changeY
        # lower bound for branch y value
        lowerBound = newY + branchHeight # not sure why this works but it does
        upperBound = newY - branchHeight
        if upperBound < snowmanY < lowerBound  and snowmanPos == self.pos:
            # New flake be in snowmans space
            scorer.snowflake_calc() # gain points and health by catching snowflakes
            self.endOfScreen = True
            

        elif (lowerBound > sHeight):
            # snowflake starts at top of screen again
            
            self.endOfScreen = True
        else:
            # Snowflake moves down
            self.y += self.changeY
            self.paint()
            


def paintEverything():
    background.draw()

    snowman.paint()

    for item in tree:
        item.paint()

    for item in branches:
        item.paint()
        
    for item in flakes:
        item.paint()

    
    scorer.draw()

    pygame.display.flip()


def moveEverything():

    for item in tree:
        item.move(snowman.pos)
        
    # Move branches
    for index, item in enumerate(branches):
        item.move(snowman.pos)
        #If reaches end of screen, delete branch
        if item.endOfScreen:
            del branches[index]


    # Move snowflakes
    for index, item in enumerate(flakes):
        item.move(snowman.pos)
        if item.endOfScreen:
            del flakes[index]
    
    
    scorer.draw()
    pygame.display.flip()
    
    
    
def add_branches():
    
    side = randint(0,1)
    gap = 200 # freezes if this is too high
    count = 1
    while True:
        newY = randint(-512, 0)
        okayPosition = True
        for item in branches:
            if abs(newY-item.y) < gap:
                okayPosition = False
        if okayPosition:
            yValue = newY
            break
        count +=1
        if count == 20:
            yValue = False
            break
    
    if len(branches) < 4 and yValue != False:
        if side == 0: # left branch
                branches.append(Branches(yValue, "left"))
        else:
                branches.append(Branches(yValue, "right"))
        
 

def add_flakes():
    
    side = randint(0,1)
    gap = 100
    count = 1
    while True:
        newY = randint(-512, 0)
        okayPosition = True
        for item in branches:
            if abs(newY-item.y) < gap:
                okayPosition = False
        for item in flakes:
            if abs(newY-item.y) < gap:
                okayPosition = False
        if okayPosition:
            yValue = newY
            break
        count += 1
        if count == 20:
            yValue = False
            break
            
    if len(flakes) < 4 and yValue != False:
        if side == 0: # left branch
                flakes.append(Snowflake(yValue, "left"))
        else:
                flakes.append(Snowflake(yValue, "right"))
    

# Main code

# Initialise pygame and draw screen
pygame.init()
screen = pygame.display.set_mode((sWidth, sHeight))

# Specify colours
flakeColour = pygame.Color("blue")

snowman = Snowman("right")

# Create initial branches
branches = []




# Create snowflakes
flakes = []
flakes.append(Snowflake(50, "right"))
flakes.append(Snowflake(340, "left"))


# Make default tree
treeHeight = GameImage('sprite/branches/middle.png').get_height()
treeWidth = GameImage('sprite/branches/middle.png').get_width()
# treeWidth is 512, treeHeight is 64

# Create tree (default background)
tree = []

for i in range(sHeight*2):
    if (i+1)%treeHeight==0:
        tree.append(Branches(i+1-(2*treeHeight), "middle"))



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
                
        # Add branches and snowflakes if necessary
        add_branches()
        add_flakes()

        # Update background
        paintEverything()


        # Branches and snowflakes move faster over time
        startSpeed = 6
        maxSpeed = 10
        if counter%300 == 0: # change to 400
            if Branches.changeY == maxSpeed:
                Branches.diretion = "down"
            elif Branches.changeY == startSpeed:
                Branches.direction = "up"
            
            if Branches.direction == "up":
                # game speeds up
                Branches.changeY += 1
                Snowflake.changeY += 1
            else:
                # game slows down
                Branches.changeY -= 1
                Snowflake.changeY -= 1
            
        # Move branches and snowflakes
        moveEverything()

        if counter%50 == 0:
            # Gain points over time
            scorer.add_points()
        if counter % 10 == 0:
            # Lose health over time
            scorer.update(counter)

        if not scorer.snowie_alive():
            game_state = 0 # Game over
        
        counter += 1

        # Shows any changes made
        pygame.display.flip()


    elif game_state == 2:
        # Menu screen
        background.draw()
        if counter < 250:
            menu_bg.draw()
            window.draw_text(str(score_manager.get_records()), 512 - 260, 320, color=(255,255,255), font_file='font.TTF', size=20)
        else:
            button.draw()
        pygame.display.flip()

        
        counter += 1
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            # Enter to start game
            game_state = 1
            counter = 1 # time starts now

            # Initial graphics
            paintEverything()
        

    elif game_state == 0:
        # Game over

        # Calculate high score
        if not record_checked:
            if scorer.get_points() > score_manager.get_records():
                score_manager.set_new_record(scorer.get_points())
            record_checked = True

        background.draw()
        game_over.draw()

        if snowman.pos== "left":
                Snowman.sprites[2].draw()

        else:
                Snowman.sprites[3].draw()

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
            snowman = Snowman("right")

            branches = []

            # Create snowflakes
            flakes = []
            
            # Reset speed 
            Branches.changeY = 6 # 6
            Snowflake.changeY = 6
            Branches.direction = "up"
            
            

            paintEverything()

            scorer = Scorer(window)
            record_checked = False
            

        pygame.display.flip()




pygame.quit()  # Stops program
os._exit(0)  # Stops program for mac OS users

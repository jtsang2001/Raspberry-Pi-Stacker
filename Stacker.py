#
# Stacker.py
#
# Stacker game for the senseHat raspberry PI
#
# Nicholas Imperius
# Jimmy Tsang
# Kristopher Poulin
#

from sense_emu import SenseHat, ACTION_PRESSED
from array import *

import time

# CONSTANTS
SPEED = 0.2
WHITE = (0,0,0)
CYAN = (129, 240, 255)

#
# --MoveBlock Function--
# moves the block one pixel to left or right and returns the new direction
#
def moveBlock(direction, currentX):
    if direction == "right":
        if currentX[7] == 1:
            direction = "left"
            for i in range(0, (len(currentX)), 1):
                if currentX[i] == 1:
                    currentX[i-1] = 1
                    currentX[i] = 0
        elif currentX[0] == 1:
            direction = "right"
            for i in range((len(currentX)-1), 0, -1):
                if currentX[i] == 1:
                    currentX[i+1] = 1
                    currentX[i] = 0
        else:
            for i in range((len(currentX)-1), 0, -1):
                if currentX[i] == 1:
                    currentX[i+1] = 1
                    currentX[i] = 0
    elif direction == "left":
        if currentX[7] == 1:
            direction = "left"
            for i in range(0, (len(currentX)), 1):
                if currentX[i] == 1:
                    currentX[i-1] = 1
                    currentX[i] = 0
        elif currentX[0] == 1:
            direction = "right"
            for i in range((len(currentX)-1), -1, -1):
                if currentX[i] == 1:
                    currentX[i+1] = 1
                    currentX[i] = 0
        else:
            for i in range(0, (len(currentX)), 1):
                if currentX[i] == 1:
                    currentX[i-1] = 1
                    currentX[i] = 0
    return direction
# end of moveBlock

#
# --normalMode Function--
#
def normalMode(hat):
    #default starting location
    currentRow = 7
    currentX = [0,0,1,1,1,0,0,0]
    
    #default moving direction
    direction = "left"

    #default taken blocks
    stacked = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]
    
    # game loop
    gameLoop = True
    
    while gameLoop:
        #Increase Difficulty as you get Higher
        if currentRow > 4:
            time.sleep(SPEED)
        elif currentRow > 2:
            time.sleep(SPEED * 0.8)
        else:
            time.sleep(SPEED * 0.6)
        
        #reset clicked flag
        clicked = False
        
        # Register click events and increment row system.
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
                clicked = True
                if currentRow == 0:
                    gameLoop = False
                else:
                    currentRow -= 1
                
        # Updates array to remove the blocks that are not on top of each other
        if (currentRow+1) < 7 and clicked == True:
            for i in range(len(stacked[currentRow+2])):
                if currentX[i] != stacked[currentRow+2][i]:
                    currentX[i] = 0
                    stacked[currentRow+1][i] = 0
        
        #Checks if game is done
        if currentX.count(1) == 0:
            hat.show_message("Oh No! You lost.", scroll_speed = 0.06)
            break
        elif gameLoop == False and currentX.count(1) != 0:
            hat.show_message("CONGRATS! You won!", scroll_speed = 0.06)
            break
        elif gameLoop == False and currentX.count(1) == 0:
            hat.show_message("Oh No! You lost.", scroll_speed = 0.06)
            break
            
        
        # Move the block and keep track of direction
        direction = moveBlock(direction, currentX)
        
        # Adjust screen of pixels
        index = 0
        for x in currentX:
            if x == 0:
                hat.set_pixel(index, currentRow, WHITE)
                stacked[currentRow][index] = 0
            elif x == 1:
                hat.set_pixel(index, currentRow, CYAN)
                stacked[currentRow][index] = 1
            index += 1
        
        # update previous line if need to remove stuff
        index = 0
        if clicked == True:
            for x in stacked[currentRow+1]:
                if x == 0:
                    hat.set_pixel(index, currentRow+1, WHITE)
                elif x == 1:
                    hat.set_pixel(index, currentRow+1, CYAN)
                index += 1
# end of normalMode

#
# --Main Function--
#
def main():
    hat = SenseHat()
    hat.clear()
    
    #default taken blocks
    startScreen = [[0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,1,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,1,1,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0]]
    
    cursorSpot = 2
    
    checker = 0
    while True:
        time.sleep(0.2)
        checker +=1
        
        for i in range(len(startScreen)):
            for j in range(len(startScreen[i])):
                if startScreen[i][j] == 1:
                    hat.set_pixel(j, i, 244, 208, 63)
                    
        if checker % 2:
            hat.set_pixel(5, cursorSpot, 142, 68, 173)
        else:
            hat.set_pixel(5, 2, WHITE)
            hat.set_pixel(5, 4, WHITE)
            hat.set_pixel(5, 6, WHITE)
            
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
                if event.direction == "up":
                    if cursorSpot == 2:
                        cursorSpot = 6
                    elif cursorSpot == 4:
                        cursorSpot = 2
                    else:
                        cursorSpot = 4
                elif event.direction == "down":
                    if cursorSpot == 2:
                        cursorSpot = 4
                    elif cursorSpot == 4:
                        cursorSpot = 6
                    else:
                        cursorSpot = 2
                elif event.direction == "middle":
                    if cursorSpot == 2:
                        hat.clear()
                        #hat.show_message("NORMAL MODE...GO!", scroll_speed=0.07)
                        normalMode(hat)
                        hat.clear()
                    elif cursorSpot == 4:
                        pass
                        #hat.clear()
                        #hat.show_message("TIME TRIAL MODE...GO!")
                        #timeTrialMode(hat)
                    elif cursorSpot == 6:
                        pass
                        #hat.clear()
                        #hat.show_message("ENDLESS MODE...GO!")
                    # lowlight line every 5 lines to show its going down
                        #endlessMode(hat)
# end of main

if __name__ == "__main__":
    main()
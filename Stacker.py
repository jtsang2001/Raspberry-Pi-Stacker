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
SPEED_MULTIPLIER = 0.1
WHITE = (0,0,0)
CYAN = (10,255,255)

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
    stacked = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    # game loop
    while True:
        time.sleep(SPEED)
        
        #reset clicked flag
        clicked = False
        
        # Register click events and increment row system.
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
                currentRow -= 1
                clicked = True
            
        # Updates array to remove the blocks that are not on top of each other
        if (currentRow+1) < 7 and clicked == True:
            for i in range(len(stacked[currentRow+2])):
                if currentX[i] != stacked[currentRow+2][i]:
                    currentX[i] = 0
                    stacked[currentRow+1][i] = 0
        
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
    
    hat.show_message("Welcome!", text_colour=CYAN, scroll_speed=0.1)
    
    normalMode(hat)
# end of main

if __name__ == "__main__":
    main()
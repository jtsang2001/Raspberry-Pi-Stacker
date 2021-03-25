#
# normalMode.py
#
# Normal Mode functionality
#
# Nicholas Imperius
# Jimmy Tsang
# Kristopher Poulin
#

from sense_emu import SenseHat, ACTION_PRESSED

import time
from datetime import timedelta

from StackerUpdater import moveBlock, updatePrevLine

# CONSTANTS
SPEED = 0.2
CLEAR = (0,0,0)
CYAN = (129, 240, 255)
YELLOW = (244, 208, 63)
RED = (255, 124, 126)

#
# --normalMode Function--
#
def normalMode(currentRow, currentX, direction, stacked, hat):
    # game loop
    gameLoop = True
    
    while gameLoop:
        #Increase Difficulty as you get Higher
        if currentRow > 4:
            time.sleep(SPEED)
        elif currentRow > 1:
            time.sleep(SPEED * 0.7)
        else:
            time.sleep(SPEED * 0.5)
        
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
            time.sleep(0.5)
            hat.show_message("You lost.", scroll_speed = 0.05)
            break
        elif gameLoop == False and currentX.count(1) != 0:
            time.sleep(0.5)
            hat.show_message("You won!", scroll_speed = 0.05)
            break
        elif gameLoop == False and currentX.count(1) == 0:
            time.sleep(0.5)
            hat.show_message("You lost.", scroll_speed = 0.05)
            break
            
        
        # Move the block and keep track of direction
        direction = moveBlock(direction, currentX)
        
        # Adjust screen of pixels
        index = 0
        for x in currentX:
            if x == 0:
                hat.set_pixel(index, currentRow, CLEAR)
                stacked[currentRow][index] = 0
            elif x == 1:
                if currentRow > 4:
                    hat.set_pixel(index, currentRow, CYAN)
                    stacked[currentRow][index] = 1
                elif currentRow > 1:
                    hat.set_pixel(index, currentRow, YELLOW)
                    stacked[currentRow][index] = 1
                else:
                    hat.set_pixel(index, currentRow, RED)
                    stacked[currentRow][index] = 1
            index += 1
        
        # update previous line if need to remove stuff
        if clicked == True:
            updatePrevLine(stacked, currentRow, hat)
# end of normalMode
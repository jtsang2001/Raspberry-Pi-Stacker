#
# endlessMode.py
#
# Endless Mode functionality
#
# Nicholas Imperius
# Jimmy Tsang
# Kristopher Poulin
#

from sense_emu import ACTION_PRESSED

import time

from StackerUpdater import moveBlock, updatePrevLine

# CONSTANTS
SPEED = 0.2
CLEAR = (0,0,0)
CYAN = (129, 240, 255)
LIGHT_CYAN = (27, 70, 75)

#
# --endlessMode Function--
#
def endlessMode(currentRow, currentX, direction, stacked, hat):
    # game loop
    gameLoop = True
    
    #Keeps track of rows completed
    numberOfCompletedRows = 0
    
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
                numberOfCompletedRows += 1
                clicked = True
                if currentRow != 0:
                    currentRow -= 1                
                
        # Updates array to remove the blocks that are not on top of each other
        if (currentRow+1) < 7 and clicked == True:
            for i in range(len(stacked[currentRow+2])):
                if currentX[i] != stacked[currentRow+2][i]:
                    currentX[i] = 0
                    stacked[currentRow+1][i] = 0
        
        #Checks if game is done
        if currentX.count(1) == 0:
            numberOfCompletedRows -= 1
            hat.show_message("Score: " + str(numberOfCompletedRows) + " rows.", scroll_speed = 0.05)
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
                hat.set_pixel(index, currentRow, CYAN)
                stacked[currentRow][index] = 1
            index += 1
        
        # update previous line if need to remove stuff
        if clicked == True:
            tempStacked = stacked
#             if currentRow == 0:
#                 stacked[0] = [0,0,0,0,0,0,0,0]
#                 stacked[1] = tempStacked[0]
#                 stacked[2] = tempStacked[1]
#                 stacked[3] = tempStacked[2]
#                 stacked[4] = tempStacked[3]
#                 stacked[5] = tempStacked[4]
#                 stacked[6] = tempStacked[5] # might need to make a different update line that just shifts
#                 stacked[7] = tempStacked[6] # the array every iteration
#                 
#                 for i in range(len(stacked) - 1):
#                     for j in range(len(stacked[i]) - 1):
#                         if stacked[i][j] == 0:
#                             hat.set_pixel(j, i, CLEAR)
#                         elif stacked[i][j] == 1:
#                             hat.set_pixel(j, i, CYAN)
#             else:
            updatePrevLine(stacked, currentRow, hat)
# end of endlessMode
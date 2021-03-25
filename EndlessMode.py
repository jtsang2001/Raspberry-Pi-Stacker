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

from StackerUpdater import moveBlock, updatePrevLine, lowerStack

# CONSTANTS
CLEAR = (0,0,0)
CYAN = (129, 240, 255)
LIGHT_CYAN = (27, 70, 75)
LIGHT_YELLOW = (71, 75, 27)
LIGHT_RED = (75, 27, 28)

#
# --endlessMode Function--
#
def endlessMode(currentRow, currentX, direction, stacked, hat):
    # game loop
    gameLoop = True
    
    speedFlag = True
    
    speed = 0.2
    
    #Keeps track of rows completed
    numberOfCompletedRows = 0
    
    while gameLoop:
        if speedFlag:
            print(speed)
        #Increase Difficulty as you get Higher
        if numberOfCompletedRows > 10 and speedFlag == True:
            speed -= 0.00035
        elif currentRow == 5 and speedFlag == True:
            speed = speed
        elif currentRow == 3 and speedFlag == True:
            speed = speed * 0.8
        elif currentRow == 1 and speedFlag == True:
            speed = speed * (0.6 / 0.8)
#         elif currentRow == 0 and speedFlag == True:
#             speed = speed * (0.5 / 0.6)
        
        time.sleep(speed)
        speedFlag = False
        
        #reset clicked flag
        clicked = False
        
        # Register click events and increment row system.
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
                speedFlag = True
                numberOfCompletedRows += 1
                clicked = True
                if currentRow != 0:
                    currentRow -= 1
                
        # Updates array to remove the blocks that are not on top of each other
        if (currentRow+1) < 7 and clicked == True:
            if numberOfCompletedRows < 8:
                for i in range(len(stacked[currentRow+2])):
                    if currentX[i] != stacked[currentRow+2][i]:
                        currentX[i] = 0
                        stacked[currentRow+1][i] = 0
            else:
                fakeCurrentX = [0,0,0,0,0,0,0,0]
                for i in range(len(stacked[currentRow])):
                    if currentX[i] != stacked[1][i]:
                        currentX[i] = 0
                        fakeCurrentX[i] = 0
                    else:
                        fakeCurrentX[i] = stacked[0][i]
                stacked[7] = stacked[6]
                stacked[6] = stacked[5]
                stacked[5] = stacked[4]
                stacked[4] = stacked[3]
                stacked[3] = stacked[2]
                stacked[2] = stacked[1]
                stacked[1] = fakeCurrentX

        #Checks if game is done
        if currentX.count(1) == 0:
            numberOfCompletedRows -= 1
            hat.show_message("Score: " + str(numberOfCompletedRows) + " rows.", scroll_speed = 0.05)
            break
        
        # Move the block and keep track of direction
        direction = moveBlock(direction, currentX)

        # Adjust current moving row of pixels
        index = 0
        for x in currentX:
            if x == 0:
                if numberOfCompletedRows > 6:
                    if numberOfCompletedRows % 3 == 0:
                        hat.set_pixel(index, currentRow, LIGHT_CYAN)
                        stacked[currentRow][index] = 0
                    elif numberOfCompletedRows % 3 == 1:
                        hat.set_pixel(index, currentRow, LIGHT_YELLOW)
                        stacked[currentRow][index] = 0
                    elif numberOfCompletedRows % 3 == 2:
                        hat.set_pixel(index, currentRow, LIGHT_RED)
                        stacked[currentRow][index] = 0
                else:
                    hat.set_pixel(index, currentRow, CLEAR)
                    stacked[currentRow][index] = 0
            elif x == 1:
                hat.set_pixel(index, currentRow, CYAN)
                stacked[currentRow][index] = 1
            index += 1

        # update previous line if need to remove stuff
        if clicked == True and numberOfCompletedRows < 7:
            updatePrevLine(stacked, currentRow, hat)
        elif clicked == True and numberOfCompletedRows > 6:
            if numberOfCompletedRows % 3 == 0:
                lowerStack(stacked, hat, LIGHT_CYAN)
            elif numberOfCompletedRows % 3 == 1:
                lowerStack(stacked, hat, LIGHT_YELLOW)
            elif numberOfCompletedRows % 3 == 2:
                lowerStack(stacked, hat, LIGHT_RED)
            
# end of endlessMode

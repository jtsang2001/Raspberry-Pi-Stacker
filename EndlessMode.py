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
    # Initialize variables to be used in the Game Loop
    gameLoop = True
    speedFlag = True
    speed = 0.2
    
    # Keeps track of rows completed
    numberOfCompletedRows = 0
    
    # Start the game loop, loop exits when user either wins or loses
    while gameLoop:
        # Increase Difficulty as you get Higher
        if numberOfCompletedRows > 10 and speedFlag == True:
            speed -= 0.001
        elif currentRow == 5 and speedFlag == True:
            speed = speed
        elif currentRow == 3 and speedFlag == True:
            speed = speed * 0.8
        elif currentRow == 1 and speedFlag == True:
            speed = speed * (0.6 / 0.8)
        
        # Sleep for the amount of time, controls speed of the stacker block
        time.sleep(speed)
        
        # speedFlag is used when the button has been pressed to increment the
        #  speed, every loop we set to false before the event loop 
        speedFlag = False
        
        # Reset clicked flag
        clicked = False
        
        # Register click events and increment row system.
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
                speedFlag = True
                numberOfCompletedRows += 1
                clicked = True
                # Once we get to the top row, we can no longer decrement
                if currentRow != 0:
                    currentRow -= 1
                
        # Updates array to remove the blocks that are not on top of each other
        #  Since this happens after the click we need to search the row that
        #  is 2 rows below since we have moved up by one. We compare the current
        #  row and that row that was 2 below to see if they are the same or
        #  different, if different we update the array to remove it when we
        #  update the screen later on in this game loop
        if (currentRow+1) < 7 and clicked == True:
            if numberOfCompletedRows < 8:
                for i in range(len(stacked[currentRow+2])):
                    if currentX[i] != stacked[currentRow+2][i]:
                        currentX[i] = 0
                        stacked[currentRow+1][i] = 0
            # If we are at the top row, we need to shift the entire array down
            #  by one so we can show that they are moving "up"
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

        # Checks if game is done, this happens when currentX is full of 0's
        if currentX.count(1) == 0:
            # Need to decrement rows since we increment at the start of the loop
            numberOfCompletedRows -= 1
            # Print message to user displaying the number of rows completed
            hat.show_message("Your Score: " + str(numberOfCompletedRows) + " rows.", scroll_speed = 0.05)
            # break out of game loop
            break
        
        # Call the moveBlock function in StackerUpdater.py to move the block and return a new direction
        direction = moveBlock(direction, currentX)

        # Adjust current moving row of pixels
        # Will print a different colour block depending on what row they are on
        index = 0
        for x in currentX:
            if x == 0:
                if numberOfCompletedRows > 6:
                    if numberOfCompletedRows % 3 == 0:
                        stacked[currentRow][index] = 0
                        if numberOfCompletedRows % 2 == 1:
                            hat.set_pixel(index, currentRow, LIGHT_CYAN)
                        else:
                            hat.set_pixel(index, currentRow, CLEAR)
                    elif numberOfCompletedRows % 3 == 1:
                        stacked[currentRow][index] = 0
                        if numberOfCompletedRows % 2 == 1:
                            hat.set_pixel(index, currentRow, LIGHT_CYAN)
                        else:
                            hat.set_pixel(index, currentRow, CLEAR)
                    elif numberOfCompletedRows % 3 == 2:
                        stacked[currentRow][index] = 0
                        if numberOfCompletedRows % 2 == 1:
                            hat.set_pixel(index, currentRow, LIGHT_CYAN)
                        else:
                            hat.set_pixel(index, currentRow, CLEAR)
                else:
                    hat.set_pixel(index, currentRow, CLEAR)
                    stacked[currentRow][index] = 0
            elif x == 1:
                hat.set_pixel(index, currentRow, CYAN)
                stacked[currentRow][index] = 1
            index += 1

        # This is where we remove the unwanted blocks from the screen.
        # Calls the updatePrevLine function in StackerUpdater.py
        if clicked == True and numberOfCompletedRows < 7:
            updatePrevLine(stacked, currentRow, hat)
        elif clicked == True and numberOfCompletedRows > 6:
            if numberOfCompletedRows % 3 == 0:
                lowerStack(stacked, hat, numberOfCompletedRows)
            elif numberOfCompletedRows % 3 == 1:
                lowerStack(stacked, hat, numberOfCompletedRows)
            elif numberOfCompletedRows % 3 == 2:
                lowerStack(stacked, hat, numberOfCompletedRows)
# end of endlessMode

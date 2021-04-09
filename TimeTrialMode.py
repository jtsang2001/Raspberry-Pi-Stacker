#
# timeTrialMode.py
#
# Time Trial Mode functionality
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
# --timeTrialMode Function--
#
def timeTrialMode(currentRow, currentX, direction, stacked, hat):
    # Start the timer
    startTime = time.monotonic()

    # Variable to keep track of gameLoop
    gameLoop = True
    
    # Start the game loop, loop exits when user either wins or loses
    while gameLoop:
        #Increase Difficulty as you get Higher
        if currentRow > 5:
            time.sleep(SPEED * 0.95)
        elif currentRow > 2:
            time.sleep(SPEED * 0.7)
        else:
            time.sleep(SPEED * 0.5)
        
        # Reset clicked flag
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
        #  Since this happens after the click we need to search the row that
        #  is 2 rows below since we have moved up by one. We compare the current
        #  row and that row that was 2 below to see if they are the same or
        #  different, if different we update the array to remove it when we
        #  update the screen later on in this game loop
        if (currentRow+1) < 7 and clicked == True:
            for i in range(len(stacked[currentRow+2])):
                if currentX[i] != stacked[currentRow+2][i]:
                    currentX[i] = 0
                    stacked[currentRow+1][i] = 0
        
        # Checks if game is done
        #  If it is, stop timer, get difference in time and then display a Win or Lose with the time it took
        if currentX.count(1) == 0:
            endTime = time.monotonic()
            totalTime = timedelta(seconds=endTime - startTime)
            time.sleep(0.5)
            hat.show_message("You lost. Time: " + str(totalTime.total_seconds())[:4] + " sec", scroll_speed = 0.05)
            break
        elif gameLoop == False and currentX.count(1) != 0:
            endTime = time.monotonic()
            totalTime = timedelta(seconds=endTime - startTime)
            time.sleep(0.5)
            hat.show_message("You won! Time: " + str(totalTime.total_seconds())[:4] + " sec", scroll_speed = 0.05)
            break
        elif gameLoop == False and currentX.count(1) == 0:
            endTime = time.monotonic()
            totalTime = timedelta(seconds=endTime - startTime)
            time.sleep(0.5)
            hat.show_message("You lost. Time: " + str(totalTime.total_seconds())[:4] + " sec", scroll_speed = 0.05)
            break
            
        
        # Call the moveBlock function in StackerUpdater.py to move the block and return a new direction
        direction = moveBlock(direction, currentX)
        
        # Adjust the screen to colour or uncolour and pixels that need to be set or unset
        index = 0
        for x in currentX:
            if x == 0:
                hat.set_pixel(index, currentRow, CLEAR)
                stacked[currentRow][index] = 0
            elif x == 1:
                if currentRow > 5:
                    hat.set_pixel(index, currentRow, CYAN)
                    stacked[currentRow][index] = 1
                elif currentRow > 2:
                    hat.set_pixel(index, currentRow, YELLOW)
                    stacked[currentRow][index] = 1
                else:
                    hat.set_pixel(index, currentRow, RED)
                    stacked[currentRow][index] = 1
            index += 1
        
        # This is where we remove the unwanted blocks from the screen.
        # Calls the updatePrevLine function in StackerUpdater.py
        if clicked == True:
            updatePrevLine(stacked, currentRow, hat)
# end of timeTrialMode
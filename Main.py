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

from NormalMode import normalMode
from TimeTrialMode import timeTrialMode
from EndlessMode import endlessMode

# CONSTANTS
SPEED = 0.2
CLEAR = (0,0,0)
YELLOW = (244, 208, 63)
PINK = (142, 68, 173)

#
# --Main Function--
#
def main():
    # Declare the hat variable that will be used to control the sense hat emulator
    hat = SenseHat()
    
    # Clear the Screen
    hat.clear()
    
    # Default layout of the start screen, with 1's representing the blocks to colour
    startScreen = [[0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,1,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,1,1,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0]]
    
    # Starting position of selector 
    cursorSpot = 2
    
    # Game Loop to run until program is quit
    checker = 0
    while True:
        # Sleep function allows the cursor to blink
        time.sleep(SPEED)
        
        # Print out the start screen layout
        for i in range(len(startScreen)):
            for j in range(len(startScreen[i])):
                if startScreen[i][j] == 1:
                    hat.set_pixel(j, i, YELLOW)
        
        # Allows us to show either a pink or clear dot for the selector
        checker +=1
        if checker % 2:
            hat.set_pixel(5, cursorSpot, PINK)
        else:
            hat.set_pixel(5, 2, CLEAR)
            hat.set_pixel(5, 4, CLEAR)
            hat.set_pixel(5, 6, CLEAR)
        
        # event checker, when joystick event is pressed
        #  it will check the location of the cursor and
        #  do the appropriate functions
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
                # Default starting location
                currentRow = 7
                currentX = [0,0,1,1,1,0,0,0]
                
                # Default moving direction
                direction = "left"

                # Default stacked array to represent the 
                stacked = [[0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0]]
                
                # Depending on the direction change where the cursor goes
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
                    # If we are on the top position, show message and start Normal Mode
                    if cursorSpot == 2:
                        hat.clear()
                        hat.show_message("Normal Mode...GO!", scroll_speed=0.06)
                        normalMode(currentRow, currentX, direction, stacked, hat)
                        hat.clear()
                    # If we are on the middle position, show message and start Time Trial Mode
                    elif cursorSpot == 4:
                        hat.clear()
                        hat.show_message("Time Trial Mode...GO!", scroll_speed=0.06)
                        timeTrialMode(currentRow, currentX, direction, stacked, hat)
                        hat.clear()
                    # If we are on the bottom position, show message and start Endless Mode
                    elif cursorSpot == 6:
                        hat.clear()
                        hat.show_message("Endless Mode...GO!", scroll_speed=0.06)
                        endlessMode(currentRow, currentX, direction, stacked, hat)
                        hat.clear()
# End of main

# Run Main function
if __name__ == "__main__":
    main()
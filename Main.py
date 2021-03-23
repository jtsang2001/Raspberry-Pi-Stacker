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
CYAN = (129, 240, 255)

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
    
    #Where to start the cursor on the welcome screen
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
            hat.set_pixel(5, 2, CLEAR)
            hat.set_pixel(5, 4, CLEAR)
            hat.set_pixel(5, 6, CLEAR)
            
        events = hat.stick.get_events()
        for event in events:
            if event.action == ACTION_PRESSED:
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
                        normalMode(currentRow, currentX, direction, stacked, hat)
                        hat.clear()
                    elif cursorSpot == 4:
                        hat.clear()
                        #hat.show_message("TIME TRIAL MODE...GO!")
                        timeTrialMode(currentRow, currentX, direction, stacked, hat)
                        hat.clear()
                    elif cursorSpot == 6:
                        hat.clear()
                        #hat.show_message("ENDLESS MODE...GO!")
                        endlessMode(currentRow, currentX, direction, stacked, hat)
                        hat.clear()
# end of main

if __name__ == "__main__":
    main()
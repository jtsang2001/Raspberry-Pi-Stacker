#
# stackerUpdater.py
#
# Provides functions that update variables/screen
#
# Nicholas Imperius
# Jimmy Tsang
# Kristopher Poulin
#

# CONSTANTS
CLEAR = (0,0,0)
CYAN = (129, 240, 255)
LIGHT_CYAN = (37, 62, 65)

#
# --MoveBlock Function--
#   - moves the block one pixel to left or right and returns the new direction
#
def moveBlock(direction, currentX):
    # Check if direction is currently right or left
    if direction == "right":
        # Get the position of the block and either move it once more in the same
        #  direction or turn it around and move the other way
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
    # Check if direction is currently right or left
    elif direction == "left":
        # Get the position of the block and either move it once more in the same
        #  direction or turn it around and move the other way
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
                    
    # Return the direction in case it has been changed
    return direction
# end of moveBlock

#
# --updatePrevLine Function--
#   - clears the pixel that needs to be removed
#
def updatePrevLine(stacked, currentRow, hat):
    index = 0
    # Increments through one row that needs to be looked at
    for x in stacked[currentRow+1]:
        if x == 0:
            hat.set_pixel(index, currentRow+1, CLEAR)
        index += 1
# end of updatePrevLine

#
# --lowerStack Function--
#   - Clears any pixels that arent set when the board is shift down
#
def lowerStack(stacked, hat, index):
    rowIndex = index
    # Go through the entire stackedArray and check to see what needs to be changed
    for i in range(1, len(stacked)):
        for j in range(0, len(stacked[i])):
            if stacked[i][j] == 0:
                if rowIndex % 2 == 0:
                    hat.set_pixel(j, i, LIGHT_CYAN)
                else:
                    hat.set_pixel(j, i, CLEAR)
        rowIndex += 1
#end of lowerStack

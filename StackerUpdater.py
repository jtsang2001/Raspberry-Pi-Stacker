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
# --updatePrevLine Function--
#
def updatePrevLine(stacked, currentRow, hat):
    index = 0
    for x in stacked[currentRow+1]:
        if x == 0:
            hat.set_pixel(index, currentRow+1, WHITE)
        elif x == 1:
            hat.set_pixel(index, currentRow+1, CYAN)
        index += 1
# end of updatePrevLine

# This program handles command line arguments to draw stars using
# information taken from a file, and optionally writes the names of named stars.
# It then prompts for valid constellation files and draws them.
# Bonus: draws a box with 15-pixel padding around each constellation,
# writes the name of the constellation above, and writes the constellation name
# and min and max x and y to a file.

# For constellation data, refer to example files in this folder

import turtle
import os
import sys

# Defining constants:
WIDTH = 600
HEIGHT = 600
AXISCOLOUR = "blue"
BACKGROUNDCOLOUR = "black"
STARCOLOUR = "white"
STARCOLOUR2 = "grey"


#
# Sets up the drawing window
# Parameters: none
# Usage -> setup()
# Returns: pointer used in the rest of the program
#


def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer.hideturtle()
    screen.delay(delay=0)
    turtle.bgcolor(BACKGROUNDCOLOUR)
    pointer.up()
    return pointer

#
# Draws the x-axis and y-axis in blue, incrementing by 0.25
# Parameters: pointer
# Usage -> drawXAxis(pointer)
# Returns: nothing
#

def drawAxes(pointer):

# Drawing the X-Axis:

    # Goes to the negative end of the x-axis
    pointer.penup()
    pointer.goto(0, HEIGHT/2)
    pointer.pendown()
    pointer.pencolor(AXISCOLOUR)

    # define local variables to be used
    pixelsPerStep = 75
    numberOfSteps = 8
    tickLength = 10
    tickNumber = -1
    tickNumberLocation = 15

    # for loop to draw each increment and tick
    for i in range(0,numberOfSteps+1):
        pointer.left(90)
        pointer.forward(tickLength/2)
        if tickNumber != 0:
            pointer.penup()
            pointer.forward(tickNumberLocation)
            pointer.write(str(tickNumber), font = 3)
            pointer.back(tickNumberLocation)
            pointer.pendown()
        pointer.back(tickLength)
        pointer.forward(tickLength/2)
        pointer.right(90)
        tickNumber += 0.25
        if tickNumber < 1.25:
            pointer.forward(pixelsPerStep)

# Now drawing the Y-Axis:

    # Goes to the negative end of the y-axis
    pointer.penup()
    pointer.goto(WIDTH/2, 0)
    pointer.pendown()
    pointer.pencolor(AXISCOLOUR)

    # define local variables to be used
    pixelsPerStep = 75
    numberOfSteps = 8
    tickLength = 10
    tickNumber = -1
    tickNumberLocation = 15

    # for loop to draw each increment and tick
    for i in range(0, numberOfSteps+1):
        pointer.setheading(0)
        pointer.pendown()
        pointer.forward(tickLength/2)
        pointer.penup()
        pointer.forward(tickNumberLocation)
        if tickNumber != 0:
            pointer.write(str(tickNumber), font = 3)
        pointer.back(tickLength + tickNumberLocation)
        pointer.pendown()
        pointer.forward(tickLength/2)
        pointer.left(90)
        tickNumber += 0.25
        if tickNumber < 1.25:
            pointer.forward(pixelsPerStep)

#
# Reads the given stars-location-file and compiles a list with tuples of (x,y,magnitude)
# for each star, and a dictionary with all the names of the stars as keys and their
# (x,y,magnitude) tuples as values. It also prints to the console the names of the stars with
# their location and magnitude.
# Parameters: fileName (the name of the given stars-location-file)
# Usage -> readStarFile(fileName)
# Returns: allStarsList (list of all the location and mag tuples of each star)
#          starNamesDict (dictionary of all named stars and their tuples)
#

def readStarFile(fileName):

    # initializing the list and dictionary to be returned at the end of the function, and other local variables used
    allStarsList = []
    starNamesDict = {}
    xIndex = 0
    yIndex = 1
    magIndex = 4
    nameIndex = 6
    numOfItems = 7

    # try-except block to catch errors when opening the file
    try:
        fileReader = open(fileName, "r")
    except:
        print("Error: cannot open file")
        sys.exit(1)
    else:

        # loop through each line in the file (each star) and save the x, y, and magnitude values in a tuple.
        for line in fileReader:
            line = line.strip()
            lineList = line.split(",")

            # check to make sure there are a correct number of entries in the star info line
            if len(lineList) != numOfItems:
                print("Error: wrong number of entries")
                sys.exit(1)

            # for loop to save the x, y, and magnitude values to variables
            for item in lineList:

                # x-value:
                if lineList.index(item) == xIndex:
                    try:
                        float(item)
                    except:
                        print("Error: entry was of wrong type")
                        sys.exit(1)
                    xCoor = float(item)

                # y-value:
                elif lineList.index(item) == yIndex:
                    try:
                        float(item)
                    except:
                        print("Error: entry was of wrong type")
                        sys.exit(1)
                    yCoor = float(item)

                # magnitude:
                elif lineList.index(item) == magIndex:
                    try:
                        float(item)
                    except:
                        print("Error: entry was of wrong type")
                        sys.exit(1)
                    mag = float(item)

            # Put the x,y, and magnitude values into a tuple and append it to the all stars list
            starTuple = (xCoor, yCoor, mag)
            allStarsList.append(starTuple)

            # for loop to save the name of the constellation (if there is one) to the star names dictionary
            for item in lineList:

                if lineList.index(item) == nameIndex:

                    namesList = item.split(";")
                    for n in namesList:
                        if n != "":
                            starNamesDict[n] = starTuple
                            print(f"{n} is at {xCoor, yCoor} with magnitude {mag}")

    # try-except block to catch errors when closing the file
    try:
        fileReader.close()
    except:
        print("Error: could not close file")
        sys.exit(1)

    return allStarsList, starNamesDict


#
# Draws all the stars given in the stars-location-file in gray, then loops back over
# named stars in white. If "-names" was a command line argument, will write the
# names of the named stars.
#
# Parameters:  allStarsList: list of all the (x,y,magnitude) tuples of each star.
#              starNamesDict: dictionary with names as keys and tuples as values.
#              pointer: the turtle drawing object
#              names: boolean determined in main() function, evaluates to True
#                     only if "-names" was a command line argument.
#
# Usage -> drawStars(allStarsList, starNamesDict, pointer, True)
#
# Returns: nothing
#
       
def drawStars(allStarsList, starNamesDict, pointer, names):

    # draw all stars in gray
    pointer.color(STARCOLOUR2)
    for tupleItem in allStarsList:
        magnitude = tupleItem[2]
        radius = (10/(magnitude+2))/2
        pointer.penup()
        pixelX = (WIDTH/2) + (WIDTH/2) * tupleItem[0]
        pixelY = (HEIGHT/2) + (HEIGHT/2) * tupleItem[1]
        pointer.goto(pixelX, pixelY)
        pointer.pendown()
        pointer.begin_fill()
        pointer.circle(radius)
        pointer.end_fill()

    # draw only named stars in white
    pointer.color(STARCOLOUR)
    firstStarNames = []
    for key in starNamesDict:
        tupleItem = starNamesDict[key]

        # only write the first name of the star (so that there isn't overlap when a star has multiple names)
        if tupleItem not in firstStarNames:
            firstStarNames.append(tupleItem)

            # draw the star in white
            magnitude = tupleItem[2]
            radius = (10/(magnitude+2))/2
            pointer.penup()
            pixelX = (WIDTH/2) + (WIDTH/2) * tupleItem[0]
            pixelY = (HEIGHT/2) + (HEIGHT/2) * tupleItem[1]
            pointer.goto(pixelX, pixelY)
            pointer.pendown()
            pointer.begin_fill()
            pointer.circle(radius)
            pointer.end_fill()

            # if "-names" was given in the command line, write the names of the named stars
            if names == True:        
                pointer.write(key, font=("Arial", 5, "normal"))

#
# Find the colour of the constellation using modulus (%)
# Parameters: counter (the number of the constellation loop in the main() function)
# Usage -> getColour(1)
# Returns: a string containing either red, green, or yellow
#

def getColour(counter):
    if counter%3 == 2:
        constellationColour = "green"
        return constellationColour
    elif counter%3 == 1:
        constellationColour = "yellow"
        return constellationColour
    else:
        constellationColour = "red"
        return constellationColour
       
#
# Reads the given constellation-file and creates a list containing tuples of two stars which together
# make up one edge of the constellation. It then prints to the console the name of the constellation
# as well as a list of the stars contained in that constellation.
#
# Parameter: constellationFile (the file containing the constellation name and pairs of stars)
# Usage -> readConstellationFile(BigDipper.dat)
#
# Returns: constellationName (the name of the constellation)
#          constStarList (a list of the star pair tuples in the given constellation)
#

def readConstellationFile(constellationFile):

    # initialize the lists used in this function
    constStarList = []
    uniqueStarList = []

    # try-except block to catch errors while opening the file
    try:
        fileReader = open(constellationFile)
    except:
        print("Error: could not open file")
        sys.exit(1)
    else:

        # try-except block to catch any errors while reading the file
        try:
            constellationName = fileReader.readline().strip()

            # for loop to save each pair of stars as a tuple
            for line in fileReader:
                line = line.strip()
                lineList = line.split(",")
                listLength = 2

                # make sure that there are the right number of entries (two stars)
                if len(lineList) != listLength:
                    print("Error: wrong number of entries")
                    sys.exit(1)

                # save each pair of stars in a tuple and append it to the constellation star list
                starTuple = (lineList[0], lineList[1])
                constStarList.append(starTuple)

                # add all unique stars to the unique star list, which will be used when printing to the console
                for star in lineList:
                    if star not in uniqueStarList:
                        uniqueStarList.append(star)

            # print the constellation name and the stars it contains
            print(f"{constellationName} constellation contains {uniqueStarList}")
       

        except:
            print("Error: something went wrong while reading the file")
            sys.exit(1)

    # try-except block to catch errors while closing the file
    try:
        fileReader.close()
    except:
        print("Error: could not close the constellation file")
        sys.exit(1)
       
    return constellationName, constStarList


#
# Draws the constellation in the colour determined by getColour() by looping through the
# star pair tuples found in readConstellationFile().
#
# Parameters:
# pointer: the turtle drawing object
# namesDictAll: a dictionary with all the names of stars as keys and the (x,y,mag) tuples as values.
# constStarList: a list containing star pair tuples for each edge in the constellation.
# constellationName: the name of the constellation as given in the constellation file.
# constellationColour: the colour returned by the getColour() function.
#
# Usage -> drawConstellation(pointer, namesDictAll, constStarList, 'BIG DIPPER', 'green')
#
# Returns: nothing
#
           
def drawConstellation(pointer, namesDictAll, constStarList, constellationName, constellationColour):

    # set the pencolor to either green, red, or yellow
    pointer.color(constellationColour)

    # for loop drawing each edge using star pair tuples
    for edge in constStarList:

        firstXYmag = namesDictAll[edge[0]]
        secondXYmag = namesDictAll[edge[1]]

        firstXY = firstXYmag[0:2]
        secondXY = secondXYmag[0:2]

        # calculate the pixel locations of the coordinate points given
        firstXpixel = (WIDTH/2) + (WIDTH/2) * firstXY[0]
        firstYpixel = (HEIGHT/2) + (HEIGHT/2) * firstXY[1]
        secondXpixel = (WIDTH/2) + (WIDTH/2) * secondXY[0]
        secondYpixel = (HEIGHT/2) + (HEIGHT/2) * secondXY[1]

        # draw the edge
        pointer.penup()
        pointer.goto(firstXpixel, firstYpixel)
        pointer.pendown()
        pointer.goto(secondXpixel, secondYpixel)
        pointer.penup()


#
# Tracks the constellation to find the min and max x and y, draws an orange box with 15-pixel padding around
# the constellation, and writes the name of the constellation above it. It then
# writes the min and max x and y, along with the constellation name, to another file.
# Parameters: pointer: (the turtle drawing object)
#             constellationName: the name of the constellation
#             constStarList: the list of star pair tuples for the constellation
#             namesDictAll: the dictionary of names as keys and (x,y,mag) tuples as values
#
# Usage -> drawBoundingBox(-0.3, 0.2, 0.4, 0.7)
# Returns: nothing
#
   

def drawBoundingBox(pointer, constellationName, constStarList, namesDictAll):

    # set the pencolor to orange and initialize local variables to be used
    boxColour = "orange"
    pointer.color(boxColour)
    textPadding = 20
    fontSize = 10
    boxPadding = 15

    # initialize variables use for drawing the bounding box
    smallestX = WIDTH
    smallestY = HEIGHT
    biggestX = 0
    biggestY = 0

    # loop back over the constellation to track min and max x and y
    for edge in constStarList:

        firstXYmag = namesDictAll[edge[0]]
        secondXYmag = namesDictAll[edge[1]]

        firstXY = firstXYmag[0:2]
        secondXY = secondXYmag[0:2]

        # calculate the pixel locations of the coordinate points given
        firstXpixel = (WIDTH/2) + (WIDTH/2) * firstXY[0]
        firstYpixel = (HEIGHT/2) + (HEIGHT/2) * firstXY[1]
        secondXpixel = (WIDTH/2) + (WIDTH/2) * secondXY[0]
        secondYpixel = (HEIGHT/2) + (HEIGHT/2) * secondXY[1]

        # track the min and max x and y, updating when applicable
        if firstXpixel < smallestX:
            smallestX = firstXpixel
        if firstXpixel > biggestX:
            biggestX = firstXpixel
        if secondXpixel < smallestX:
            smallestX = secondXpixel
        if secondXpixel > biggestX:
            biggestX = secondXpixel
       
        if firstYpixel < smallestY:
            smallestY = firstYpixel
        if firstYpixel > biggestY:
            biggestY = firstYpixel
        if secondYpixel < smallestY:
            smallestY = secondYpixel
        if secondYpixel > biggestY:
            biggestY = secondYpixel


    # Draw the bounding box
    pointer.penup()
    pointer.goto(smallestX-boxPadding, smallestY-boxPadding)
    pointer.pendown()
    pointer.goto(biggestX+boxPadding, smallestY-boxPadding)
    pointer.goto(biggestX+boxPadding, biggestY+boxPadding)
    pointer.goto(smallestX-boxPadding, biggestY+boxPadding)
    pointer.goto(smallestX-boxPadding, smallestY-boxPadding)

    # write the constellation name above the box
    pointer.penup()
    pointer.goto(smallestX + ((biggestX-smallestX)/2), biggestY + textPadding)
    pointer.write(constellationName, font=("Arial", fontSize), align="center")

    # try-except block to catch errors while writing to the file
    try:
        fileWriter = open(f"{constellationName}_box.dat", "w")
        fileWriter.write(f"{constellationName}\n{smallestX}, {biggestX}, {smallestY}, {biggestY}")
        fileWriter.close()

    except:
        print("Error: something went wrong with the constellation box file")
        sys.exit(1)


#
# Main function that handles command line arguments and calls on all the other functions to set up the window, draw the axes, read
# the files, and draw the stars and constellations.
#
# Returns: nothing
#

def main():
   
    # Handle command line arguments

    # set "names" to False - will be True if "-names" is one of the command line arguments
    names = False
   
    # if statement: if calling the script file is the only argument
    if len(sys.argv) == 1:
        starsFile = input("Enter a stars location file: ")
        if os.path.isfile(starsFile) == False:
            print(f"Error: the file '{starsFile}' does not exist. Please try again.")
            sys.exit(1)

    # elif statement: if the script file is one of two arguments
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-names":
            names = True
            starsFile = input("Enter a stars location file: ")
            if os.path.isfile(starsFile) == False:
                print(f"Error: the file '{starsFile}' does not exist. Please try again.")
                sys.exit(1)

        else:
            if os.path.isfile(sys.argv[1]) == False:
                print(f"Error: the file '{sys.argv[1]}' does not exist. Please try again.")
                sys.exit(1)
            else:
                starsFile = sys.argv[1]

    # elif statement: if there are two arguments beside the script file
    elif len(sys.argv) == 3:

        if sys.argv[1] != "-names" and sys.argv[2] != "-names":
            print('Error: too many arguments, none are "-names". Please try again.')
            sys.exit(1)

        elif sys.argv[2] == "-names":
            if os.path.isfile(sys.argv[1]):                  
                starsFile = sys.argv[1]
                names = True
            else:
                print(f"Error: the file '{sys.argv[1]}' does not exist. Please try again.")
                sys.exit(1)

        elif sys.argv[1] == "-names":
            if os.path.isfile(sys.argv[2]):
                starsFile = sys.argv[2]
                names = True
            else:
                print(f"Error: the file '{sys.argv[2]}' does not exist. Please try again.")
                sys.exit(1)

    # elif statement: if there are more than two arguments beside the script file, there are too many arguments
    elif len(sys.argv) > 3:
        print("Error: too many command line arguments. Please try again.")
        sys.exit(1)

   
    #Read star information from file (function)
    allStarsList, starNamesDict = readStarFile(starsFile)

    #Set up the window
    pointer = setup()
   
    #Draw Axes (function)
    drawAxes(pointer)
   
    #Draw Stars (function)
    drawStars(allStarsList, starNamesDict, pointer, names)
   
    #Loop getting filenames
   
    constellationFile = input("Enter a constellation filename: ")
    constellationList = []

    # while loop to prompt for valid constellation files until a blank input is entered
    while constellationFile != "":

        if os.path.isfile(constellationFile):
            if constellationFile not in constellationList:
                constellationList.append(constellationFile)
            constellationFile = input("Enter another constellation filename: ")

        else:
            constellationFile = input("The file you entered does not exist. Please try again: ")


    # set counter to 0 for calculating the constellation colour
    counter = 0

    # for loop: for each constellation file inputted, read the file, draw the constellation, and draw the bounding box and name
    for constellationFile in constellationList:

        # use the counter to calculate the constellation colour
        constellationColour = getColour(counter)
       
        #Read constellation file (function)
        constellationName, constStarList = readConstellationFile(constellationFile)

        #Draw Constellation (function)
        drawConstellation(pointer, starNamesDict, constStarList, constellationName, constellationColour)
   
        #Draw bounding box (Bonus) (function)
        drawBoundingBox(pointer, constellationName, constStarList, starNamesDict)

        # update the counter
        counter += 1

# Call the main function
main()


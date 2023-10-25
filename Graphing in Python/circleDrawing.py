
import turtle          
from math import *

# CONSTANTS
WIDTH = 800
HEIGHT = 600
AXISCOLOR = "black"

#
#  Returns the screen (pixel based) coordinates of some (x, y) graph location based on configuration
#
#  Parameters:
#   xo, yo : the pixel location of the origin of the  graph
#   ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#   x, y: the graph location to change into a screen (pixel-based) location
#
#  Usage -> screenCoor(xo, yo, ratio, 1, 0)
#
#  Returns: (screenX, screenY) which is the graph location (x,y) as a pixel location in the window
#

def screenCoor(xo, yo, ratio, x, y):
    screenX = xo + ratio*x
    screenY = yo + ratio*y
    return (screenX, screenY)

#
#  Returns a string of the colour to use for the current expression being drawn
#  This colour is chosen based on which how many expressions have previously been drawn
#  The counter starts at 0, the first or 0th expression, should be red, the second green, the third blue
#  then loops back to red, then green, then blue, again
#
#  Usage -> getColor(counter)
#
#  Parameters:
#  counter: an integer where the value is a count (starting at 0) of the expressions drawn
#
#  Returns: 0 -> "red", 1 -> "green", 2 -> "blue", 3 -> "red", 4 -> "green", etc.
#

def getColor(counter):
    if counter % 3 == 0:
        return "red"

    elif counter % 3 == 1:
        return "green"

    else:
        return "blue"

#
#  Draw in the window an xaxis label (text) for a point at (screenX, screenY)
#  the actual drawing points will be offset from this location as necessary
#  Ex. for (x,y) = (1,0) or x-axis tick/label spot 1, draw a tick mark and the label 1
#
#  Usage -> drawXAxisLabelTick(pointer, 1, 0, "1")
#
#  Parameters:
#  pointer: the turtle drawing object
#  (screenX, screenY): the pixel screen location to drawn the label and tick mark for
#  text: the text of the label to draw
#
#  Returns: Nothing
#

def drawXAxisLabelTick(pointer, screenX, screenY, text):

    # Defining local variables to use when drawing the ticks:
    halfTickLength = 5
    textSpotX = 25

    # Drawing the tick:
    pointer.goto(screenX, screenY + halfTickLength)
    pointer.goto(screenX, screenY - halfTickLength)

    # Writing the tick number and going back to start location:
    pointer.penup()
    pointer.goto(screenX, screenY - textSpotX)
    pointer.write(text, align = "center", font = 20)
    pointer.goto(screenX, screenY)

#
#  Draw in the window an yaxis label (text) for a point at (screenX, screenY)
#  the actual drawing points will be offset from this location as necessary
#  Ex. for (x,y) = (0,1) or y-axis tick/label spot 1, draw a tick mark and the label 1
#
#  Usage -> drawXAxisLabelTick(pointer, 0, 1, "1")
#
#  Parameters:
#  pointer: the turtle drawing object
#  screenX, screenY): the pixel screen location to drawn the label and tick mark for
#  text: the text of the label to draw
#
#  Returns: Nothing
#

def drawYAxisLabelTick(pointer, screenX, screenY, text):

    # Defining local variables to use when drawing the ticks:
    halfTickLength = 5
    textSpotY = 15
   
    # Drawing the tick:
    pointer.goto(screenX + halfTickLength, screenY)
    pointer.goto(screenX - halfTickLength, screenY)

    # Writing the tick number and going back to start location:
    pointer.penup()
    pointer.goto(screenX - textSpotY, screenY)
    pointer.write(text, align = "center", font = 20)
    pointer.goto(screenX, screenY)
   

#
#  Draw in the window an xaxis (secondary function is to return the minimum and maximum graph locations drawn at)
#
#  Usage -> drawXAxis(pointer, xo, yo, ratio)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#
#  Returns: (xmin, xmax) where xmin is minimum x location drawn at and xmax is maximum x location drawn at
#

def drawXAxis(pointer, xo, yo, ratio):
    xmin = 0
    xmax = 0

    # Defining and setting the pointer direction for the + x-axis:
    headingX1 = 0
    pointer.setheading(headingX1)

    # Setting the number of ticks to start at zero:
    tickNumberX1 = 0
    tickNumberX2 = 0

    # Setting two local variables to xo:
    xStart1 = xo
    xStart2 = xo
   
    pointer.penup()

    # While loop that draws the + x-axis:
    while xStart1 <= WIDTH:
        pointer.goto(xStart1, yo)
        pointer.pendown()
        pointer.forward(ratio)
        tickNumberX1 += 1
        xStart1 += ratio
        drawXAxisLabelTick(pointer, xStart1, yo, str(tickNumberX1))
        pointer.penup()

    # Set xmax to the number of ticks drawn in the positive direction:
    xmax = tickNumberX1

    # Defining and setting the pointer direction for the - x-axis:
    headingX2 = 180
    pointer.setheading(headingX2)
   
    # While loop that draws the - x-axis:
    while xStart2 >= 0:
        pointer.goto(xStart2, yo)
        pointer.pendown()
        pointer.forward(ratio)
        xStart2 -= ratio
        tickNumberX2 -= 1
        drawXAxisLabelTick(pointer, xStart2, yo, str(tickNumberX2))
        pointer.penup()

    # Setting xmin to the number of ticks drawn in the negative direction:
    xmin = tickNumberX2
   
    return xmin, xmax

#
#  Draw in the window a yaxis
#
#  Usage -> drawYAxis(pointer, xo, yo, ratio)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#
#  Returns: Nothing
#

def drawYAxis(pointer, xo, yo, ratio):

    # Defining and setting the pointer for the + y-axis:
    headingY1 = 90
    pointer.setheading(headingY1)

    # Setting the number of ticks to start at zero:
    tickNumberY1 = 0
    tickNumberY2 = 0

    # Setting two local variables to yo:
    yStart1 = yo
    yStart2 = yo
   
    pointer.penup()

    # While loop that draws the + y-axis:
    while yStart1 <= HEIGHT:
        pointer.goto(xo, yStart1)
        pointer.pendown()
        pointer.forward(ratio)
        tickNumberY1 += 1
        yStart1 += ratio
        drawYAxisLabelTick(pointer, xo, yStart1, str(tickNumberY1))

    pointer.penup()

    # Defining and setting the pointer direction for the - y-axis:
    headingY2 = 270
    pointer.setheading(headingY2)

    # While loop that draws the - y-axis:
    while yStart2 >= 0:
        pointer.goto(xo, yStart2)
        pointer.pendown()
        pointer.forward(ratio)
        tickNumberY2 -= 1
        yStart2 -= ratio
        drawYAxisLabelTick(pointer, xo, yStart2, str(tickNumberY2))

       
#
#  Draw in the window the given expression (expr) between [xmin, xmax] graph locations
#
#  Usage -> drawExpr(pointer, xo, yo, ratio, xmin, xmax, expr)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#  expr: the expression to draw (assumed to be valid)
#  xmin, ymin : the range for which to draw the expression [xmin, xmax]
#
#  Returns: Nothing
#

def drawExpr(pointer, xo, yo, ratio, xmin, xmax, expr):
    #Draw expression

    # Setting the change in x each loop to equal 0.1:
    delta = 0.1

    # Setting x equal to xmin:
    x=xmin
   
    pointer.penup()
   
    # Try-Except block to evaluate for functions that don't start at xmin,
    # such as log(x) or sqrt(x):
    tryBlock = True
    while tryBlock == True:
        try:
            y = eval(expr)
       
        except:
            x += delta
           
        else:
            tryBlock = False

    # Calling screenCoor() to find the pixel locations of the start location
    # and going there:
    pixelX, pixelY = screenCoor(xo, yo, ratio, x, y)
    pointer.goto(pixelX, pixelY)
    pointer.pendown()

    # While loop that draws the function until x reaches xmax:


    while x <= xmax:
        x += delta
        y = eval(expr)            
        pixelX, pixelY = screenCoor(xo, yo, ratio, x, y)
        pointer.goto(pixelX, pixelY)
       

#
#  Setup of turtle screen before we draw
#  DO NOT CHANGE THIS FUNCTION
#
#  Returns: Nothing
#

def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer.hideturtle()
    screen.delay(delay=0)
    return pointer

#
#  Main function that attempts to graph a number of expressions entered by the user
#  The user is also able to designate the origin of the chart to be drawn, as well as the ratio of pixels to steps (shared by both x and y axes)
#  The window size is always 800 width by 600 height in pixels
#  DO NOT CHANGE THIS FUNCTION
#
#  Returns: Nothing
#

def main():
    #Setup window
    pointer = setup()

    #Get input from user
    xo, yo = eval(input("Enter pixel coordinates of origin: "))
    ratio = int(input("Enter ratio of pixels per step: "))

    #Set color and draw axes (store discovered visible xmin/xmax to use in drawing expressions)
    pointer.color(AXISCOLOR)
    xmin, xmax = drawXAxis(pointer, xo, yo, ratio)
    drawYAxis(pointer, xo, yo, ratio)

    #Loop and draw experssions until empty string "" is entered, change expression colour based on how many expressions have been drawn
    expr = input("Enter an arithmetic expression: ")
    counter = 0
    while expr != "":
        pointer.color(getColor(counter))
        drawExpr(pointer, xo, yo, ratio, xmin, xmax, expr)
        expr = input("Enter an arithmetic expression: ")
        counter += 1
 
#Run the program
main()

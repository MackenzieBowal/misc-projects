# I did not write any code in this file - it's the support and test for my code in Board.py

from SimpleGraphics import *
from random import shuffle
from math import factorial
from copy import deepcopy
import inspect
import sys
from pprint import pprint
import traceback
from Board import Board, X, O, EMPTY

# Contants for the board size
WIDTH = 600
HEIGHT = 600
# Constants to turn off tests for parts of assignment   
TESTPART1 = True
TESTPART2 = True
TESTPART3 = True
TESTPART4 = True
TESTPART5 = True
TESTPART6 = True
TESTPART7 = True
STOP1STFAIL = True

##############################################################################
#
# Code below is for testing student functions (IF YOU ARE READING THIS YOU BETTER NOT BE CHANGING CODE DOWN HERE)
#
##############################################################################

# Determine whether or not a function exists in the namespace at the time
# this function is called
# Parameters:
#   name: The name of the function to check the existence of
# Returns: True if the function exists, False otherwise
def functionExists(name):
  if name in dir(Board()):
      return True
  return False


# Run a series of tests on the createBoard function
# Parameters: (None)
# Returns: True if all tests passed.  False if any test fails.
def testCreateBoard():
    if not TESTPART1:
        return True
    print("Testing createBoard...")
    # Does the Board() function exist?
    succ = False
    try:
        Board()
        succ = True
    except TypeError as e:
        print("Exception on Board()")
        traceback.print_exc(file=sys.stdout)        
    try:
        Board(3,3)
        succ = True
    except TypeError as e:
        print("Exception on Board()")
        traceback.print_exc(file=sys.stdout)        
    if succ:
        print("  The __init__() constructor seems to be defined...")
    else:
        print("  The __init__() constructor don't seem to be defined properly...")
        return False
        
      
    try:
        Board(3,3)
        print("  The __init__(rows,cols) constructor seems to be defined properly...")
    except TypeError as e:
        print("  The __init__(rows,cols) constructor doesn't seem to exist...")
        return False
    try:
        Board()
        print("  The defaults for the __init__(rows=3,cols=3) constructor seem to be defined properly...")
    except TypeError as e:
        print("  The defaults for the __init__(rows=3,cols=3) constructor don't seem to exist...")
        return False

    for (rows, cols) in [(3, 3), (3, 4), (4, 3), (4, 4), (3, 5), (5, 3), (4, 5), (5, 4), (5,5)]:
        # Try and call the function
        try:
            print("  Attempting to use Board(%d, %d)... " % (rows, cols))
            b = Board(rows, cols)                
        except Exception as e:
            print("An exception occurred during the attempt.")
            traceback.print_exc(file=sys.stdout)
            return False

        # Does it have the set the board field to a correct type?
        if type(b.board) is not list:
            print("    The value of board was a", str(type(b.board)) + ", not a list.")
            return False

        # Does the list have the corret number of elements?
        if len(b.board) != rows:
            print("    The board had", len(b.board), "rows when", rows, "were expected.")
            return False

        # Is each row a list?  Does each row have the correct length?
        for i in range(len(b.board)):
            if type(b.board[i]) is not list:
                print("    The row at index", i, "is a", str(type(b.board[i])) + ", not a list.")
                return False
            if len(b.board[i]) != cols:
                print("    The row at index", i, "had", len(b.board[i]), "elements when", cols, "were expected.")
                return False

        # Is each row unique
        for i in range(len(b.board)):
            for j in range(len(b.board)):
                if i != j :
                    if b.board[i] is b.board[j]:
                        print("    The row at index", i, "is pointing to the same row as the row at index ", str(j) + ".")
                        return False
      
        # Is every space on the board populated with an integer value between 
        # 0 and syms (not including syms)?
        for r in range(0, len(b.board)):
            for c in range(0, len(b.board[r])):
                if type(b.board[r][c]) is not int:
                    print("    The value in row", r, "column", c, "is a", str(type(b.board[r][c])) + ", not an integer")
                    return False
                if b.board[r][c] != EMPTY:
                    print("    The integer in row", r, "column", c, "is a", b.board[r][c], "which is not EMPTY=0")
                    return False
    try:
        Board().rows()
        print("  The rows() method seems to exist...")
    except:
        print("  The rows() method doesn't seem to exist...")
        return False
    if type(Board(3,4).rows()) is not int or Board(3,4).rows() != 3:
      print("  The rows() method does not seem to be defined properly...")
      return False
    
    try:
        Board().cols()
        print("  The cols() method seems to exist...")
    except:
        print("  The cols() method doesn't seem to exist...")
        return False
    if type(Board(3,4).cols()) is not int or Board(3,4).cols() != 4:
      print("  The cols() method does not seem to be defined properly...")
    print("Success.")
    print()
    return True

# Run a series of tests on the canPlay and play functions
# Parameters: (None)
# Returns: True if all tests passed.  False if any test fails.
def testPlay():
    if not TESTPART2:
        return True
    print("Testing play, canPlay...")
    # Does the play, canPlay function exist?
    if functionExists("play"):
        print("  The method play seems to exist...")
    else:
        print("  The play method doesn't seem to exist...")
        return False
    if functionExists("canPlay"):
        print("  The method canPlay seems to exist...")
    else:
        print("  The canPlay method doesn't seem to exist...")
        return False

    for rows in [3,4]:
        for cols in [3,4]:
            b = Board(rows, cols)
            print("  The canPlay for all spots in empty board...")
            for row in range(rows):
                for col in range(cols):
                    r = b.canPlay(row, col)
                    # Check return type and value? Should be able to play everywhere.
                    if type(r) is not bool:
                        print("    The value returned was a", str(type(r)) + ", not a boolean.")
                        return False
                    if r is False:
                        message = "    The board "+str(b.board)+" is empty but canPlay(board, %d, %d) was False."
                        print(message % (row, col))
                        return False
                    b.board[row][col] = X
                    r = b.canPlay(row, col)
                    # Check return type and value? Should not be able to play here now.
                    if type(r) is not bool:
                        print("    The value returned was a", str(type(r)) + ", not a boolean.")
                        return False
                    if r is True:
                        message = "    The board "+str(b.board)+" has piece at this spot but canPlay(board, %d, %d) was True."
                        print(message % (row, col))
                        return False
                    b.board[row][col] = EMPTY
            copy = deepcopy(b)
            # Change a copy of the board and check if result of play, canPlay matches changes expected
            print("  Test play/canPlay before and after playing at every location in",rows,"x",cols," empty board")
            for row in range(rows):
                for col in range(cols):
                    r0 = b.canPlay(row, col)
                    if r0 is False:
                        message = "   The board "+str(b.board)+" is empty but canPlay(board, %d, %d) was False."
                        print(message % (row, col))
                        return False
                    # Play an X. Should not be able to play in this spot now.
                    r1 = b.play(row, col, X)
                    if type(r1) is not type(None):
                        message = "    The value returned by play(board, %d, %d, %d) was a "+ str(type(r1)) + ", not None."
                        print(message % (row,col,X))
                        return False
                    copy.board[row][col] = X
                    if copy.board != b.board:
                        message = "    The board "+str(b.board)+" returned by play(board, %d, %d, %d) was not "+str(copy.board)
                        print(message % (row,col,X))
                        return False                
                    r2 = b.canPlay(row, col)
                    if r2 is True:
                        message = "   The board "+str(b.board)+" is occupied but canPlay(board, %d, %d) was True."
                        print(message % (row, col))
                        return True
                    # Play an EMPTY. Should be able to play in this spot now.
                    r3 = b.play(row, col, EMPTY)
                    if type(r3) is not type(None):
                        message = "    The value returned by play(board, %d, %d, %d) was a "+ str(type(r3)) + ", not None."
                        print(message % (row,col,EMPTY))
                        return False
                    copy.board[row][col] = EMPTY
                    if copy.board != b.board:
                        message = "    The board "+str(b.board)+" returned by play(board, %d, %d, %d) was not "+str(copy.board)
                        print(message % (row,col,EMPTY))
                        return False           
                    r4 = b.canPlay(row, col)
                    if r4 is False:
                        message = "   The board "+str(b.board)+" is empty but canPlay(board, %d, %d) was False."
                        print(message % (row, col))
                        return False       
                    # Play an O. Should not be able to play in this spot now.
                    r5 = b.play(row, col, O)
                    if type(r5) is not type(None):
                        message = "    The value returned by play(board, %d, %d, %d) was a "+ str(type(r5)) + ", not None."
                        print(message % (row,col,O))
                        return False
                    copy.board[row][col] = O
                    if copy.board != b.board:
                        message = "    The board "+str(b.board)+" returned by play(board, %d, %d, %d) was not "+str(copy.board)
                        print(message % (row,col,O))
                        return False           
                    r6 = b.canPlay(row, col)
                    if r6 is True:
                        message = "   The board "+str(b.board)+" is occupied but canPlay(board, %d, %d) was True."
                        print(message % (row, col))
                        return True          
                    # Play an EMPTY. Should be able to play in this spot now.
                    r7 = b.play(row, col, EMPTY)
                    if type(r7) is not type(None):
                        message = "    The value returned by play(board, %d, %d, %d) was a "+ str(type(r7)) + ", not None."
                        print(message % (row,col,EMPTY))
                        return False
                    copy.board[row][col] = EMPTY
                    if copy.board != b.board:
                        message = "    The board "+str(b.board)+" returned by play(board, %d, %d, %d) was not "+str(copy.board)
                        print(message % (row,col,EMPTY))
                        return False           
                    r8 = b.canPlay(row, col)
                    if r8 is False:
                        message = "   The board "+str(b.board)+" is empty but canPlay(board, %d, %d) was False."
                        print(message % (row, col))
                        return False            
    print("Success.")
    print()
    return True

# Run a series of tests on the full functions
# Parameters: (None)
# Returns: True if all tests passed.  False if any test fails.   
def testFull():
    if not TESTPART3:
        return True
    print("Testing full...")
    # Does the full function exist?
    if functionExists("full"):
        print("  The method full seems to exist...")
    else:
        print("  The full method doesn't seem to exist...")
        return False

    for rows in [3,4]:
        for cols in [3,4]:
            print("Testing full for a board of size",rows,"x",cols)
            b = Board(rows, cols)
            # Does full return right for empty board?
            print("  Testing call to full for empty board.")
            r = b.full()
            if type(r) is not bool:
                print("    The value returned by full(board) was a", str(type(r)) + ", not a boolean.")
                return False
            if r == True:
                print("    The board ",b.board," is empty but full returned True.")
                return False
            for row in range(rows):
                for col in range(cols):
                    b.board[row][col] = X
            r = b.full()        
            # Does full return right for full board?
            print("  Testing call to full for board full of Xs.")
            if type(r) is not bool:
                print("    The value returned by full(board) was a", str(type(r)) + ", not a boolean.")
                return False
            if r == False:
                print("    The board ",b.board," is full but full returned False.")
                return False
            # Does full return right if we selectively remove single piece from anywhere on board?
            print("  Testing full for almost full board of Xs with one EMPTY spot")
            for row in range(rows):
                for col in range(cols):
                    b.board[row][col] = EMPTY
                    r = b.full()
                    if type(r) is not bool:
                        print("    The value returned by full(board) was a", str(type(r)) + ", not a boolean.")
                        return False
                    if r == True:
                        print("    The board ",b.board," is not full returned True.")
                        return False
                    b.board[row][col] = X
            for row in range(rows):
                for col in range(cols):
                    b.board[row][col] = O
            r = b.full()        
            # Does full return right for full board?
            print("  Testing call to full for board full of Os.")
            if type(r) is not bool:
                print("    The value returned by full(board) was a", str(type(r)) + ", not a boolean.")
                return False
            if r == False:
                print("    The board ",b.board," is full but full returned False.")
                return False
            # Does full return right if we selectively remove single piece from anywhere on board?
            print("  Testing full for almost full board of Os with one EMPTY spot")
            for row in range(rows):
                for col in range(cols):
                    b.board[row][col] = EMPTY
                    r = b.full()
                    if type(r) is not bool:
                        print("    The value returned by full(board) was a", str(type(r)) + ", not a boolean.")
                        return False
                    if r == True:
                        print("    The board ",b.board," is not full returned True.")
                        return False
                    if r == True:
                        print()
                        return False
                    b.board[row][col] = O            
    print("Success.")
    print()
    return True

#
# Run a series of tests on the winInRow function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testWinInRow():
    if not TESTPART4:
        return True
    print("Testing winInRow...")

    # Does the winInRow function exist?
    if functionExists("winInRow"):
        print("  The function winInRow seems to exist...")
    else:
        print("  The winInRow function doesn't seem to exist...\n")
        return

    passed = 0
    failed = 0
    attempt = 0
    for (b, r, p, s) in [ \
        #Board sizes with wins
      ([[1, 1, 1], \
        [0, 0, 0], \
        [0, 0, 0]], 0, 1, True), \
      ([[1, 1, 1], \
        [0, 0, 0], \
        [0, 0, 0], \
        [0, 0, 0]], 0, 1, True), \
      ([[1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[0, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[1, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[0, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[1, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      #Win in other rows
      ([[0, 0, 0, 0], \
        [1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 1, True), \
      ([[0, 0, 0, 0], \
        [1, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 1, 0], \
        [0, 0, 0, 0]], 2, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 1, 1, 1], \
        [0, 0, 0, 0]], 2, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 1, 1], \
        [0, 0, 0, 0]], 2, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 1, 0]], 3, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 1, 1, 1]], 3, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 1, 1]], 3, 1, True), \
      #Win with other piece type
      ([[0, 0, 0, 0], \
        [2, 2, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 2, True), \
      ([[0, 0, 0, 0], \
        [0, 2, 2, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 2, True), \
      ([[0, 0, 0, 0], \
        [2, 2, 2, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 2, True), \
      #Win has other type around      
      ([[1, 1, 1, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[2, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      #Win isn't with asked about piece type
      ([[1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 2, False), \
      ([[0, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 2, False), \
      ([[1, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 2, False), \
      ([[2, 2, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[0, 2, 2, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[2, 2, 2, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
        #Win broken by non empty  
      ([[1, 1, 2, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[1, 2, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[1, 1, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[1, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[1, 0, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 0, 1]], 0, 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 1]], 0, 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 1, 1]], 0, 1, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False)]:

        # Attempt the function call
        try:
            temp = Board()
            temp.board = b
            b = temp
            for i in range(len(b.board)):
                attempt+=1
                result = b.winInRow(i, p)
                # Does it have the correct return type?
                if type(result) is not bool:
                    print("\nFAILED: The value returned was a", str(type(result)) + ", not a Boolean.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    Failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue

                # Did it return the correct value
                if s and not result and r==i:
                    print("  Attempting to use winInRow Test",attempt,end="")
                    print("\nFAILED: The value returned was", str(result), " for row = ",i," piece =",p,"when True was expected.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                # Did it return the correct value
                elif s and result and r!=i:
                    print("  Attempting to use winInRow Test",attempt,end="")
                    print("\nFAILED: The value returned was", str(result), " for row = ",i," piece =",p,"when False was expected.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                elif not s and result:
                    print("  Attempting to use winInRow Test",attempt,end="")
                    print("\nFAILED: The value returned was", str(result), " for row = ",i," piece =",p,"when False was expected.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                passed += 1
        except Exception as e:
            print("  Attempting to use winInRow Test",attempt,end="")
            print("\nFAILED: An exception occurred during the attempt.")
            print("The board was:")
            pprint(b.board)
            print()
            traceback.print_exc(file=sys.stdout)
            failed += 1
            if STOP1STFAIL:
                return
            else:
                continue
    if failed > 0 :
        print("Failed ", failed, "test cases", "of",attempt)
    else:
        print("Passed all tests. <",attempt,">")

    print()
    return


#
# Run a series of tests on the winInCol function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testWinInCol():
    if not TESTPART4:
        return True
    print("Testing winInCol...")

    # Does the winInCol function exist?
    if functionExists("winInCol"):
        print("  The function winInCol seems to exist...")
    else:
        print("  The winInCol function doesn't seem to exist...\n")
        return

    passed = 0
    failed = 0
    attempt = 0
    for (b, r, p, s) in [ \
  
      ([[1, 0, 0], \
        [1, 0, 0], \
        [1, 0, 0]], 0, 1, True), \
      ([[1, 0, 0], \
        [1, 0, 0], \
        [1, 0, 0], \
        [0, 0, 0]], 0, 1, True), \
      ([[0, 0, 0], \
        [1, 0, 0], \
        [1, 0, 0], \
        [1, 0, 0]], 0, 1, True), \
      ([[1, 0, 0], \
        [1, 0, 0], \
        [1, 0, 0], \
        [1, 0, 0]], 0, 1, True), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, True), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, True), \
      ([[0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, True), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, True), \
      #Win in other rows
      ([[0, 1, 0, 0], \
        [0, 1, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0]], 1, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 1, 0, 0], \
        [0, 1, 0, 0]], 1, 1, True), \
      ([[0, 1, 0, 0], \
        [0, 1, 0, 0], \
        [0, 1, 0, 0], \
        [0, 1, 0, 0]], 1, 1, True), \
      ([[0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 2, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0]], 2, 1, True), \
      ([[0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0]], 2, 1, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 0]], 3, 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1]], 3, 1, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1]], 3, 1, True), \
      #Win with other piece type
      ([[0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 1, 2, True), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0]], 1, 2, True), \
      ([[0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0]], 1, 2, True), \
      #Win has other type around      
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [2, 0, 0, 0]], 0, 1, True), \
      ([[2, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, True), \
      #Win isn't with asked about piece type
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 2, False), \
      ([[0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 2, False), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 2, False), \
      ([[2, 0, 0, 0], \
        [2, 0, 0, 0], \
        [2, 0, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[0, 0, 0, 0], \
        [2, 0, 0, 0], \
        [2, 0, 0, 0], \
        [2, 0, 0, 0]], 0, 1, False), \
      ([[2, 0, 0, 0], \
        [2, 0, 0, 0], \
        [2, 0, 0, 0], \
        [2, 0, 0, 0]], 0, 1, False), \
        #Win broken by non empty  
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [2, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, False), \
      ([[1, 0, 0, 0], \
        [2, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, False), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 0, 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 0, 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 0, 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1]], 0, 1, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 0, 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0]], 0, 1, False)]:

        # Attempt the function call
        try:
            temp = Board()
            temp.board = b
            b = temp
            for i in range(len(b.board[0])):
                attempt+=1
                result = b.winInCol(i, p)
                # Does it have the correct return type?
                if type(result) is not bool:
                    print("  Attempting to use winInCol Test",attempt,end="")
                    print("\nFAILED: The value returned was a", str(type(result)) + ", not a Boolean.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    Failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                # Did it return the correct value
                elif s and not result and r==i:
                    print("  Attempting to use winInCol Test",attempt,end="")
                    print("\nFAILED: The value returned was", str(result), " for row = ",i," piece =",p,"when True was expected.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                # Did it return the correct value
                elif s and result and r!=i:
                    print("  Attempting to use winInCol Test",attempt,end="")
                    print("\nFAILED: The value returned was", str(result), " for row = ",i," piece =",p,"when False was expected.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                elif not s and result:
                    print("  Attempting to use winInCol Test",attempt,end="")
                    print("\nFAILED: The value returned was", str(result), " for row = ",i," piece =",p,"when False was expected.")
                    print("The board was:")
                    pprint(b.board)
                    print()
                    failed += 1
                    if STOP1STFAIL:
                        return
                    else:
                        continue
                passed += 1
        except Exception as e:
            print("  Attempting to use winInCol Test",attempt,end="")
            print("\nFAILED: An exception occurred during the attempt.")
            print("The board was:")
            pprint(b.board)
            print()
            traceback.print_exc(file=sys.stdout)
            failed += 1
            if STOP1STFAIL:
                return
            else:
                continue
    if failed > 0 :
        print("Failed ", failed, "test cases", "of",attempt)
    else:
        print("Passed all tests. <",attempt,">")

    print()
    return

#
# Run a series of tests on the winInDiag function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testWinInDiag():
    if not TESTPART5:
        return True
    print("Testing winInDiag...")

    # Does the winInDiag function exist?
    if functionExists("winInDiag"):
        print("  The function winInDiag seems to exist...")
    else:
        print("  The winInDiag function doesn't seem to exist...\n")
        return

    passed = 0
    failed = 0
    attempt = 0
    for (b,  p, s) in [ \
      #win in different board sizes
      ([[1, 0, 0], \
        [0, 1, 0], \
        [0, 0, 1]], 1, True), \
      ([[1, 0, 0], \
        [0, 1, 0], \
        [0, 0, 1], \
        [0, 0, 0]], 1, True), \
      ([[0, 0, 0], \
        [1, 0, 0], \
        [0, 1, 0], \
        [0, 0, 1]], 1, True), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0]], 1, True), \
      ([[0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 1, True), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 1, True), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 1, True), \
      ([[0, 0, 1], \
        [0, 1, 0], \
        [1, 0, 0]], 1, True), \
      ([[0, 0, 1], \
        [0, 1, 0], \
        [1, 0, 0], \
        [0, 0, 0]], 1, True), \
      ([[0, 0, 0], \
        [0, 0, 1], \
        [0, 1, 0], \
        [1, 0, 0]], 1, True), \
      ([[0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0]], 1, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, True), \
      #Win with other piece type
      ([[0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0]], 2, True), \
      #Win has other type around  
      ([[0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [1, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0]], 2, True), \
      #Win isn't with asked about piece type
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 2, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 2, False), \
      ([[0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0]], 1, False), \
        #Win broken by non empty
      ([[1, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 2, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 2, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 2, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[1, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 1, False)]:

        # Attempt the function call
        try:
            temp = Board()
            temp.board = b
            b = temp
            attempt+=1
            result = b.winInDiag(p)
            # Does it have the correct return type?
            if type(result) is not bool:
                print("  Attempting to use winInDiag Test",attempt,end="")
                print("\nFAILED: The value returned was a", str(type(result)) + ", not a Boolean.")
                print("The board was:")
                pprint(b.board)
                print()
                Failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue

            # Did it return the correct value
            if s and not result:
                print("  Attempting to use winInDiag Test",attempt,end="")
                print("\nFAILED: The value returned was", str(result), " piece =",p,"when True was expected.")
                print("The board was:")
                pprint(b.board)
                print()
                failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue
            # Did it return the correct value
            elif not s and result:
                print("  Attempting to use winInDiag Test",attempt,end="")
                print("\nFAILED: The value returned was", str(result), " for piece =",p,"when False was expected.")
                print("The board was:")
                pprint(b.board)
                print()
                failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue
            passed += 1
        except Exception as e:
            print("  Attempting to use winInDiag Test",attempt,end="")
            print("\nFAILED: An exception occurred during the attempt.")
            print("The board was:")
            pprint(b.board)
            print()
            traceback.print_exc(file=sys.stdout)
            failed += 1
            if STOP1STFAIL:
                return
            else:
                continue
    if failed > 0 :
        print("Failed ", failed, "test cases", "of",attempt)
    else:
        print("Passed all tests. <",attempt,">")

    print()
    return


#
# Run a series of tests on the won function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testWon():
    if not TESTPART6:
        return True
    print("Testing won...")

    # Does the won function exist?
    if functionExists("won"):
        print("  The function won seems to exist...")
    else:
        print("  The won won doesn't seem to exist...\n")
        return

    passed = 0
    failed = 0
    attempt = 0    
    for (b, p, s) in [ \
      ([[1, 1, 1], \
        [0, 0, 0], \
        [0, 0, 0]], 1, True), \
      ([[1, 1, 1], \
        [0, 0, 0], \
        [0, 0, 0], \
        [0, 0, 0]], 1, True), \
      ([[1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [2, 2, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 0], \
        [0, 2, 2, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 1, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 1, 1, 1], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [2, 2, 2, 0]], 2, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 2, 2]], 2, True), \
      ([[1, 1, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 1, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 0, 0, 0], \
        [2, 2, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 2, 2, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 1, 0], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 1, 1, 1], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [2, 2, 2, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 2, 2]], 1, False), \
      ([[1, 1, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[1, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[1, 0, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 0, 1]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 1]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 1, 1]], 1, False), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 1, True), \
      ([[0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0]], 2, True), \
      ([[0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0]], 1, True), \
      ([[0, 0, 0, 2], \
        [0, 0, 0, 2], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0]], 2, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 2], \
        [0, 0, 0, 2]], 2, True), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 2, False), \
      ([[0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0], \
        [0, 2, 0, 0]], 1, False), \
      ([[0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]], 2, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0]], 2, False), \
      ([[0, 0, 0, 2], \
        [0, 0, 0, 2], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 2], \
        [0, 0, 0, 2]], 1, False), \
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1]], 1, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]],  1, True), \
      ([[0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]],  1, True), \
      ([[0, 0, 0, 0], \
        [2, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 2, 0]],  2, True), \
      ([[0, 2, 0, 0], \
        [0, 0, 2, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0]],  2, True), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0]],  1, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]],  1, True), \
      ([[0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0], \
        [0, 0, 0, 0]],  2, True), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0]],  2, True), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0]],  2, False), \
      ([[0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]],  2, False), \
      ([[0, 0, 0, 0], \
        [2, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 2, 0]],  1, False), \
      ([[0, 2, 0, 0], \
        [0, 0, 2, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0]],  1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0]],  2, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]],  2, False), \
      ([[0, 0, 2, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0], \
        [0, 0, 0, 0]],  1, False), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0]],  1, False), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]],  1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]],  1, False), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]],  1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]],  1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]],  1, False), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]],  1, False)]:

        # Attempt the function call
        try:
            temp = Board()
            temp.board = b
            b = temp
            attempt+=1
            result = b.won(p)
            # Does it have the correct return type?
            if type(result) is not bool:
                print("  Attempting to use won Test",attempt,end="")
                print("\nFAILED: The value returned was a", str(type(result)) + ", not a Boolean.")
                print("The board was:")
                pprint(b.board)
                print()
                Failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue

            # Did it return the correct value
            if s and not result:
                print("  Attempting to use won Test",attempt,end="")
                print("\nFAILED: The value returned was", str(result), " piece =",p,"when True was expected.")
                print("The board was:")
                pprint(b.board)
                print()
                failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue
            # Did it return the correct value
            elif not s and result:
                print("  Attempting to use won Test",attempt,end="")
                print("\nFAILED: The value returned was", str(result), " for piece =",p,"when False was expected.")
                print("The board was:")
                pprint(b.board)
                print()
                failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue
            passed += 1
        except Exception as e:
            print("  Attempting to use won Test",attempt,end="")
            print("\nFAILED: An exception occurred during the attempt.")
            print("The board was:")
            pprint(b.board)
            print()
            traceback.print_exc(file=sys.stdout)
            failed += 1
            if STOP1STFAIL:
                return
            else:
                continue
    if failed > 0 :
        print("Failed ", failed, "test cases", "of",attempt)
    else:
        print("Passed all tests. <",attempt,">")

    print()
    return


#
# Run a series of tests on the hint function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testHint():
    if not TESTPART7:
        return True
    print("Testing hint...")

    # Does the hint function exist?
    if functionExists("hint"):
        print("  The function hint seems to exist...")
    else:
        print("  The winInDiag hint doesn't seem to exist...\n")
        return

    passed = 0
    failed = 0
    attempt = 0    
    for (b, p, r, c) in [ \
      ([[1, 1, 0], \
        [0, 0, 0], \
        [0, 0, 0]], 1, 0, 2), \
      ([[1, 1, 0], \
        [0, 0, 0], \
        [0, 0, 0], \
        [0, 0, 0]], 1, 0, 2), \
      ([[1, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 0, 2), \
      ([[1, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 0, 2), \
      ([[0, 0, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 0, 1), \
      ([[0, 0, 0, 0], \
        [2, 0, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, 1, 1), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, 1, 2), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 0, 0], \
        [0, 0, 0, 0]], 1, 2, 2), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 1, 1], \
        [0, 0, 0, 0]], 1, 2, 1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [2, 0, 2, 0]], 2, 3, 1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 0, 2]], 2, 3, 2), \
      
      ([[1, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, -1, -1), \
      ([[0, 0, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, -1, -1), \
      ([[0, 0, 0, 0], \
        [2, 0, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 0, 0], \
        [0, 0, 0, 0]], 2, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 1, 1], \
        [0, 0, 0, 0]], 2, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [2, 0, 2, 0]], 1, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 0, 2]], 1, -1, -1), \
      
      ([[1, 1, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 0, 2), \
      ([[1, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, -1, -1), \
      ([[1, 0, 1, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 0, 1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 1, 0, 1]], 1, 3, 2), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 1]], 1, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 1, 1]], 1, 3, 1), \

      
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 2, 0), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 1, 1, 0), \
      ([[0, 2, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 2, 1, 1), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 0, 0]], 2, 2, 1), \
      ([[0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 2, 2), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0]], 1, 1, 2), \
      ([[0, 0, 0, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0]], 2, 1, 3), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 2]], 2, 2, 3), \

      
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 2, -1, -1), \
      ([[0, 2, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 1, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0], \
        [0, 2, 0, 0]], 1, -1, -1), \
      ([[0, 0, 1, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 1, 0]], 2, -1, -1), \
      ([[0, 0, 0, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0]], 1, -1, -1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 2], \
        [0, 0, 0, 0], \
        [0, 0, 0, 2]], 1, -1, -1), \
      
      ([[1, 0, 0, 0], \
        [1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 1, 2, 0), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0]], 1, -1, -1), \
      ([[1, 0, 0, 0], \
        [0, 0, 0, 0], \
        [1, 0, 0, 0], \
        [1, 0, 0, 0]], 1, 1, 0), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, 2, 3), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, -1, -1), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1], \
        [0, 0, 0, 1]], 1, 1, 3), \


      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, 2, 2), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, 1, 2), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 1, 2, 2), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 1, 1, 2), \
      ([[0, 2, 0, 0], \
        [0, 0, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, 2, 3), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0], \
        [0, 0, 0, 0]], 2, 0, 2), \
      ([[0, 0, 0, 0], \
        [2, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 2, 3, 2), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0]], 2, 1, 3), \
      
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 2, -1,-1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 2, -1,-1), \
      ([[1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 1]], 2, -1,-1), \
      ([[0, 0, 0, 1], \
        [0, 0, 0, 0], \
        [0, 1, 0, 0], \
        [1, 0, 0, 0]], 2, -1,-1), \
      ([[0, 2, 0, 0], \
        [0, 0, 2, 0], \
        [0, 0, 0, 0], \
        [0, 0, 0, 0]], 1, -1,-1), \
      ([[0, 0, 0, 0], \
        [0, 2, 0, 0], \
        [2, 0, 0, 0], \
        [0, 0, 0, 0]], 1, -1,-1), \
      ([[0, 0, 0, 0], \
        [2, 0, 0, 0], \
        [0, 2, 0, 0], \
        [0, 0, 0, 0]], 1, -1,-1), \
      ([[0, 0, 0, 0], \
        [0, 0, 0, 0], \
        [0, 0, 2, 0], \
        [0, 2, 0, 0]], 1, -1,-1)

      ]:

        # Attempt the function call
        try:
            temp = Board()
            temp.board = b
            b = temp
            attempt+=1
            row,col = b.hint( p)
            # Does it have the correct return type?
            if type(row) is not int:
                print("  Attempting to use hint Test",attempt,end="")
                print("\nFAILED: The value returned was a", str(type(row)) + ", not a Integer.")
                print("The board was:")
                pprint(b)
                print()
                Failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue
            if type(col) is not int:
                print("  Attempting to use hint Test",attempt,end="")
                print("\nFAILED: The value returned was a", str(type(col)) + ", not a Integer.")
                print("The board was:")
                pprint(b.board)
                print()
                Failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue

            # Did it return the correct value
            if r != row or c != col:
                print("  Attempting to use hint Test",attempt,end="")
                print("\nFAILED: The value returned was", str(row),",", str(col), "for piece =",p,"when", str(r),",", str(c)," was expected.")
                print("The board was:")
                pprint(b.board)
                print()
                failed += 1
                if STOP1STFAIL:
                    return
                else:
                    continue
            passed += 1
        except Exception as e:
            print("  Attempting to use hint Test",attempt,end="")
            print("\nFAILED: An exception occurred during the attempt.")
            print("The board was:")
            pprint(b.board)
            print()
            traceback.print_exc(file=sys.stdout)
            failed += 1
            if STOP1STFAIL:
                return
            else:
                continue
    if failed > 0 :
        print("Failed ", failed, "test cases", "of",attempt)
    else:
        print("Passed all tests. <",attempt,">")
    print()
    return

def testArgs():
    fail = []
    fail.append(["tictactoe.py"])
    fail.append(["tictactoe.py","3"])
    fail.append(["tictactoe.py","3","3"])
    fail.append(["tictactoe.py","3","3","0"])
    fail.append(["tictactoe.py","4","4","0","X","anything"])
    fail.append(["tictactoe.py","3","3","0","X","-a","anything"])
    fail.append(["tictactoe.py","3","3","0","X","-h","anything"])
    fail.append(["tictactoe.py","2","3","0","X"])
    fail.append(["tictactoe.py","6","3","0","X"])
    fail.append(["tictactoe.py","3","2","0","X"])
    fail.append(["tictactoe.py","3","6","0","X"])
    fail.append(["tictactoe.py","3","3","5","X"])
    fail.append(["tictactoe.py","4","4","4","X"])
    fail.append(["tictactoe.py","3","3","4","Z"])
    fail.append(["tictactoe.py","a","3","0","X"])
    fail.append(["tictactoe.py","3","a","0","X"])    
    fail.append(["tictactoe.py","3","3","a","X"])
    print("Check those that should fail")
    for f in fail:
        if checkArgs(f) != False:
            print(f)
            sys.exit(0)
    print("Check those that should fail DONE")
    succ = []
    succ.append(["tictactoe.py","3","3","0","X"])
    succ.append(["tictactoe.py","4","3","0","X"])
    succ.append(["tictactoe.py","3","4","0","X"])
    succ.append(["tictactoe.py","4","4","0","X"])
    succ.append(["tictactoe.py","3","5","0","X"])    
    succ.append(["tictactoe.py","5","3","0","X"])
    succ.append(["tictactoe.py","5","5","0","X"])
    succ.append(["tictactoe.py","4","5","0","X"])
    succ.append(["tictactoe.py","5","4","0","X"])
    succ.append(["tictactoe.py","3","3","1","X"])
    succ.append(["tictactoe.py","3","3","2","X"])
    succ.append(["tictactoe.py","3","3","3","X"])
    succ.append(["tictactoe.py","3","3","4","X"])
    succ.append(["tictactoe.py","3","4","1","X"])
    succ.append(["tictactoe.py","3","4","2","X"])
    succ.append(["tictactoe.py","3","4","3","X"])
    succ.append(["tictactoe.py","4","3","1","X"])
    succ.append(["tictactoe.py","4","3","2","X"])
    succ.append(["tictactoe.py","4","3","3","X"])
    succ.append(["tictactoe.py","4","4","1","X"])
    succ.append(["tictactoe.py","4","4","2","X"])
    succ.append(["tictactoe.py","4","4","3","X"])
    succ.append(["tictactoe.py","3","3","0","O"])
    succ.append(["tictactoe.py","3","3","0","X","-h"])
    succ.append(["tictactoe.py","3","3","0","X","-a"])
    print("Check those that should succeed")
    for s in succ:
        if checkArgs(s) != True:
            print(s)
            sys.exit(0)
    print("Check those that should succeed DONE")

##############################################################################
##
##  Code for drawing (IF YOU ARE READING THIS YOU BETTER NOT BE CHANGING CODE DOWN HERE)
##
##############################################################################

# Draw X with lines in box beginning at (x,y) with given square size and color
def drawX(x, y, size, color="black"):
    setColor(color)
    line(x+15,y+15,x+size-15,y+size-15)
    line(x+size-15,y+15,x+15,y+size-15)

# Draw O with lines in box beginning at (x,y) with given square size and color    
def drawO(x, y, size, color="black"):
    setColor(color)
    setFill(None)
    ellipse(x+15,y+15,size-30,size-30)

# Draw hint information and X or O based on piece in given row, col of board
def drawHint(board, row, col, piece):
    setColor("orange")
    setFill(None)
    rows = board.rows()
    cols = board.cols()
    row_diff = int(HEIGHT/rows)
    col_diff = int(WIDTH/cols)
    rect(col*col_diff,row*row_diff,row_diff+1,col_diff+1)
    if piece == X:
        drawX(col*col_diff,row*row_diff,min(row_diff,col_diff), "orange")
    elif piece == O:
        drawO(col*col_diff,row*row_diff,min(row_diff,col_diff), "orange")

# Draw the board in given color
def drawBoard(board, color="black"):
    setColor("white")
    rect(0,0,WIDTH,HEIGHT)
    setColor(color)
    rows = board.rows()
    cols = board.cols()
    row_diff = int(HEIGHT/rows)
    col_diff = int(WIDTH/cols)
    for y in range(row_diff,HEIGHT-1,row_diff):
        line(0,y,WIDTH,y)
    for x in range(col_diff,WIDTH-1,col_diff):
        line(x,0,x,HEIGHT)
    for row in range(board.rows()):
        for col in range(board.cols()):
            if board.board[row][col] == X:
                drawX(col*col_diff,row*row_diff,min(row_diff,col_diff), color)
            elif board.board[row][col] == O:
                drawO(col*col_diff,row*row_diff,min(row_diff,col_diff), color)

#Setup window and draw initial white line to make it resize
def setupWindow():
    background("white")
    setColor("white")
    resize(WIDTH,HEIGHT)
    line(0,0,1,1)    

##############################################################################
##
##  Code for AI and hint for 3x3 tic-tac-toe (IF YOU ARE READING THIS YOU BETTER NOT BE CHANGING CODE DOWN HERE)
##
##############################################################################

#Main minmax, calls subfunction for recursion
#uses game board with player1 trying to decide move vs player 2, limit to depth given
def minmax1(board, player1, player2, depth):
    #Find all valid moves, shuffle for interesting
    moves = []
    rows = list(range(0,board.rows()))
    shuffle(rows)
    cols = list(range(0,board.cols()))
    shuffle(cols)
    for row in rows:
        for col in cols:
            if board.canPlay(row, col):
                moves.append([row,col])
    values = []
    #for each move if game won save value (make bigger than regular to show next play wins)
    #if not won recurse on game state for opponent playing
    for move in moves:
        row = move[0]
        col = move[1]
        board.play(row,col,player1)
        if board.won(player1):
            values.append(20)
        elif board.won(player2):
            values.append(-20)
        elif board.full():
            values.append(0)
        else:
            values.append(minmax2(board, player1, player2, False, depth-1))
        board.play(row,col,EMPTY)
    #Return best move found, next play wins first, followed by future wins, and ties, losses, and next play losses
    for i in range(len(moves)):
        if values[i] == 20:
            return moves[i][0], moves[i][1]
    for i in range(len(moves)):
        if values[i] == 10:
            return moves[i][0], moves[i][1]
    for i in range(len(moves)):
        if values[i] == 0:
            return moves[i][0], moves[i][1]
    for i in range(len(moves)):
        if values[i] == -10:
            return moves[i][0], moves[i][1]
    for i in range(len(moves)):
        if values[i] == -20:
            return moves[i][0], moves[i][1]
    return -1, -1
        
#Recursion minmax, calls itself for recursion
#uses game board with player1 trying to decide move vs player 2, limit to depth given
#not of maximze means it is player1's turn and not maximize is player2's turn
def minmax2(board, player1, player2, maximize, depth):
    if depth == 0:
        return 0
    #Find all valid moves, shuffle for interesting
    moves = []
    rows = list(range(0,board.rows()))
    shuffle(rows)
    cols = list(range(0,board.cols()))
    shuffle(cols)
    for row in rows:
        for col in cols:
            if board.canPlay(row, col):
                moves.append([row,col])
    values = [] 
    #for each move if game won save value
    #if not won recurse on game state for opponent playing
    for move in moves:
        row = move[0]
        col = move[1]
        if maximize:
            board.play(row,col,player1)
        else:
            board.play(row,col,player2)
        if board.gameover():
            if board.won( player1):
                board.play(row,col,EMPTY)
                return 10
            elif board.won( player2):
                board.play(row,col,EMPTY)
                return -10
            elif board.full():
                board.play(row,col,EMPTY)
                return 0
        result = minmax2(board, player1, player2, not maximize, depth-1)
        values.append(result)
        if maximize and result == 10:
            board.play(row,col,EMPTY)
            break
        elif not maximize and result == -10:
            board.play(row,col,EMPTY)
            break
        board.play(row,col,EMPTY)
    #Return maximial or minimal value found depending on recursion level
    if len(values) == 0:
        return 0
    if maximize:
        return max(values)
    else:
        return min(values)

#Calling AI, if level 4 we do full recursive minmax, if not we recurse only to certain depth
#If level=0 AI we just pick random open spot
def AI(board, level, human, computer):
    if level == 4:
        return minmax1(board, computer, human, board.rows()*board.cols()+1)
    elif level > 0 :
        return minmax1(board, computer, human, level*2)
    rows = list(range(0,board.rows()))
    shuffle(rows)
    cols = list(range(0,board.cols()))
    shuffle(cols)
    trying = True
    for row in rows:
        for col in cols:
            if board.canPlay( row, col):
                return row, col
    return -1, -1
 
##############################################################################
##
##  Main function (IF YOU ARE READING THIS YOU BETTER NOT BE CHANGING CODE DOWN HERE)
##
##############################################################################

def main():
    #testArgs()
    if not testCreateBoard():
        sys.exit(1)
    if not testPlay():
        sys.exit(1)
    testFull()
    testWinInRow()
    testWinInCol()
    testWinInDiag()
    testWon()
    testHint()
    rows = None
    cols = None
    difficulty = None
    human = None
    computer = None
    hint = None
    if not checkArgs(sys.argv):
        sys.exit(1)
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    difficulty = int(sys.argv[3])
    piece = sys.argv[4]
    if piece == "X":
        print("Human is X.")
        print("Computer is O.")
        human = X
        computer = O
    else:
        print("Human is O.")
        print("Computer is X.")
        human = O
        computer = X
    if(len(sys.argv) == 6):
        if sys.argv[5] == "-a":
            hint = "adv"
        else:
            hint = "hint"
    setupWindow()
    board = Board(rows,cols)
    drawBoard(board)
    player = X
    plays = 0
    while not board.gameover():
        value = (rows*cols)-plays
        if(value > 0):
            complexity = factorial(value)
            print("Estimated complexity of current game:",complexity)
        if human == player:
            print("Human player's turn.")
            if hint == "hint":
                row1, col1 = board.hint(human)
                row2, col2 = board.hint(computer)
                if row1 != -1:
                    print("Hint is row =",row1,"and col =",col1)
                    drawHint(board, row1,col1,human)
                elif row2 != -1:
                    print("Hint is row =",row2,"and col =",col2)
                    drawHint(board, row2,col2,human)
                else:
                    print("No hint")
            elif hint == "adv":
                row = -1
                col = -1
                if rows == cols == 3:
                    row, col = minmax1(board, human, computer, 5)
                else:
                    row, col = minmax1(board, human, computer, 4)
                if row != -1:
                    print("Hint is row =",row,"and col =",col)
                    drawHint(board, row,col,human)
                else:
                    print("No hint")

            trying = True
            while trying:
                selection = list(range(0,rows))
                row = -1
                while row < 0 or row > rows-1:
                    try:
                        row = int(input("Enter row "+str(selection)+": "))
                    except Exception as e:
                        print("Invalid row entered!")    
                selection = list(range(0,cols))
                col = -1
                while col < 0 or col > cols-1:
                    try:
                        col = int(input("Enter col "+str(selection)+": "))
                    except Exception as e:
                        print("Invalid row entered!")
                if board.canPlay(row, col):
                    board.play(row, col, human)
                    trying = False
                else:
                    print("Chosen location board["+str(row)+"]["+str(col)+"] is full!")
                print("Human plays in row",row,"and column",str(col)+".")
                player = computer
        else:
            row, col = AI(board, difficulty, human, computer)
            board.play(row, col, computer)
            print("AI plays in row",row,"and column",str(col)+".")
            player = human        
        drawBoard(board)
        plays+=1
    setFont("Times", "50", "bold")

    if board.won(X):
        if human == X:
            drawBoard(board, "green")
        else :
            drawBoard(board, "red")
        setColor("black")
        text(300,300,"X won!")
    elif board.won(O):
        if human == O:
            drawBoard(board, "green")
        else :
            drawBoard(board, "red")
        setColor("black")
        text(300,300,"O won!")
    else:
        drawBoard(board, "blue")
        setColor("black")
        text(300,300,"Board full. Draw.")

def checkArgs(args):
    if(len(args) != 5 and len(args) != 6):
        print("Arguments %s"% args)
        print("Usage: python tictactoe.py <rows> <cols> <difficulty> <piece> <optional -h hint -a advanced hint>")
        return False
    if not args[1].isdigit() or int(args[1]) not in [3,4,5]:
        print("Rows <%s> should be from [3,4]"%args[1])
        return False
    if not args[2].isdigit() or int(args[2]) not in [3,4,5]:
        print("Rows <%s> should be from [3,4]"%args[2])
        return False
    if (int(args[1])==int(args[2])==3):
        if not args[3].isdigit() or int(args[3]) not in [0,1,2,3,4]:
            print("Difficulty <%s> should be from [0=RANDOM,1=WINS,2=LOOKAHEAD1,3=LOOKAHEAD2,4=FULLAI]"%args[3])
            return False           
    elif not args[3].isdigit() or int(args[3]) not in [0,1,2,3]:
        print("Difficulty <%s> should be from [0=RANDOM,1=WINS,2=LOOKAHEAD1,3=LOOKAHEAD2]"%args[3])
        return False
    if args[4] != "X" and args[4] != "O":
        print("Piece <%s> should be from [X,O]"%args[4])
        return False
    if(len(args) == 6):
        if args[5] != "-h" and args[5] != "-a":
            print("Hint <%s> should be from [-h,-a]"%args[5])
            return False
    return True
        
main()

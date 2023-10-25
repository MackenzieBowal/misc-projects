
# This program consists of three constants and the Board class, which is used in the given tictactoe.py
# file. There are several methods in this class which all aid in evaluating the board, doing specific
# actions to the board, and ending the game.

#Constants for piece types
EMPTY = 0
X = 1
O = 2


class Board:
    board = None

#
# Constructor:
# Creates the board represented by a 2-dimensional list. All board "spaces"
# are filled with zeros (EMPTY)
#
# Parameters: self
#             rows: number of rows in the gameboard, default set to 3
#             cols: number of columns in the gameboard, default set to 3
#
# Returns: nothing
#

    def __init__(self, rows = 3, cols = 3):
       
        # creating the "board" attribute and initializing it as an empty list
        self.board = []
       
        # iterating through the number of rows given and creating an empty
        # list for each
        for row in range(rows):
            self.board.append([])
           
            # iterating through the number of columns given and appending an
            # EMPTY value for each
            for column in range(cols):
                self.board[row].append(EMPTY)

#
# Rows:
# Finds the number of rows in the gameboard by calculating the length of
# the board list
# Parameter: self
# Returns: the number of rows
#
   
    def rows(self):
        return len(self.board)

#
# Cols:
# Finds the number of columns in the gameboard by calculating the length
# of the first (always present) element of the board list, which is itself
# a list
# Parameter: self
# Returns: the number of columns
#

    def cols(self):
        firstIndex = 0
        return len(self.board[firstIndex])

#
# canPlay:
# Finds out if a given space on the gameboard is EMPTY (available) or not.
# Parameters: self
#             rowNum: the row number of the space
#             colNum: the column number of the space
# Returns: a boolean indicating whether or not that space is empty
#

    def canPlay(self, rowNum, colNum):
        # return True if the space in the indicated column and row is EMPTY
        if self.board[rowNum][colNum] == EMPTY:
            return True
        # otherwise, return False
        else:
            return False

#
# Play:
# Replaces a space in the gameboard with a desired piece
# Parameters: self
#             row: the row which contains the desired space
#             col: the column which contains the desired space
#             piece: the gamepiece (X or O) which is to be played in the space
# Returns: nothing
#

    def play(self, row, col, piece):
        self.board[row][col] = piece

#
# Full:
# Determines if the board is completely full, i.e., there are no EMPTY spaces left
# Parameter: self
# Returns: a boolean indicating whether or not the board is full
#
                   
    def full(self):
        # nested loop to access individual spaces in the gameboard
        for row in self.board:
            for column in row:
                # if there are any spaces that contain EMPTY, return False
                if column == EMPTY:
                    return False
        # if the loop is completed and none of the spaces were "EMPTY", return True
        return True


#
# winInRow:
# Determines if a player has gotten three consecutive pieces in a specific row
# Parameters: self
#             row: the specific row to check for a win in
#             piece: the gamepiece type of one of the players
# Returns: a boolean indicating whether or not a player has won in that row
#

    def winInRow(self, row, piece):
       
        # local variables used in this method to check the columns
        threeCols = 3
        fourCols = 4
        fiveCols = 5
        colZero = 0
        colOne = 1
        colTwo = 2
        colThree = 3
        colFour = 4

        # If the board has three columns:
        if self.cols() == threeCols:
            # return True if all three entries are equal to the player's piece
            if self.board[row][colZero] == self.board[row][colOne] == self.board[row][colTwo] == piece:
                return True

        # If the board has four columns:
        elif self.cols() == fourCols:
            # return True if the first three or the last three entries are equal to the player's piece
            if self.board[row][colZero] == self.board[row][colOne] == self.board[row][colTwo] == piece:
                return True
            elif self.board[row][colOne] == self.board[row][colTwo] == self.board[row][colThree] == piece:
                return True

        # If the board has five columns
        elif self.cols() == fiveCols:
            # return True if the first, middle, or last three entries are equal to the player's piece
            if self.board[row][colZero] == self.board[row][colOne] == self.board[row][colTwo] == piece:
                return True
            elif self.board[row][colOne] == self.board[row][colTwo] == self.board[row][colThree] == piece:
                return True
            elif self.board[row][colTwo] == self.board[row][colThree] == self.board[row][colFour] == piece:
                return True

        # If the program has reached this point, then the player has not won in
        # a row and the method returns false
        return False
           
#
# winInCol:
# Determines if a player has gotten three consecutive pieces in a specific column
# Parameters: self
#             col: the specific column to check for a win in
#             piece: the gamepiece type of one of the players
# Returns: a boolean indicating whether or not a player has won in that column
#
    def winInCol(self, col, piece):

        # local variables used in this method to check the rows
        threeRows = 3
        fourRows = 4
        fiveRows = 5
        rowZero = 0
        rowOne = 1
        rowTwo = 2
        rowThree = 3
        rowFour = 4

        # If the board has three rows:
        if self.rows() == threeRows:
           
            # return True if all three entries in that column are equal to the player's piece
            if self.board[rowZero][col] == self.board[rowOne][col] == self.board[rowTwo][col] == piece:
                return True

        # If the board has four rows:
        elif self.rows() == fourRows:
           
            # return True if the first three or the last three entires in the column are equal to the player's piece
            if self.board[rowZero][col] == self.board[rowOne][col] == self.board[rowTwo][col] == piece:
                return True
            elif self.board[rowOne][col] == self.board[rowTwo][col] == self.board[rowThree][col] == piece:
                return True
           
        # If the board has five rows:
        elif self.rows() == fiveRows:
           
            # return true if the first, middle, or last three entries in the column are equal to the player's piece
            if self.board[rowZero][col] == self.board[rowOne][col] == self.board[rowTwo][col] == piece:
                return True
            elif self.board[rowOne][col] == self.board[rowTwo][col] == self.board[rowThree][col] == piece:
                return True
            elif self.board[rowTwo][col] == self.board[rowThree][col] == self.board[rowFour][col] == piece:
                return True


        # If the program has reached this point, then the player has not won in
        # a column and the method returns false
        return False
       
#
# winInDiag:
# Determines if the player has achieved a win in any diagonal, forward or backward, with any grid dimensions. The function
# consists of an if-statement chain with executable code for each possible grid shape, and checks every set of indexes
# that could be a win in that diagonal.
# Parameters: self
#             piece: the gamepiece of one of the players
# Returns: a boolean indicating if the player has a win in any diagonal.
#

    def winInDiag(self, piece):
        # local variables to help search specific indexes
        indexZero = 0
        indexOne = 1
        indexTwo = 2
        indexThree = 3
        indexFour = 4

        # local variables to help differentiate between possible grid dimensions
        threeRows = 3
        threeCols = 3
        fourRows = 4
        fourCols = 4
        fiveRows = 5
        fiveCols = 5

        # The only two diagonals that all grids have in common:
        # Backward diagonal
        if self.board[indexZero][indexZero] == self.board[indexOne][indexOne] == self.board[indexTwo][indexTwo] == piece:
            return True
        # Forward diagonal
        elif self.board[indexZero][indexTwo] == self.board[indexOne][indexOne] == self.board[indexTwo][indexZero] == piece:
            return True
       

        # Possible diagonals in a 3x4 grid:
        if self.rows() == threeRows and self.cols() == fourCols:

            # Forward diagonal
            if self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == self.board[indexZero][indexThree] == piece:
                return True
           
            # Backward diagonal
            elif self.board[indexZero][indexOne] == self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True
           

        # Possible diagonals in a 4x3 grid:
        elif self.rows() == fourRows and self.cols() == threeCols:

            # Backward diagonal
            if self.board[indexOne][indexZero] == self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] == piece:
                return True

            # Forward diagonal
            elif self.board[indexThree][indexZero] == self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == piece:
                return True


        # Possible diagonals in a 4x4 grid:
        elif self.rows() == fourRows and self.cols() == fourCols:
           
            # Forward central diagonal
            if self.board[indexOne][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexThree][indexThree] == piece:
                return True
           
            # Forward lower and upper diagonals
            elif self.board[indexOne][indexZero] == self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] == piece:
                return True
            elif self.board[indexZero][indexOne] == self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True

            # Backward central diagonal
            elif self.board[indexThree][indexZero] == self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == self.board[indexZero][indexThree] == piece:
                return True

            # Backward lower and upper diagonals
            elif self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == piece:
                return True
           

        # Possible diagonals in a 4x5 grid:
        elif self.rows() == fourRows and self.cols() == fiveCols:
            # Forward lower diagonals
            if self.board[indexOne][indexZero] == self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] == piece:
                return True
            elif self.board[indexOne][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexThree][indexThree] == piece:
                return True

            # Forward upper diagonals
            elif self.board[indexZero][indexOne] == self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True
            elif self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == self.board[indexThree][indexFour] == piece:
                return True
            elif self.board[indexZero][indexTwo] == self.board[indexOne][indexThree] == self.board[indexTwo][indexFour] == piece:
                return True

            # Backward upper diagonals
            elif self.board[indexThree][indexZero] == self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == self.board[indexZero][indexThree] == piece:
                return True

            # Backward lower diagonals
            elif self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == piece:
                return True
            elif self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == self.board[indexZero][indexFour] == piece:
                return True
            elif self.board[indexThree][indexTwo] == self.board[indexTwo][indexThree] == self.board[indexOne][indexFour] == piece:
                return True

        # Possible diagonals in a 5x4 grid:
        elif self.rows() == fiveRows and self.cols() == fourCols:
           
            # Forward upper diagonals
            if self.board[indexThree][indexZero] == self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == self.board[indexZero][indexThree] == piece:
                return True

            # Forward lower diagonals
            elif self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == piece:
                return True
            elif self.board[indexFour][indexZero] == self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == piece:
                return True
            elif self.board[indexFour][indexOne] == self.board[indexThree][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True

            # Backward lower diagonals
            elif self.board[indexTwo][indexZero] == self.board[indexThree][indexOne] == self.board[indexFour][indexTwo] == piece:
                return True
            elif self.board[indexOne][indexZero] == self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] ==  self.board[indexFour][indexThree] == piece:
                return True

            # Backward upper diagonals
            elif self.board[indexOne][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexThree][indexThree] == piece:
                return True
            elif self.board[indexZero][indexOne] == self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True
           

        # Possible diagonals in a 5x5 grid:
        elif self.rows() == fiveRows and self.cols() == fiveCols:

            # Forward upper diagonals
            if self.board[indexThree][indexZero] == self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == self.board[indexZero][indexThree] == piece:
                return True

            # Forward central diagonal
            elif self.board[indexFour][indexZero] == self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == piece:
                return True
            elif self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == piece:
                return True
            elif self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == self.board[indexZero][indexFour] == piece:
                return True

            # Forward lower diagonals
            elif self.board[indexFour][indexOne] == self.board[indexThree][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True
            elif self.board[indexThree][indexTwo] == self.board[indexTwo][indexThree] == self.board[indexOne][indexFour] == piece:
                return True
            elif self.board[indexFour][indexTwo] == self.board[indexThree][indexThree] == self.board[indexTwo][indexFour] == piece:
                return True

            # Backward lower diagonals
            elif self.board[indexTwo][indexZero] == self.board[indexThree][indexOne] == self.board[indexFour][indexTwo] == piece:
                return True
            elif self.board[indexOne][indexZero] == self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] ==  self.board[indexFour][indexThree] == piece:
                return True

            # Backward central diagonal
            elif self.board[indexOne][indexOne] == self.board[indexTwo][indexTwo] == self.board[indexThree][indexThree] == piece:
                return True
            elif self.board[indexTwo][indexTwo] == self.board[indexThree][indexThree] == self.board[indexFour][indexFour] == piece:
                return True

            # Backward upper diagonals
            elif self.board[indexZero][indexOne] == self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True
            elif self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == self.board[indexThree][indexFour] == piece:
                return True
            elif self.board[indexZero][indexTwo] == self.board[indexOne][indexThree] == self.board[indexTwo][indexFour] == piece:
                return True

        # Possible diagonals in a 5x3 grid:
        elif self.rows() == fiveRows and self.cols() == threeCols:

            # Forward diagonals
            if self.board[indexThree][indexZero] == self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == piece:
                return True
            elif self.board[indexFour][indexZero] == self.board[indexThree][indexOne] == self.board[indexTwo][indexTwo] == piece:
                return True

            # Backward diagonals
            elif self.board[indexOne][indexZero] == self.board[indexTwo][indexOne] == self.board[indexThree][indexTwo] == piece:
                return True
            elif self.board[indexTwo][indexZero] == self.board[indexThree][indexOne] == self.board[indexFour][indexTwo] == piece:
                return True


        # Possible diagonals in a 3x5 grid:
        elif self.rows() == threeRows and self.cols() == fiveCols:

            # Forward diagonals
            if self.board[indexTwo][indexOne] == self.board[indexOne][indexTwo] == self.board[indexZero][indexThree] == piece:
                return True
            elif self.board[indexTwo][indexTwo] == self.board[indexOne][indexThree] == self.board[indexZero][indexFour] == piece:
                return True

            # Backward diagonals
            elif self.board[indexZero][indexOne] == self.board[indexOne][indexTwo] == self.board[indexTwo][indexThree] == piece:
                return True
            elif self.board[indexZero][indexTwo] == self.board[indexOne][indexThree] == self.board[indexTwo][indexFour] == piece:
                return True

        # If the player has not achieved a win in a diagonal, return False
        return False


#
# won:
# Determines whether or not a player has won in either a row, a column, or a diagonal.
# Parameters: self
#             piece: the gamepiece of one of the players
# Returns: a boolean returning True if the player has won in a row, column, or diagonal, and False if they have not.
#

    def won(self, piece):

        # for-loop to iterate through all the rows in the grid:
        for row in range(self.rows()):
            # Evaluating each row to see if there is a win:
            if self.winInRow(row, piece):
                return True
           
        # for-loop to iterate through all the columns in the grid:
        for col in range(self.cols()):
            # Evaluating each column to see if there is a win:
            if self.winInCol(col, piece):
                return True

        # Evaluating each possible diagonal to see if there is a win:
        if self.winInDiag(piece):
            return True

        # If the player has not won, return False
        return False


#
# hint:
# Evaluates all possible playable positions on the board and checks if playing there would result in a win for that player.
# Parameters: self
#             piece: the gamepiece of one of the players
# Returns: two numbers indicating the row and column of the space that will result in a win, and -1, -1 if there is no such space.
#
           
    def hint(self, piece):

        # for-loop iterating through all the rows in the grid
        for row in range(self.rows()):
           
            # nested for-loop iterating through all the spaces in each row
            for col in range(self.cols()):
               
                # if-statement checking if the player can play in that space, and playing if it returns True
                if self.canPlay(row, col):
                    self.play(row, col, piece)

                    # if-statement checking if that new move will result in a win, and changing the
                    # space back to EMPTY and returning the row and column if it does
                    if self.won(piece):
                        self.board[row][col] = EMPTY
                        return row, col

                    # if that move does not result in a win, change the space back to EMPTY
                    # and finish the loop
                    else:
                        self.board[row][col] = EMPTY

        # If no winning space was found, return -1, -1
        return -1, -1


#
# gameover:
# Determines if the game is finished or not, having either X or O win, or having filled the board completely.
# Parameter: self
# Returns: a boolean, either True (a player has won or the board is full) or False (no player has won or the board is not full).
#

    def gameover(self):
        if self.won(X) or self.won(O) or self.full():
            return True
        return False


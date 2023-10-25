/*
 * This program emulates a search engine. The user will enter two integers 
 * between 5 and 20 in the command line, and optionally a file name as well. 
 * If no file name is given, the program randomly populates a 2-dimensional 
 * array to make a matrix with the dimensions specified by the command line 
 * arguments. If a file name is given, the program populates the matrix by 
 * reading from the file. 
 * Each row is considered a document, and the columns represent specific 
 * words within the documents. 
 * The user is then prompted for the index of the word they would like to search 
 * for, and the number of top documents they would like to retrieve. The program 
 * utilizes the bubble sort algorithm to determine the order of the documents 
 * according to word frequency. The top number of documents as specified by 
 * the user is printed to the console and input and output information 
 * is written to a log file. 
 * The user can repeatedly search the original 2-dimensional array until 
 * they wish to exit the program.
 */

.data					// Data section: for accepting user input
indexToSearch:  .word 0
numDocuments:   .word 0
continue:       .word 0


.text
invalidInputMsg:        .string "Please enter two integers through the command line.\n"                                 // Error message string for invalid number of command line arguments
invalidRangeMsg:        .string "Please enter two integers between 5 and 20 through the command line.\n"                // Error message string for input out of range
docInfoMsg:     .string "Document %d:\n\tMax Word Index: %d\n\tMax Word Occurrences: %d\n\tMax Word Frequency: %d\n"    // String that prints information about each document
printNum:       .string "%-4d"                                                                                          // For printing elements of the table to the console
newline:        .string "\n"                                                                                            // To print a new line
fileErrorMsg:   .string "Error: could not open file %s\n"
displayMsg:     .string "\nThese are the documents:\n\n"
inputMsg1:      .string "Enter the index of the word you are searching for: "
inputMsg2:      .string "How many top documents do you want to retrieve? "
scanInt:        .string "%d"
topDocMsg:      .string "The top %d documents are:\n"
topDoc:         .string "#%d: Document %d\n"							// For printing the top documents
inputLoopMsg1:  .string "That was not a valid index. Please try again: "			// Input validation messages
inputLoopMsg2:  .string "That was not a valid number of documents. Please try again: "
contPrompt:     .string "Enter -1 to quit, or 0 to continue searching: "
appendMode:	.string "a"
logFileName:	.string "assign5.log"								// Sets the log file name for writing
tableStr:	.string "These are the documents:\n\n"						
indexStr:	.string "The index searched: %d\n"
numDocStr:	.string "The number of documents returned: %d\n"


fp .req x29                    		// Register equate for the frame pointer
lr .req x30                     	// Register equate for the link register

        define(argc_r, w19)             // Macros for accessing command line arguments
        define(argv_r, x20)             

        define(rows, w21)               // rows is the number of documents, specified by the user
        define(cols, w22)               // cols is the number of words per document, specified by the user

        define(fileName, x23)
        define(useFile, w24)		// Used to determine if the user entered a file name or not
        define(fileValid, w24)		// Used to determine if the file name entered was valid or not
        define(fd_r, w12)
        define(buffer_base, x21)
        define(numElements, w20)	
        define(readBytes, w20)		// How many bytes to read from the file
        define(elementCounter, w19)
        define(maxRange, w9)		
        define(minRange, w10)
        define(randNum, w11)
        define(table_base, x28)		// Address of the table
        define(rowCounter, w19)         // rowCounter is used to iterate through the documents in the loops
        define(colCounter, w20)         // colCounter is used to iterate through the words in a document in the loop
        define(element_offset, w26)
        define(tableElement, w27)
        define(searchIndex, w23)	// Which word the user would like to search for
        define(numDocs, w25)		// How many documents the user would like to return
        define(docSize, w24)
        define(f_docSize, s8)
        define(f_wordOccurrences, s9)
        define(f_frequency, s10)
        define(this_freq, s11)
        define(next_freq, s12)
        define(swap, w24)
        define(index1, w23)
        define(index2, w27)
        define(docIndex, w23)
        define(cont, w26)
	define(sortedTable_base, x26)	// Address of the sorted array
	define(logFile, x24)		// file descriptor for the log file
	define(offset, w13)


        define(randNum_r, w25)          // randNum_r is used to generate and store a random number, for populating the table
        define(Arr_offset, w26)         // Arr_offset is used to calculate the offset from fp of elements in the table, for loads and stores
        define(maxWord, w27)            // maxWord is used to store the word with the highest occurrence in a document
        define(arrElement, w28)         // arrElement is used to store the number of occurrences of a word in a document
        define(docSize_r, w19)          // docSize_r is used to keep track of the size of a document
        define(maxFreq_r, w20)          // maxFreq_r is used to calculate the maximum frequency of a document
        define(maxWordIndex_r, w21)     // maxWordIndex_r is the index of the highest word in a document
        define(struct_offset, w26)      // struct_offset is used to calculate the offset from fp of elements in the struct array
        define(structSize_r, w28)       // structSize_r is used to calculate struct_offset
        define(maxWordIndex, w21)       // maxWordIndex is also used as the index of the highest word of a document
        define(A_offset, w26)           // A_offset is the word-length version of Arr_offset, used for different instructions



        tableSize_s = 4
        buffer_s = 20
        AT_FDCWD = -100

        row_size = 4                            // Equate for the bytes used to store rows on the stack
        row_s = structArr_s + struct_size*16    // Equate for the offset of the row variable on the stack from fp
        docArr_size = 20*20*1                   // Equate for the max possible size of the document array: 20 rows by 20 columns at 1 byte each
        struct_size = 4*2                       // Equate for the size of each entry in the struct array: 2 variables of 4 bytes each
        structArr_s = docArr_size + 16          // Equate for the offset of the beginning of the struct array from fp
        docArr_s = 16                           // Equate for the offset of the beginning of the table array from fp

        alloc = -(16 +docArr_size + row_size) & -16   // Equate for the stack memory needed to allocate to sp
        dealloc = -alloc        // Equate for the stack memory to deallocate at the end of the program

        trdAlloc = -475 & -16
        trdDealloc = -trdAlloc
        initAlloc = -(475) & -16
        initDealloc = -initAlloc
	LTFAlloc = -(100) & -16
	LTFDealloc = -LTFAlloc


        .balign 4               // Ensures instructions are properly aligned
        .global main            // Makes the label "main" visible to the linker


//=============================================\\


/**
 * initialize
 * Populates a given 2-dimensional array, either by reading from a file specified by the user
 * or randomly. Also sets the seed for the rand() function in initialize(), which is called if
 * the table is populated randomly.
 * Parameters:
 * 	table_base - the base address of the table to be populated
 * 	useFile - integer is 0 if no file was given and 1 if a file was given
 * 	fileName - the name of the file (only applicable if one was given)
 *	rows, cols - dimensions of the board
 */



initialize:
        stp fp, lr, [sp, initAlloc]!
        mov fp, sp
	
        str w21, [fp, 16]			// Stores callee-saved register modified in this subroutine

        					// Gets parameters
        mov table_base, x0
        mov useFile, w1
        mov fileName, x2
        mov rows, w3
        mov cols, w4
        mul numElements, rows, cols

        					// Seeds rand
        mov x0, 0
        bl time
        bl srand

        					// Checks to populate with file or randomly
        cmp useFile, 0
        b.eq populateRandomly
        
populateFile:					// Opens bin file
        mov w0, AT_FDCWD
        mov x1, fileName
        mov w2, 0
        mov w3, 0
        mov x8, 56
        svc 0
        mov fd_r, w0
        cmp fd_r, -1
        b.gt fileOpened

        ldr x0, =fileErrorMsg			// Prints an error message and exit to calling
        mov x1, fileName			// code if the file could not be opened
        bl printf
        mov fileValid, 0
        b exitInitialize

fileOpened:
        add buffer_base, fp, buffer_s		// Sets the buffer base for reading the file

readFile:
        mov fileValid, 1			// Reads the file
        mov x1, buffer_base
        lsl w2, numElements, 2
        mov x8, 63
        svc 0
        mov elementCounter, 0

strElementLoop:
        mov element_offset, elementCounter				// Transfers the integers read from the buffer
        ldr tableElement, [buffer_base, element_offset, SXTW 2]		// to the table, according to the dimensions
        mov element_offset, elementCounter				// specified by the user
        strb tableElement, [table_base, element_offset, SXTW]
        add elementCounter, elementCounter, 1

        cmp elementCounter, numElements
        b.lt strElementLoop

endReading:								// Closes the file, exits back to calling code
        mov w0, fd_r		
        mov x8, 57
        svc 0

        b exitInitialize

populateRandomly:							// If no file was given, populates the table with random integers
        mov rowCounter, 0
        mov fileValid, 1

outerLoop2:								// Outer loop for populating randomly - row by row
        mov colCounter, 0
        b innerLoopTest2

innerLoop2:								// Inner loop for populating randomly - column by column
        madd element_offset, rowCounter, cols, colCounter
        mov w0, 9
        mov w1, 0
        bl randomNum
        mov tableElement, w0
        strb tableElement, [table_base, element_offset, SXTW]
        add colCounter, colCounter, 1
        b innerLoopTest2

innerLoopTest2:								// Fills entries until that row is filled
        cmp colCounter, cols
        b.lt innerLoop2

        add rowCounter, rowCounter, 1

outerLoopTest2:								// Fills rows until the table is filled
        cmp rowCounter, rows
        b.lt outerLoop2
								// Exits back to calling code
exitInitialize:
	ldr w21, [fp, 16]					// Restores callee-saved register
        mov w0, fileValid					// Returns fileValid
        ldp fp, lr, [sp], initDealloc
        ret



//=============================================\\


/**
 * randomNum
 * Generates and returns a random integer between two given integers
 * Parameters:
 * 	maxRange is the maximum value (inclusive) returned by the random number generator
 *  	minRange is the minimum value to be returned
 */

randomNum:
        stp fp, lr, [sp, -16]!
        mov fp, sp

        add maxRange, w0, 1		// Gets parameters
        mov minRange, w1

        bl rand				// Generates a random number and uses modulus
        mov randNum, w0			// to restrict its range
        mov w10, maxRange
        sdiv w11, w0, w10
        mul randNum, w11, w10
        sub randNum, w0, randNum

        mov w0, randNum			// Returns the random number generated

        ldp fp, lr, [sp], 16
        ret



//=============================================\\

/**
 * display
 * Prints the contents of the table to the console
 * Parameters:
 * 	table_base - the address to the table
 *	rows, cols - the dimensions of the table
 */

display:
        stp fp, lr, [sp, -16]!
        mov fp, sp

        mov table_base, x0						// Gets parameters
	mov rows, w1
	mov cols, w2
        mov rowCounter, 0

        ldr x0, =displayMsg						// Prints a display message
        bl printf

outerLoop3:								// Loops through printing the rows
        mov colCounter, 0
        b innerLoopTest3

innerLoop3:								// Loops through printing the columns, by
        madd element_offset, rowCounter, cols, colCounter		// loading each element from stack memory
        ldrb tableElement, [table_base, element_offset, SXTW]

        ldr x0, =printNum
        mov w1, tableElement
        bl printf
        add colCounter, colCounter, 1
        b innerLoopTest3

innerLoopTest3:								// Prints elements until the row is complete
        cmp colCounter, cols
        b.lt innerLoop3

        ldr x0, =newline						// Prints a newline character after each row
        bl printf

        add rowCounter, rowCounter, 1

outerLoopTest3:								// Prints rows until the table is complete
        cmp rowCounter, rows
        b.lt outerLoop3

exitDisplay:								// Exits the subroutine and return to calling code
        ldp fp, lr, [sp], 16
        ret


//=============================================\\


/**
 * topRelevantDocs
 * Determines the order of the documents according to decreasing frequency of a given word's index. Prints the 
 * resulting top documents to the console, where the number of documents printed is determined by the user. Passes 
 * information to the logToFile() function to write the result to a file.
 * Parameters:
 * 	table_base - the address to the table
 * 	numDocs - the number of top documents to find in this search
 * 	searchIndex - the word index for this search
 */

topRelevantDocs:
        stp fp, lr, [sp, trdAlloc]!
        mov fp, sp

        mov table_base, x0					// Gets parameters
        mov numDocs, w2
        mov searchIndex, w1

        mov rowCounter, 0					// Sets up registers for the function
	scvtf d15, searchIndex

outerLoop4:							// Loops through each row, calculating the
        mov colCounter, 0					// frequency of the given word and storing 
        mov docSize, 0						// the frequency and document number to the stack

innerLoop4:
        madd element_offset, rowCounter, cols, colCounter	// Goes through each element of the row and adds
        ldrb tableElement, [table_base, element_offset, SXTW]	// the occurrences to the document size
        add docSize, docSize, tableElement

        add colCounter, colCounter, 1

innerLoopTest4:							// Loops through columns until the row is done
        cmp colCounter, cols
        b.lt innerLoop4


        madd element_offset, rowCounter, cols, searchIndex	// Calculates the frequency for the specified
        ldrb tableElement, [table_base, element_offset, SXTW]   // word in each row
        scvtf f_docSize, docSize
        scvtf f_wordOccurrences, tableElement
        fdiv f_frequency, f_wordOccurrences, f_docSize
        lsl element_offset, rowCounter, 3
        add element_offset, element_offset, 16
        str rowCounter, [fp, element_offset, SXTW]		// Stores the row's document number and frequency
        add element_offset, element_offset, 4			// to the stack
        str f_frequency, [fp, element_offset, SXTW]

        add rowCounter, rowCounter, 1

outerLoopTest4:							// Loops through each row until the table is done
        cmp rowCounter, rows
        b.lt outerLoop4


sortLoop:							// Sorts the frequencies in descending order, using
        mov swap, 0						// bubble sort
        mov rowCounter, 0

swapLoop:							// Compares "this" frequency with the next frequency
        lsl element_offset, rowCounter, 3
        add element_offset, element_offset, 20
        ldr this_freq, [fp, element_offset, SXTW]

        add element_offset, element_offset, 8
        ldr next_freq, [fp, element_offset, SXTW]

        add rowCounter, rowCounter, 1

        fcmp this_freq, next_freq
        b.lt swapElements

        b swapLoopTest

swapElements:							// Performs a swap if they are out of order
        add swap, swap, 1

        sub element_offset, element_offset, 12		
        ldr index1, [fp, element_offset, SXTW]		// Get a temporary index
        add element_offset, element_offset, 8
        ldr index2, [fp, element_offset, SXTW]		// Get another temporary index
        str index1, [fp, element_offset, SXTW]		// Store the first index where it belongs
        sub element_offset, element_offset, 8
        str index2, [fp, element_offset, SXTW]		// Store the second index where it belongs

        add element_offset, element_offset, 4
        str next_freq, [fp, element_offset, SXTW]	// Store the second frequency where it belongs
        add element_offset, element_offset, 8
        str this_freq, [fp, element_offset, SXTW]	// Store the first frequency where it belongs

swapLoopTest:							// Iterates through the whole table
        cmp rowCounter, rows
        b.lt swapLoop

sortLoopTest:							// Stops the algorithm once none of the
        cmp swap, 0						// frequencies have to be swapped, i.e. they
        b.gt sortLoop						// are all sorted


printTopDocs:							// Starts printing the search result to the console
        ldr x0, =topDocMsg
        mov w1, numDocs
        bl printf

        mov rowCounter, 0
        b printLoopTest

printLoop:							// Prints the top n documents to the console
        lsl element_offset, rowCounter, 3
        add element_offset, element_offset, 16
        ldr docIndex, [fp, element_offset, SXTW]		// Loads the document index from the stack

        add rowCounter, rowCounter, 1

        ldr x0, =topDoc
        mov w1, rowCounter
        mov w2, docIndex
        bl printf

printLoopTest:							// Loops through printing until the number
        cmp rowCounter, numDocs					// of documents chosen by the user is reached
        b.lt printLoop

	add sortedTable_base, fp, 16				// Prepares registers for calling the
	fcvtns searchIndex, d15					// logToFile() subroutine

//Call logToFile
	mov w0, rows						// Calls the logToFile() subroutine
	mov w1, cols
	mov x2, table_base
	mov w3, numDocs
	mov x4, sortedTable_base
	mov w5, searchIndex
	bl logToFile

exitTRD:							// Exits and returns to calling code
        ldp fp, lr, [sp], trdDealloc
        ret


//=============================================\\


/**
 * logToFile
 * Appends the input/output information from the latest search to a file named "assign5.log". 
 * Writes the table, as well as the word index, number of documents, and resulting top documents 
 * of the search, to the file.
 * Parameters:
 * 	rows, cols - the table dimensions
 * 	table_base - base address for the table
 * 	numDocs - the number of documents specified by the user in this search
 * 	sortedTable_base - base address of the sorted document indices and frequencies
 * 	searchIndex - the index of the word specified by the user in this search
 */


logToFile:

       	stp fp, lr, [sp, LTFAlloc]!
       	mov fp, sp 

	//store registers
	stp x19, x20, [fp, 16]					// Stores callee-saved registers
	stp x21, x22, [fp, 32]
	stp x23, x24, [fp, 48]
	stp x25, x26, [fp, 64]
	stp x27, x28, [fp, 80]

	mov rows, w0						// Gets parameters
	mov cols, w1
	mov table_base, x2
	mov numDocs, w3
	mov sortedTable_base, x4
	mov searchIndex, w5
	
	ldr x0, =logFileName					// Opens the log file, gets a file descriptor
	ldr x1, =appendMode
	bl fopen
	mov logFile, x0

	mov x0, logFile						// Writes an intro message to the file
	ldr x1, =tableStr
	bl fprintf

	mov rowCounter, 0
	
logRows:							// Loops through the rows of the table
	mov colCounter, 0

logCols:							// Loops through the columns of the table
	madd offset, rowCounter, cols, colCounter
	ldrb tableElement, [table_base, offset, SXTW]	// Loads and prints the table element
	mov x0, logFile
	ldr x1, =printNum
	mov w2, tableElement
	bl fprintf

logColsTest:							// Loops until the row is complete
	add colCounter, colCounter, 1
	cmp colCounter, cols
	b.lt logCols

logRowsTest:
	mov x0, logFile						// Prints a new line after each row
	ldr x1, =newline
	bl fprintf

	add rowCounter, rowCounter, 1				// Loops until the table is done
	cmp rowCounter, rows
	b.lt logRows

	mov x0, logFile						// Prints a new line to the file
	ldr x1, =newline
	bl fprintf

	mov x0, logFile						// Writes the user input for word index
	ldr x1, =indexStr
	mov w2, searchIndex
	bl fprintf
	
	mov x0, logFile						// Writes the user input for number of documents
	ldr x1, =numDocStr
	mov w2, numDocs
	bl fprintf
	
	mov x0, logFile						// Writes the top document message
	ldr x1, =topDocMsg
	mov w2, numDocs
	bl fprintf

	mov rowCounter, 0

logDocs:							// Loops through the sorted array and prints
	lsl offset, rowCounter, 3				// the top n documents
	ldr docIndex, [sortedTable_base, offset, SXTW]
	add rowCounter, rowCounter, 1
	mov x0, logFile
	ldr x1, =topDoc
	mov w2, rowCounter
	mov w3, docIndex
	bl fprintf

	cmp rowCounter, numDocs					// Loops through the top documents until the
	b.lt logDocs						// number specified by the user is reached

	mov x0, logFile						// Prints a new line to the file
	ldr x1, =newline
	bl fprintf

	mov x0, logFile						// Closes the file
	bl fclose

	// restore registers
	ldp x19, x20, [fp, 16]					// Restores callee-saved registers
	ldp x21, x22, [fp, 32]		
	ldp x23, x24, [fp, 48]
	ldp x25, x26, [fp, 64]
	ldp x27, x28, [fp, 80]

exitLTF:							// Exits and returns to calling code
        ldp fp, lr, [sp], LTFDealloc
        ret

//=============================================\\

/**
 * main
 * Executes the program by calling other functions. First, checks and handles the command line arguments,
 * then creates, populates, and displays the table. Loops through the functionality of getting input
 * and finding the top documents until the user wishes to quit.
 * Parameters:
 * 	argc_r - is a count of the command line arguments entered by the user. It should
 *  		be either 3 (no file) or 4 (file)
 *  	argv_r - contains the command line arguments. The first element is expected to be the name
 *  		of the program, the second and third is expected to be integers corresponding to rows and columns,
 *  		and the fourth (optional) is expected to be a file name
 */

main:
        stp fp, lr, [sp, alloc]!        // Saves the state of registers used by calling code, allocates space in stack memory
        mov fp, sp                      // Updates FP to the current SP

        mov useFile, 0                  // Initially sets useFile to false (0)

        mov argc_r, w0                  // Gets the count of the command line arguments from w0
        mov argv_r, x1                  // Gets the pointer to the command line arguments from x1

        cmp argc_r, 4			// Checks if a file name was given
        b.eq fileGiven
        b noFile

fileGiven:				// If a file name was given, loads it to a register
        ldr fileName,  [argv_r, 24]
        mov useFile, 1                  // sets useFile to true (1)
        b rowsAndCols

noFile:					// If no file name was given, checks to make sure
        cmp argc_r, 3			// there are the right number of command line arguments
        b.ne invalidNumArgs
        b rowsAndCols

invalidNumArgs:				// If there are <3 or >4 command line arguments, prints
        ldr x0, =invalidInputMsg	// an error message and exits the program
        bl printf
        b exit

rowsAndCols:
        ldr x0, [argv_r, 8]             // Gets the rows from the command line
        bl atoi            
        mov rows, w0          

        ldr x0, [argv_r, 16]            // Gets the columns from the command line
        bl atoi               
        mov cols, w0                

        cmp rows, 5                   	// Checks that the rows and columns are in range 5-20
        b.lt invalidRangeArgs       
        cmp rows, 20                  
        b.gt invalidRangeArgs         
        cmp cols, 5                    
        b.lt invalidRangeArgs        
        cmp cols, 20                   
        b.gt invalidRangeArgs     
        b next                      

invalidRangeArgs:			// Prints an error message and quits the program if
        ldr x0, =invalidRangeMsg	// the rows or columns were out of range
        bl printf
        b exit

next:					// Initializes the table
        add table_base, fp, 16
        mov x0, table_base
        mov w1, useFile
        mov x2, fileName
        mov w3, rows
        mov w4, cols
        bl initialize

        mov fileValid, w0		// If the file was invalid, exits the program
        cmp fileValid, 0
        b.eq exit

        mov x0, table_base		// Displays the table
	mov w1, rows
	mov w2, cols
        bl display

getInput:				// Prompts the user for input about the index to search
        ldr x0, =inputMsg1
        bl printf			// Prints the prompt message

        ldr x0, =scanInt
        ldr w1, =indexToSearch
        bl scanf			// Scans for the user's response

        ldr searchIndex, indexToSearch

        cmp searchIndex, cols		// Checks if the index is in range
        b.ge invalidSearchIndex
        cmp searchIndex, 0
        b.lt invalidSearchIndex
        b input2

invalidSearchIndex:
        ldr x0, =inputLoopMsg1		// If the index was not in range, prints another prompt message
        bl printf

        ldr x0, =scanInt
        ldr w1, =indexToSearch
        bl scanf			// Scans for user input again

        ldr searchIndex, indexToSearch

        cmp searchIndex, cols		// Checks if the index is in range
        b.ge invalidSearchIndex
        cmp searchIndex, 0
        b.lt invalidSearchIndex

input2:					// Prompts the user for input about the number of documents
        ldr x0, =inputMsg2
        bl printf			// Prints the prompt message

        ldr x0, =scanInt
        ldr w1, =numDocuments
        bl scanf			// Scans for the user's response

        ldr numDocs, numDocuments

        cmp numDocs, rows		// Checks if the number of documents is in range
        b.gt invalidNumDocs
        cmp searchIndex, 0
        b.lt invalidNumDocs
        b afterInput

invalidNumDocs:				// If the number of documents was not in range,
        ldr x0, =inputLoopMsg2		// prints another prompt message
        bl printf

        ldr x0, =scanInt
        ldr w1, =numDocuments
        bl scanf			// Scans for user input again

        ldr numDocs, numDocuments

        cmp numDocs, rows		// Checks if the number of documents is in range
        b.gt invalidNumDocs
        cmp numDocs, 0
        b.lt invalidNumDocs

afterInput:				// Performs the functionality of the program
        mov x0, table_base
        mov w1, searchIndex
        mov w2, numDocs
        bl topRelevantDocs		// Calls the topRelevantDocs() subroutine

        ldr x0, =contPrompt		// Prompts the user to continue or quit
        bl printf

        ldr x0, =scanInt
        ldr w1, =continue
        bl scanf			// Scans for the user's response

        ldr cont, continue		// Checks that the user entered a valid response
        cmp cont, -1
        b.eq exit
        cmp cont, 0
        b.eq getInput

invalidCont:				// If the user did not enter -1 or 0, loops for valid input
        ldr x0, =contPrompt
        bl printf			// Prints the prompt message again

        ldr x0, =scanInt
        ldr w1, =continue
        bl scanf			// Scans for a new response

        ldr cont, continue		// Checks the response again
        cmp cont, -1
        b.eq exit
        cmp cont, 0
        b.eq getInput
        b invalidCont

exit:
        ldp fp, lr, [sp], dealloc       // Restores the state of the FP and LR registers, and deallocates 406 bytes in stack memory
        ret                             // Returns control to calling code, ends the program




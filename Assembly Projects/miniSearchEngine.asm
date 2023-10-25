
// This program emulates a search engine. The user enters two integers between 4 and 16
// through the command line, and then a table with the specified dimensions is randomly 
// populated with integers between 1 and 16. This table is stored as a 2D array on the stack.
// Each row represents a document, and each column represents a word in that row. The values
// at each entry are the number of occurrences of the word in the document. 
// For each document, the index, frequency and number of occurrences of the most common word
// is found and printed to the console. In addition, the top index and frequency of each document
// are stored to the stack as structs.

.text
invalidInputMsg:        .string "Please enter two integers through the command line.\n"                                 // Error message string for invalid number of command line arguments
invalidRangeMsg:        .string "Please enter two integers between 4 and 16 through the command line.\n"                // Error message string for input out of range
docInfoMsg:     .string "Document %d:\n\tMax Word Index: %d\n\tMax Word Occurrences: %d\n\tMax Word Frequency: %d\n"    // String that prints information about each document
printNum:       .string "%-4d"                                                                                          // For printing elements of the table to the console
newline:        .string "\n"                                                                                            // To print a new line

fp .req x29                     // Register equate for the frame pointer
lr .req x30                     // Register equate for the link register

        define(argc_r, w19)             // argc_r is used to store the number of comamnd line arguments
        define(argv_r, x20)             // argv_r is used to access the command line arguments
        define(rows, x21)               // rows is the number of documents, specified by the user
        define(cols, x22)               // cols is the number of words per document, specified by the user
        define(rowCounter, x23)         // rowCounter is used to iterate through the documents in the loops
        define(colCounter, x24)         // colCounter is used to iterate through the words in a document in the loop
        define(randNum_r, w25)          // randNum_r is used to generate and store a random number, for populating the table
        define(Arr_offset, x26)         // Arr_offset is used to calculate the offset from fp of elements in the table, for loads and stores
        define(maxWord, w27)            // maxWord is used to store the word with the highest occurrence in a document
        define(arrElement, w28)         // arrElement is used to store the number of occurrences of a word in a document
        define(docSize_r, w19)          // docSize_r is used to keep track of the size of a document
        define(maxFreq_r, w20)          // maxFreq_r is used to calculate the maximum frequency of a document
        define(maxWordIndex_r, x21)     // maxWordIndex_r is the index of the highest word in a document
        define(struct_offset, x26)      // struct_offset is used to calculate the offset from fp of elements in the struct array
        define(structSize_r, x28)       // structSize_r is used to calculate struct_offset
        define(maxWordIndex, w21)       // maxWordIndex is also used as the index of the highest word of a document
        define(A_offset, w26)           // A_offset is the word-length version of Arr_offset, used for different instructions

        row_size = 8                            // Equate for the bytes used to store rows on the stack
        row_s = structArr_s + struct_size*16    // Equate for the offset of the row variable on the stack from fp
        docArr_size = 16*16*1                   // Equate for the max possible size of the document array: 16 rows by 16 columns at 1 byte each
        struct_size = 4*2                       // Equate for the size of each entry in the struct array: 2 variables of 4 bytes each
        structArr_s = docArr_size + 16          // Equate for the offset of the beginning of the struct array from fp
        docArr_s = 16                           // Equate for the offset of the beginning of the table array from fp

        alloc = -(16 + docArr_size + struct_size*16 + row_size) & -16   // Equate for the stack memory needed to allocate to sp
        dealloc = -alloc        // Equate for the stack memory to deallocate at the end of the program

        .balign 4               // Ensures instructions are properly aligned
        .global main            // Makes the label "main" visible to the linker

main:
        stp fp, lr, [sp, alloc]!        // Saves the state of registers used by calling code, allocates 406 bytes in stack memory
        mov fp, sp                      // Updates FP to the current SP

        mov argc_r, w0                  // Gets the count of the command line arguments from w0
        mov argv_r, x1                  // Gets the pointer to the command line arguments from x1

        cmp argc_r, 3                   // Compares the number of comman line arguments the 3
        b.ne invalidNumArgs             // Branches to "invalidNumArgs" if there are not 3 command line arguments
        b rowsAndCols                   // Otherwise, branches to rowsAndCols

invalidNumArgs:
        ldr x0, =invalidInputMsg        // Loads the error message into x0 for printing
        bl printf                       // Prints the error message to the console
        b end                           // Branches to the end of the program

rowsAndCols:
        ldr x0, [argv_r, 8]             // Loads the second command line argument, the number of rows, into x0
        bl atoi                         // Converts the second command line argument from a string to an int
        mov rows, x0                    // Sets the rows register to the return value of the atoi function call

        ldr x0, [argv_r, 16]            // Loads the third command line argument, the number of columns, into x0
        bl atoi                         // Converts the third command line argument from a string to an int
        mov cols, x0                    // Sets the cols register to the return value of the atoi function call

        cmp rows, 4                     // Compares the number of rows inputted by the user to 4
        b.lt invalidRangeArgs           // Branches to "invalidRangeArgs" if rows is less than 4
        cmp rows, 16                    // Compares the number of rows inputted by the user to 16
        b.gt invalidRangeArgs           // Branches to "invalidRangeArgs" if rows is greater than 16
        cmp cols, 4                     // Compares the number of cols inputted by the user to 4
        b.lt invalidRangeArgs           // Branches to "invalidRangeArgs" if cols is less than 4
        cmp cols, 16                    // Compares the number of cols inputted by the user to 16
        b.gt invalidRangeArgs           // Branches to "invalidRangeArgs" if cols is greater than 16
        b populate                      // If the command line arguments are all valid, continues to "populate"

invalidRangeArgs:
        ldr x0, =invalidRangeMsg        // Loads the error message into x0 for printing
        bl printf                       // Prints the error message to the console
        b end                           // Branches to the end of the program

populate:
        str rows, [fp, row_s]		// Stores the number of rows to the stack to free up register x21

        mov x0, 0                       // Sets x0 to 0 for seeding purposes
        bl time                         // Calls time function for seeding purposes
        bl srand                        // Seeds the rand function
        mov rowCounter, 0               // Sets the rowCounter initially to zero
        mov Arr_offset, 0               // Sets the array offset initially to zero
        b outerLoopTest1                // Branches to the test for the outer loop

outerLoop1:
        mov colCounter, 0                               // Sets colCounter to zero for the current document
        mov maxWord, 0                                  // Sets the maxWord to zero for the current document
        mov docSize_r, 0                                // Sets the document size to zero for the current document
        b innerLoopTest1                                // Branches to the test for the inner loop

innerLoop1:
        bl rand                                         // Calls the rand function to generate an integer
        mov randNum_r, w0                               // Puts the random integer into randNum_r
        mov x10, 16                                     // Sets register x10 to 16 for future use in restricting
                                                        // the random number to be between 1 and 16
        sdiv x11, x0, x10                               // Divides the original integer by 10 and stores the
                                                        // value (without the remainder) in x11
        mul randNum_r, w11, w10                         // Multiplies the value in x11 by 16
        sub randNum_r, w0, randNum_r                    // Subtracts the original value by the current value of
                                                        // randNum_r to get the value of the remainder, which will
                                                        // be between 0 and 15
        add randNum_r, randNum_r, 1                     // Adds 1 to the result of the above operations, to ensure
                                                        // a range of 1-16

        mul Arr_offset, rowCounter, cols                // Increases the array offset according to which row is being populated
        add Arr_offset, Arr_offset, docArr_s            // Increases the offset by 16 to account for the frame record
        add Arr_offset, Arr_offset, colCounter          // Increases the offset according to which column is being populated

        strb randNum_r, [fp, Arr_offset]                // Stores the generated number to the appropriate byte in the stack

        ldr x0, =printNum                               // Loads the "printNum" string into x0 for printing
        mov w1, randNum_r                               // Copies the generated number into w1 for printing
        bl printf                                       // Prints the generated array entry to the console

        add docSize_r, docSize_r, randNum_r             // Updates the document size with the occurrences of the current word

        add colCounter, colCounter, 1                   // Increments the colCounter by 1

        cmp randNum_r, maxWord                          // Compares the new entry to the highest occurring word so far in the current document
        b.le innerLoopTest1                             // If the new entry is not greater than the highest word, branches to the inner loop test
        mov maxWord, randNum_r                          // Otherwise, updates the maxWord to the new highest word
        sub maxWordIndex_r, colCounter, 1               // Updates the maxWordIndex to the index of the new highest word

innerLoopTest1:
        cmp colCounter, cols                            // Compares the colCounter to the total number of columns
        b.lt innerLoop1                                 // Branches to the beginning of the inner loop if there are more columns to populate

        ldr x0, =newline                                // Loads the new line string into x0 for printing
        bl printf                                       // Prints a new line to the console

        mov w26, 100                                    // Sets register w26 to 100 for frequency calculation
        mul maxFreq_r, maxWord, w26                     // Multiplies the document's highest word by 100 as part of the frequency calculation
        udiv maxFreq_r, maxFreq_r, docSize_r            // Calculates the frequency by dividing the previous result by the document size

        mov structSize_r, 8                             // Sets structSize_r to 8 in order to calculate the offset
        mul struct_offset, structSize_r, rowCounter     // Multiplies the rowCounter by 8 to find the proper document in the struct array
        add struct_offset, struct_offset, structArr_s   // Adds the initial struct array offset to the internal offset to get the total offset from fp

        str maxWordIndex_r, [fp, struct_offset]         // Stores the highest word's index to the first entry of this row's struct
        add struct_offset, struct_offset, 4             // Increments the offset by 4 bytes to get the offset for frequency
        str maxFreq_r, [fp, struct_offset]              // Stores the highest word's frequency to the second entry of this row's struct

        add rowCounter, rowCounter, 1                   // Increments row counter by 1

outerLoopTest1:
        ldr rows, [fp, row_s]                           // Loads the rows from the stack
        cmp rowCounter, rows                            // Compares the rowCounter to the total number of rows
        b.lt outerLoop1                                 // Branches to the beginning of the outer loop if there are more rows to populate
        b next                                          // If there are no more rows to populate, branches to next

next:
        mov rowCounter, 0                               // Sets the rowCounter to zero for the next loop 
        ldr x0, =newline                                // Loads the new line string into x0 for printing
        bl printf                                       // Prints a new line to the console
        b looptest                                      // Branches to the next loop's test

loop:
        mov structSize_r, 8                             // Sets structSize_r to 8 in order to calculate the offset
        mul struct_offset, structSize_r, rowCounter     // Multiplies the rowCounter by 8 to find the proper document in the struct array
        add struct_offset, struct_offset, structArr_s   // Adds the initial struct array offset to the internal offset to get the total offset from fp

        ldr maxWordIndex, [fp, struct_offset]           // Loads the current document's highest word index
        add struct_offset, struct_offset, 4             // Increments the offset by 4 bytes to get the offset for frequency
        ldr maxFreq_r, [fp, struct_offset]              // Loads the current document's highest word's frequency

        mul Arr_offset, rowCounter, cols                // Increases the array offset according to which is the current document
        add A_offset, A_offset, docArr_s                // Increases the offset by 16 to account for the frame record
        add A_offset, A_offset, maxWordIndex            // Increases the offset according to the index of the highest word

        ldrb maxWord, [fp, Arr_offset]                  // Loads the current document's highest word from the stack

        ldr x0, =docInfoMsg                             // Loads the document info message into x0 for printing
        mov x1, rowCounter                              // Copies the current document number into x1
        mov w2, maxWordIndex                            // Copies the highest word's index into w2
        mov w3, maxWord                                 // Copies the occurrences of the highest word into w3
        mov w4, maxFreq_r                               // Copies the highest word's frequency into w4
        bl printf                                       // Prints the document information to the console

        add rowCounter, rowCounter, 1                   // Increments the rowCounter by 1

looptest:
        ldr rows, [fp, row_s]                           // Loads the rows from the stack
        cmp rowCounter, rows                            // Compares the rowCounter to the total number of rows
        b.lt loop                                       // Branches to the beginning of the loop if there are more rows

end:
        ldp fp, lr, [sp], dealloc       // Restores the state of the FP and LR registers, and deallocates 406 bytes in stack memory
        ret                             // Returns control to calling code, ends the program


// This program accepts an integer as input from the user, and after verifying that the integer is
// between 5 and 20 inclusive, generates that many integers randomly, where each integer is between 
// 0 and 9. Each integer represents the occurrences of a word within a document. These integers, which
// together make up the document, are printed to the console. Then the minimum and maximum frequencies of
// the smallest and largest integers within the document are both printed, as well as the sum of all the
// random integers generated, which is the document size. 

.data					// Starts .data segment
n: .word 0				// Sets label "n", has 32 bits

.text									// Starts .text segment
prompt: .string "Enter the number of integers to generate: "		// Defines the string for the prompt for input
scanfmt:        .string "%d"						// Sets label "scanfmt" used to accept user input
invalidInput:   .string "You must enter an integer between 5 and 20\n"	// Creates the error message string
currentNum:     .string "%d "						// Creates the string for printing the document contents
printDocSize:   .string "\n\nThe document size is: %d\n"		// Defines the string for printing the document size
minFrequency:   .string "The minimum frequency is: %d\n"		// Defines the string for printing the min frequency
maxFrequency:   .string "The maximum frequency is: %d\n\n"		// Defines the string for printing the max frequency
goodbye:        .string "Have a great day\n\n"				// Creates a string for printing an ending message

	define(numWords_r, x19)						// Defines a macro for register x19, which will be
									// used to store the number of integers to generate
	define(randNum_r, x20)						// Defines a macro for register x20, which will store
									// each random number as they are generated
	define(min_r, x21)						// Defines a macro for register x21, which will
									// store and update the lowest random number and 
									// compute the min frequency
	define(max_r, x22)						// Defines a macro for register x22, which will
									// store and update the highest random number and
									// compute the max frequency
	define(docSize_r, x23)						// Defines a macro for register x23, which will store
									// and update the document size

        .balign 4							// Aligns instructions properly
        .global main							// Makes the label "main" visible to the linker

main:					// Label "main"
        stp x29, x30, [sp, -16]!	// Saves the state of registers used by calling code, allocates 16 bytes in stack memory
        mov x29, sp			// Updates FP to the current SP

        ldr x0, =prompt			// Loads contents of "prompt" into register x0 for printing
        bl printf			// Calls the printf function

        ldr x0, =scanfmt		// Loads contents of "scanfmt" into register x0 for printing
        ldr x1, =n			// Loads contents of "n" into register x1 for scanning
        bl scanf			// Calls the scanf function

        ldr numWords_r, n		// Loads the value inputted by the user into register x19 (numWords_r)

        cmp numWords_r, 5               // Compares the input to 5
        b.lt invalid                    // Branches to "invalid" if the input is less than 5

        cmp numWords_r, 20              // Compares the input to 20
        b.gt invalid                    // Branches to "invalid" if the input is less than 5

        mov min_r, 10                   // Sets the min for future comparison
        mov max_r, 0                    // Sets the max for future comparison
        mov docSize_r, 0                // Sets the document size register to be 0 at first

	mov x24, 100			// Puts value 100 into register x24 for later frequency calculations

        mov x0, 0			// Resets register x0 to 0 for seeding purposes
        bl time				// Calls time function for seeding purposes 
        bl srand			// Seeds the rand function
        b looptest			// Branches to the loop's test, which is located after the loop

loop:					// Label "loop"
        sub numWords_r, numWords_r, 1	// Decrements the number of integers left to produce by 1

        bl rand				// Calls the rand function to generate an integer
        mov randNum_r, x0		// Puts the output of the rand function into the register that
					// stores each generated integer
        mov x10, 10			// Sets register x10 to 10 for future use in restricting the
					// random number to be between 0 and 9
        sdiv x11, x0, x10		// Divides the original integer by 10 and stores the value
					// (without the remainder) in register x11
        mul randNum_r, x11, x10		// Multiplies the value in x11 by 10
        sub randNum_r, x0, randNum_r	// Subtracts the original value by the current value of register
					// x20 to get the value of the remainder, which will be the rightmost
					// digit of the original integer

        add docSize_r, docSize_r, randNum_r	// Updates the document size by adding the new integer

        ldr x0, =currentNum		// Loads the string for printing the integer
        mov x1, randNum_r		// Copies the current random integer into register x1 for printing
        bl printf			// Prints the current random integer to the console

minCmp:					// Label "minCmp"
        cmp randNum_r, min_r		// Compares the current random integer with the minimum value so far
        b.ge maxCmp			// Branches to the next section if the current integer is not less
					// than the current minimum value
        mov min_r, randNum_r		// If the current value is less than the minimum value, updates the
					// minimum value

maxCmp:					// Label "maxCmp"
        cmp randNum_r, max_r		// Compares the current random integer with the maximum value so far
        b.le next			// Branches to the next section if the current integer is not greater
					// than the current maximum value
        mov max_r, randNum_r		// If the cuurrent value is greater than the maximum, updates the
					// maximum value

next:					// Label "next"
        b looptest			// End of the loop - branches to the loop test to repeat

looptest:                               // Label "looptest"
	mov x25, 0			// Puts 0 into register x25 for comparison puproses later
        cmp x25, numWords_r             // Compares 0, the value of x25, with the number of integers left to generate
        b.lt loop                       // Branches to the loop if there are still integers left to generate
        b printResults                  // Branches to the printing stage of the program if
                                        // there are no more integers left to generate

printResults:				// Label "printResults"
        mul min_r, min_r, x24           // Multiplies the minimum value by 100
        udiv min_r, min_r, docSize_r	// Divides the new "minimum" by the document size to get the 
					// minimum frequency

        mul max_r, max_r, x24           // Multiplies the maximum value by 100
        udiv max_r, max_r, docSize_r	// Divides the new "maximum" by the document size to get the
					// maximum frequency

        ldr x0, =printDocSize		// Loads the string for the document size into x0 for printing
        mov x1, docSize_r		// Copies the value of the document size into x1 for printing
        bl printf			// Prints the document size information to the console

        ldr x0, =minFrequency		// Loads the string for the min frequency into x0 for printing
        mov x1, min_r			// Copies the value of the min frequency into x1 for printing
        bl printf			// Prints the min frequency to the console

        ldr x0, =maxFrequency		// Loads the string for the max frequency into x0 for printing
        mov x1, max_r			// Copies the value of the max frequency into x1 for printing
        bl printf			// Prints the max frequency to the console

        ldr x0, =goodbye		// Loads the ending message to x0 for printing
        bl printf			// Prints the ending message to the console
        b done				// Branches to done instead of continuing to "invalid"

invalid:				// Label "invalid"
        ldr x0, =invalidInput		// Loads the invalid input message to x0 for printing
        bl printf			// Prints the invalid input message to the console

done:					// Label "done"
        ldp x29, x30, [sp], 16		// Restores the state of the FP and LR registers, and deallocates 16 bytes in stack memory
        ret				// Returns control to calling code, ends the program


// This program performs 31 multiplications, on two integers each time. The multiplier begins at -15
// and is incremented until +15, each time being multiplied by a random number between 0 and 15. The
// algorithm implements a type of bitwise long multiplication, in which each bit of the multiplicand
// is multiplied with the multiplier, and the result is shifted left according to the significance 
// of the bit. Each partial result is added up to get the final product, which is then printed
// to the console.

.text                                           // Starts .text segment
message: .string "%d * %d = %d\n"               // Defines the string for the output message

        define(multiplier, x19)                 // Defines a macro for the register x19, which will be used to store the
                                                // multipliers, from -15 to 15
        define(multiplicand, x20)               // Defines a macro for register x20, which will be used to store the
                                                // randomly generated multiplicands
        define(temp_multiplicand, x21)          // Defines a macro for register x21, which will be used to copy and manipulate
                                                // the values of the multiplicands without changing the original number
        define(temp_multiplier, x22)            // Defines a macro for register x22, which will be used to copy and manipulate
                                                // the values of the multipliers without changing the original number
        define(sum, x23)                        // Defines a macro for register x23, which will be used as a running sum to
                                                // add up the partial results of the product
        define(i, x24)                          // Defines a macro for register x24, which will be used as a counter for the
                                                // inner loop

        .balign 4                               // Aligns instructions properly
        .global main                            // Makes the label "main" visible to the linker


main:                                                   // Label "main"
        stp x29, x30, [sp, -16]!                        // Saves the state of registers used by calling code, allocates 16 bytes in stack memory
        mov x29, sp                                     // Updates FP to the current SP

        mov multiplier, -15                             // Moves the starting value of -15 into the multiplier register
        mov x0, 0                                       // Resets register x0 to 0 for seeding purposes
        bl time                                         // Calls the time function for seeding purposes
        bl srand                                        // Seeds the rand function

firstLoop:                                              // Label "firstLoop" denotes the outer loop
        bl rand                                         // Calls the rand function to generate a random integer
        mov multiplicand, x0                            // Puts the output of the rand function into the multiplicand register
        and multiplicand, multiplicand, 15              // Performs a bitwise AND on the random number and 15, so that the random 
                                                        // number is restricted to a range of 0-15
        mov i, 0                                        // Puts the starting value of 0 into the register i

secondLoop:                                             // Label "secondLoop" denotes the inner loop
        mov temp_multiplicand, multiplicand             // Copies the multiplicand, which is between -15 and 15, to temp_multiplicand
        lsr temp_multiplicand, temp_multiplicand, i     // Logically shifts temp_multiplicand right until the ith bit is the least significant
        and temp_multiplicand, temp_multiplicand, 1     // Performs a bitwise AND on temp_multiplicand, which zeroes out all bits but the first

        cmp temp_multiplicand, 1                        // Compares the ith bit of the original multiplicand with the immediate value 1
        b.eq bitIsOne                                   // Branches to bitIsOne if the ith bit of the original multiplicand is 1
        b bitIsZero                                     // Otherwise, the bit must be 0, so it branches to bitIsZero

bitIsZero:                                              // Label "bitIsZero"
        add i, i, 1                                     // Increments i by one
        cmp i, 64                                       // Checks the updated value of i against the immediate value 64
        b.lt secondLoop                                 // If i is still less than 64, branches to the secondLoop again, since
                                                        // nothing more needs to be done when the ith bit is 0
        b printResult                                   // Otherwise, branches to printResult

bitIsOne:                                               // Label "bitIsOne"
        mov temp_multiplier, multiplier                 // Copies the value of multiplier into the register temp_multiplier, since the ith
                                                        // bit is 1, and 1 times the multiplier is still the original multiplier
        lsl temp_multiplier, temp_multiplier, i         // Shifts temp_multiplier left by i bits
        add sum, sum, temp_multiplier                   // Updates the running sum with the partial result of the ith bit

        add i, i, 1                                     // Increments i by one
        cmp i, 64                                       // Compares the updated value of i to 64
        b.lt secondLoop                                 // branches to the secondLoop again if i is less than 64
        b printResult                                   // Otherwise, branches to printResult

printResult:                                            // Label "printReult"
        ldr x0, =message                                // Loads contents of "message" into register x0 for printing
        mov x1, multiplier                              // Puts the value of the current multiplier into register x1 for printing
        mov x2, multiplicand                            // Puts the value of the current multiplicand into register x2 for printing
        mov x3, sum                                     // Puts the value of the final sum (product) into regiister x3 for printing
        bl printf                                       // Calls the printf function, prints to the console
        mov sum, 0                                      // Zeroes the sum register for the next loop's calculations
        add multiplier, multiplier,  1                  // Increments the multiplier by 1
        cmp multiplier, 16                              // Compares the updated value of the multiplier to 16
        b.lt firstLoop                                  // While the multiplier is less than 16, branches back to the beginning of firstLoop

        ldp x29, x30, [sp], 16                          // Restores the state of the FP and LR registers, and deallocates 16 bytes in stack memory  
        ret                                             // Returns control to calling code, ends the program 


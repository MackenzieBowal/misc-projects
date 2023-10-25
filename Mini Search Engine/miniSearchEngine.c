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
 * the user is printed to the console and all input and output information 
 * is written to a log file. 
 * The user can repeatedly search the original 2-dimensional array until 
 * they wish to exit the program.
 * 
 * 
Compiling and running the program:

Use the following command to compile the program:
>>gcc assign1.c -o <outputFileName>

To run the program use the following command:
>>./<outputFileName> <numberOfRows> <numberOfColumns> <optionalFile>

and follow the prompts.
 */

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>
#include<ctype.h>
#include <time.h>


//creates global variables of the number of rows and columns
int rows;
int cols;


/**
 * randomNum
 * Generates and returns a random integer between two given integers
 * Parameters:
 * 	int m is the minimum (inclusive) value that can be returned by the random number generator
 *  int n is the maximum (inclusive) value that can be returned
 */
int randomNum(int m, int n) {
		
	int num = rand()%(n+1);
	if (num >= m) {
		return num;
	} else {
		return -1;
	}
}


/**
 * initialize
 * Populates a given 2-dimensional array, either by reading from a file specified by the user
 * or randomly. Also sets the seed for the rand() function in initialize(), which is called if
 * the table is populated randomly.
 * Parameters:
 * 	int table[rows][cols] is the 2-dimensional array, which is populated randomly or using the file
 * 	bool useFile states whether or not a file was given in the command line arguments
 * 	char fileName[] is the name of the file if one was given, not used to populate randomly
 */
void initialize(int table[rows][cols], bool useFile, char fileName[]) {
	
	srand(time(0));

	//copies from the file if one was provided
	if (useFile) {
		
		FILE *readFile;
		readFile = fopen(fileName, "r");
		int rowCounter = 0;
		int colCounter = 0;
		char ch;
		fscanf(readFile, "%c", &ch);
		
			while (rowCounter < rows) {
				while (colCounter < cols) {
	
					if (ch != ' ' && ch != '\n') {
						table[rowCounter][colCounter] = (int)ch - '0';
						colCounter++;
					} else if (ch == '\n') {
						break;
					}
					fscanf(readFile, "%c", &ch);
				}
				colCounter = 0;
				fscanf(readFile, "%c", &ch);
				rowCounter++;
			}
		fclose(readFile);
		
		

	//if no file was provided, populates randomly
	} else {
		int i=0, j=0;
		for (i=0; i<=rows; i++) {
			for (j=0; j<=cols; j++) {
				int val = randomNum(0,9);
				table[i][j] = val;
			}
		}
		
	}
	
}

/**
 * logToFile
 * Appends the input/output information from the latest search to a file named "assign1.log". 
 * Prints the number of the search, the word index, number of documents, and resulting top 
 * documents of the search. If this is the first time the user has searched since starting
 * the program, the rows, columns, and document table are printed at the beginning.
 * Parameters:
 * 	int *numDocs is a pointer to the number of top documents the user specified in this search
 * 	int *wordIndex is a pointer to the index of the word the user specified in this search
 * 	int timesSearched is a nonnegative integer describing how many times the user has searched while
 *  running the program, including the current search
 * 	int docNums[*numDocs] is an array containing the indices of the top documents of the original table
 * 	int table[rows][cols] is the original table
 */
void logToFile(int *numDocs, int *wordIndex, int timesSearched, int docNums[*numDocs], int table[rows][cols]) {
	
	//Opens file in append mode
	FILE *logFile;
	logFile = fopen("assign1.log", "a");
	
	//Prints extra information if this is the first search
	if (timesSearched == 1) {
		fprintf(logFile, "The number of rows specified by the user: %d\n", rows);
		fprintf(logFile, "The number of columns specified by the user: %d\n\n", cols);
		int i,j;
		
		fprintf(logFile, "These are the documents:\n\n");
		
		for (i=0; i<rows; i++) {
			for (j=0; j<cols; j++) {
				fprintf(logFile, "%d ",table[i][j]);
			}
			fprintf(logFile, "\n");
		}
		
		fprintf(logFile, "\n");
	}
	
	//Prints current search-specific information about user input
	fprintf(logFile, "The number of times the user has searched is %d\n", timesSearched);
	fprintf(logFile, "The word index specified by the user: %d\n", *wordIndex);
	fprintf(logFile, "The number of documents specified by the user: %d\n\n", *numDocs);
	
	//Prints the resulting top documents of the search
	fprintf(logFile, "The top %d documents are:\n", *numDocs);
	for (int q=0; q < *numDocs; q++) {
		fprintf(logFile, "#%d: Document %d\n", q+1, docNums[q]);
	}	
	
	fprintf(logFile, "\n\n\n");
	
	fclose(logFile);
	
	
}


/**
 * topRelevantDocs
 * Determines the order of the documents according to decreasing frequency of a given word's index. Prints the 
 * resulting top documents to the console, where the number of documents printed is determined by the user. Passes 
 * information to the logToFile() function to write the result to a file.
 * Parameters:
 * 	int table[rows][cols] is the original table
 * 	int *wordIndex is a pointer to the index of the word specified by the user in this search
 * 	int *numDocs is a pointer to the number top documents specified by the user in this search
 * 	int timesSearched is a nonnegative integer describing how many times the user has searched while
 *  running the program, including the current search
 */
void topRelevantDocs(int table[rows][cols], int *wordIndex, int *numDocs, int timesSearched) {
		
	//Makes a new array which will hold frequency and index information for each document, to be sorted
	double sortingArray[rows][2];
	
	//Makes an array which will hold the indices of the documents, in order
	int docNums[*numDocs];
	
	//Calculates the word frequency for each document and use it to populate sortingArray
	int i, j;
	int docSize = 0;
	int occurrences = 0;
	double frequency;
	
	for (i=0; i < rows; i++) {
		for (j=0; j < cols; j++) {
			if (j == *wordIndex) {
				occurrences = table[i][j];
			}
			docSize += table[i][j];
		}
		
		frequency = ((double)occurrences)/((double)docSize);
		
		sortingArray[i][0] = frequency;
		sortingArray[i][1] = i;

		
		frequency = 0.0;
		docSize = 0;
		occurrences = 0;
	}
	

	//Uses bubble sort to arrange sortingArray in order of increasing frequency
	int swap;
	int p;
	
	do {
		swap = 0;
		for (int p=0; p < rows-1; p++) {
			
			//Swaps the current and next documents if they are out of order
			if (sortingArray[p][0] < sortingArray[p+1][0]) {
				swap += 1;
				double temp[2];
				temp[0] = sortingArray[p][0];
				temp[1] = sortingArray[p][1];
				
				sortingArray[p][0] = sortingArray[p+1][0];
				sortingArray[p][1] = sortingArray[p+1][1];
				
				sortingArray[p+1][0] = temp[0];
				sortingArray[p+1][1] = temp[1];
				
			}
			
		}
		p = 0;
	} while (swap != 0);
	
	//Populates docNums with the indices of the original documents, in order of decreasing frequency
	for (int q=0; q<*numDocs; q++) {
		docNums[q] = (int)sortingArray[q][1];
	}
	
	//Prints the top documents to the console, according to the number specified by the user
	printf("The top %d documents are:\n", *numDocs);
	for (int q=0; q < *numDocs; q++) {
		printf("#%d: Document %d\n", q+1, docNums[q]);
	}
	printf("\n");
	

	
	logToFile(numDocs, wordIndex, timesSearched, docNums, table);
	
}



/**
 * display
 * Prints the contents of the original table to the console
 * Parameter:
 * 	int table[rows][cols] is the original table
 */
void display(int table[rows][cols]) {
	
	int i,j;
	
	printf("\nThese are the documents:\n\n");
	
	for (i=0; i<rows; i++) {
		for (j=0; j<cols; j++) {
			printf("%d ",table[i][j]);
		}
		printf("\n");
	}
	
	printf("\n");
	
}




//main function
/**
 * main
 * Executes the program by calling other functions. First, checks and handles the command line arguments,
 * then creates, populates, and displays the table. 
 * Parameters:
 * 	int argc is a count of the command line arguments entered by the user. It should
 *  be either 3 (no file) or 4 (file)
 *  char* argv[] contains the command line arguments. The first element is expected to be the name
 *  of the program, the second and third is expected to be integers corresponding to rows and columns,
 *  and the fourth (optional) is expected to be a file name
 */

void main(int argc, char* argv[]) {
	bool useFile = false;
	
	//Checks that the file exists, and prints a message and exits if it does not
	if (argc == 4) {
		if( access( argv[3], F_OK ) != -1 ) {
			useFile = true;
		} else {
			printf("The file you entered does not exist.");
			exit(0);
		}
	//Checks that there are a valid number of command line arguments
	} else if (argc < 3 || argc > 4) {
		printf("Please enter an appropriate number of arguments.");
		exit(0);
	}
	
	//assigns the given command line values to rows and cols
	rows = atoi(argv[1]);
	cols = atoi(argv[2]);
	
	//If the command line arguments were invalid, prints a message and exits the program
	if (rows < 4 || rows > 21 || cols < 4 || cols > 21) {
		printf("Something is wrong with the command line arguments. Please try again.\n");
		exit(0);
	}
	


	//Creates, populates, and displays the table array
	int table[rows][cols];
	
	initialize(table, useFile, argv[3]);
		
	display(table);
	
	
	//Prepares for validation of user input and initialize variables needed
	char wordIndexValidation[2];
	wordIndexValidation[0] = '0';
	wordIndexValidation[1] = '0';
	int wordIndex;
	
	char numDocsValidation[2];
	numDocsValidation[0] = '0';
	numDocsValidation[1] = '0';
	int numDocs;
	
	char cont;
	
	int timesSearched = 0;
	
	
	//Performs the search algorithm, and loops as long as the user wishes to continue
	do {
		
		timesSearched += 1;
		
		//Prompts user for word index and validate
		printf("Enter the index of the word you are searching for: ");
		scanf(" %s", &wordIndexValidation);
		printf("\n");

		if (!isdigit(wordIndexValidation[0])) {
			printf("The index must be a nonnegative integer that is less than the number of columns. Please try again.\n\n");
			exit(0);
		}
		
		wordIndex = atoi(wordIndexValidation);
		
		if (wordIndex < 0 || wordIndex > cols-1) {
			printf("The index must be a nonnegative integer that is less than the number of columns. Please try again.\n\n");
			exit(0);
		}
		
		//Prompts user for number of top documents information and validate
		printf("How many top documents do you want to retrieve? ");
		scanf(" %s", &numDocsValidation);
		printf("\n");
		
		if (!isdigit(numDocsValidation[0])) {
			printf("The number of documents must be an integer between 0 and the number of documents. Please try again.\n\n");
			exit(0);
		}
		
		numDocs = atoi(numDocsValidation);

		if (numDocs < 0 || numDocs > rows) {
			printf("The number of documents must be an integer between 0 and the number of documents. Please try again.\n\n");
			exit(0);
		}
		
		//Finds and prints top documents, and logs input/output information to the log file
		topRelevantDocs(table, &wordIndex, &numDocs, timesSearched);
		
		//Prompts the user to search again or exit the program
		printf("Would you like to perform another search? (y/n) ");
		scanf(" %c", &cont);
		printf("\n");
		while (cont != 'n' && cont != 'y') {
			printf("Please enter \"y\" to continue searching or \"n\" to exit the program: ");
			scanf(" %c", &cont);
			printf("\n");
		}
			
	} while (cont == 'y');
		
	printf("Have a great day!\n\n");

	exit(0);
		
}

/**
 * This program simulates a horse race. A main thread is created, which takes 
 * two integers as input from the user during runtime. The first, n, is the number
 * of horses in the race, and the second is the finish line. The main thread then 
 * initializes a shared global struct, assigning default values to several variables.
 * Then the main thread creates the horse threads (as specified by the user) and assigns
 * them unique integer IDs increasing from 0 to n-1. As the horse threads race, the main
 * thread loops through displaying the race, assigning ranks to horses as they finish
 * the race, and checking if all the horse threads are done. Once every horse has reached
 * the finish line, the main thread joins back with each horse thread and displays the 
 * final results, then exits itself.
 * Each horse thread loops through sleeping a random number of seconds (restricted between 0
 * and 7 seconds for brevity) then taking one step. Once the horse has taken enough steps
 * to reach the finish line, the horse thread records the time taken and exits.
 */ 

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>
#include<ctype.h>
#include<time.h>
#include<pthread.h>

/**
 * Definition for the shared struct, which is accessed by the main thread
 * and each horse thread. 
 * Variables:
 * 	int progress[] tracks the number of steps each horse thread has
 * 		taken at a given point in the race.
 * 	int rank[] records the rank (between 1 and n) that each horse thread
 * 		has achieved when they finish the race.
 * 	bool raceFinished is true only when every horse has reached the finish line.
 * 	time_t finishTime[] records each horse's time taken for the race.
 * 	int finishLine is assigned a user-inputted value, which is the number of
 * 		steps each horse has to take to finish the race.
 */

struct shared {
	int progress[100];
	int rank[100];
	bool raceFinished;
	time_t finishTime[100];
	int finishLine;
};

// Declaration of the global shared struct
struct shared s;

/**
 * findMaxRank()
 * This function searches through the rank array in the shared struct to find the latest
 * rank a horse has been assigned. 
 * Parameter:
 * 	int n is the number of horses in the race, specified by the user.
 * Returns:
 * 	int maxRank is the highest number that any of the finished horses have yet been assigned.
 */

int findMaxRank(int n) {
	
	int maxRank = 0;
	for (int j=0; j < n; j++) {
		if (s.rank[j] > maxRank) {
			maxRank = s.rank[j];
		}
	}
	return maxRank;
}

/**
 * rankFinishedHorses()
 * This function creates a new array consisting solely of the horses (ordered 
 * by increasing ID) that have finished the race but not yet been assigned a rank.
 * This array is then sorted in order of increasing time, with ties broken in favour
 * of horses with lower ID numbers. According to the max rank that has been previously
 * assigned, the finished-but-unranked horses are given ranks.
 * Parameter:
 * 	int n is the number of horses in the race, specified by the user.
 * No return value.
 */

void rankFinishedHorses(int n) {
	
	// Creates new array of finished horses that have not been ranked
	int numJustFinished = 0;
	int justFinished[n];
	for (int k=0; k < n; k++) {
		if (s.progress[k] >= s.finishLine && s.rank[k] == 0) {
			justFinished[numJustFinished] = k;
			numJustFinished++;
		}
	}

	// Sorts just-finished horses with bubble sort
	int swap;
	int l;
	do {
		swap = 0;
		for (int l=0; l < numJustFinished-1; l++) {
			
			//Swaps the current and next horses if they are out of order
			if (s.finishTime[justFinished[l]] > s.finishTime[justFinished[l+1]]) {
				swap += 1;
				int temp;
				temp = justFinished[l];
				justFinished[l] = justFinished[l+1];
				justFinished[l+1] = temp;
			}
		}
		l = 0;
	} while (swap != 0);
	
	// Assigns ranks to the horses
	int maxRank = findMaxRank(n) + 1;
	for (int m=0; m < numJustFinished; m++) {
		s.rank[justFinished[m]] = maxRank;
		maxRank++;
	}
}

/**
 * horseThreadFunc()
 * Performs the functionality of the horse threads. First, each thread accepts 
 * its ID and initializes its start time before entering the race loop. In the loop,
 * the horse thread sleeps for a random number of seconds (restricted to a max of 7) 
 * then takes one step by incrementing its progress variable. Once its progress
 * reaches the finish line, the loop ends and the ending time is recorded. The difference
 * between the start time and ending time is calculated and recorded in the finishTime 
 * array. Then the thread exits.
 * Parameter:
 * 	void *idParam is the unique ID for the horse thread, cast to an integer at
 * 		the beginning of the function.
 * No return value.
 */

void *horseThreadFunc(void *idParam){
	
	int id = * (int *) idParam;
	time_t start = time(0);
	
	// Race loop
	for (int a=0; a < s.finishLine; a++) {
		int numSeconds = rand() % 7;
		sleep(numSeconds);
		s.progress[id]++;
		if (s.progress[id]>=s.finishLine) {
			break;
		}
	}
	
	// Record time taken
    time_t end = time(0);
	s.finishTime[id] = end - start;
	pthread_exit(0);
}

/**
 * displayProgress()
 * This function prints the current state of the race to the console. Each 
 * horse is represented by several dashes "-" corresponding to their current
 * progress in the race, followed by a ">" if they are not finished and a "*"
 * if they are. The console is cleared every time to give the illusion of animation.
 * Parameter:
 * 	int n is the number of horse threads, specified by the user.
 * No return value.
 */

void displayProgress(int n) {
	
	system("clear");
	for (int b=0; b < n; b++) {
		printf("Horse %d:\t", b);
		for (int c=0; c < s.progress[b]; c++) {
			printf("-");
		}
		if (s.progress[b] == s.finishLine) {
			printf("*");
		} else {
			printf(">");
		}
		printf("\n");
	}
}

/**
 * displayResults()
 * This function prints to the console the ranking of the horses, from 1 to n.
 * Parameter:
 * 	int n is the number of horses in the race, specified by the user.
 * No return value.
 */

void displayResults(int n) {
	int rankNum;
	printf("\nWINNERS\n________\n\n");
	
	for (int q=0; q<n; q++) {
		sleep(1);
		// Find the IDs of the horses by increasing rank
		for (int r=0; r<n; r++) {
			if (s.rank[r] == q+1) {
				rankNum = r;
				break;
			}
		}
		// Print out the result
		printf("#%d: Horse %d\n", q+1, rankNum);
	}
	sleep(1);
}

/**
 * mainThreadFunc()
 * Performs the central functionality of the program. First, it prompts the user for
 * inputs n (the number of horses) and fLine (the finish line). Then it initializes 
 * the variables and arrays of the shared struct to their beginning values, and 
 * creates n horse threads with distinct IDs. The main thread then begins a loop in
 * which it displays the current state of the race, updates the ranks of any recently
 * finished horses, and checks whether the race is done. Afterwards it displays the final
 * progress of the race, joins with the now-finished horse threads, and announces the
 * winners before exiting.
 * No parameters or return value.
 */

void *mainThreadFunc(){
	
	// Get n and finishLine
	int n;
	printf("Enter the number of horses: ");
	scanf("%d", &n);
	while (n < 0 || n > 100) {
		printf("That was not a valid number of horses. Please try again: ");
		scanf("%d", &n);
		printf("\n");
	}

	// Get finish line from user
	int fLine;
	printf("Please enter the finish line (integer): ");
	scanf("%d", &fLine);
	printf("\n");
	while (fLine < 0) {
		printf("That was not a valid finish line. Please try again: ");
		scanf("%d", &fLine);
		printf("\n");
	}
	
	// Initialize struct
	s.finishLine = fLine;
	s.raceFinished = false;

	for (int d=0; d<n; d++) {
		s.progress[d] = 0;
		s.rank[d] = 0;
		s.finishTime[d] = -1;
	}
	
	// Create the horse threads
	pthread_t tid[n];
	pthread_attr_t attrs[n];
	int idNums[n];
	
	for (int f=0; f < n; f++) {
		idNums[f] = f;
		pthread_attr_init(&attrs[f]);
		pthread_create(&tid[f], &attrs[f], horseThreadFunc, &idNums[f]);
	}
	
	displayProgress(n);
	
	// Loop during the race
	while(!s.raceFinished) {
		
		sleep(1);
		displayProgress(n);
		
		rankFinishedHorses(n);
		
		s.raceFinished = true;
		for (int g=0; g < n; g++) {
			if (s.progress[g] < s.finishLine) {
				s.raceFinished = false;
				break;
			}
		}
	}
	displayProgress(n);
	printf("\n");
	
	// Wait and join back with the horse threads
	for (int h=0; h < n; h++) {
		pthread_join(tid[h], NULL);
	}

	// Display results/leaderboard
	displayResults(n);
	
	pthread_exit(0);
}

/**
 * main()
 * First seeds rand() for future purposes, then creates the main thread and waits for
 * it to join before finishing the program.
 * No parameters or return value.
 */

void main() {
	srand(time(0));
	
	pthread_t maintid;
	pthread_attr_t mainAttr;
	pthread_attr_init(&mainAttr);
	pthread_create(&maintid, &mainAttr, mainThreadFunc, NULL);
	pthread_join(maintid, NULL);
}

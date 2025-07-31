#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void determine_floor(char *file_name) {
  long counter = 0;
  FILE *filepointer;
  filepointer = fopen(file_name, "r");

  if (!filepointer) {
    perror("open");
    exit(EXIT_FAILURE);
  }

  int current = fgetc(filepointer);
  while (current != EOF) {
    if (current == '(') {
      counter++;
    } else if (current == ')') {
      counter--;
    }
    current = fgetc(filepointer);
  }

  printf("Floor: %ld\n", counter);
}

int main(int argc, char *argv[]) {
  clock_t start_time, end_time;
  double elapsed_seconds;

  start_time = clock();
  determine_floor(argv[1]);
  end_time = clock();

  elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);

  return EXIT_SUCCESS;
}

// 232 is the right answer for part 1

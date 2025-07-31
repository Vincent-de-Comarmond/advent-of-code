#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void determine_basement_chars(char *file_name) {
  long current_floor = 0;
  FILE *filepointer;
  filepointer = fopen(file_name, "r");

  if (!filepointer) {
    perror("open");
    exit(EXIT_FAILURE);
  }

  int current_char = fgetc(filepointer);
  int character_no = 1;

  while (current_char != EOF) {
    if (current_char == '(') {
      current_floor++;
    } else if (current_char == ')') {
      current_floor--;
    }

    if (current_floor == -1) {
      break;
    }

    current_char = fgetc(filepointer);
    character_no++;
  }

  printf("Instructions needed: %d\n", character_no);
}

int main(int argc, char *argv[]) {
  clock_t start_time, end_time;
  double elapsed_seconds;

  start_time = clock();
  determine_basement_chars(argv[1]);
  end_time = clock();

  elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);

  return EXIT_SUCCESS;
}

// 1783 is the right answer for part 2

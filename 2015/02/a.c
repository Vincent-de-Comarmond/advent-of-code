#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

long ribbon_for_present(char *input_line) {
  int idx;
  long sides[3];
  long areas[4];
  areas[3] = LONG_MAX;

  sscanf(strtok(input_line, "x"), "%ld", &sides[0]);
  sscanf(strtok(NULL, "x"), "%ld", &sides[1]);
  sscanf(strtok(NULL, "x"), "%ld", &sides[2]);

  areas[0] = sides[0] * sides[1];
  areas[1] = sides[0] * sides[2];
  areas[2] = sides[1] * sides[2];

  for (idx = 0; idx < 3; idx++) {
    areas[3] = areas[idx] < areas[3] ? areas[idx] : areas[3];
  }

  return 2 * areas[0] + 2 * areas[1] + 2 * areas[2] + areas[3];
}

void wrapping_paper_needed(char *filename) {

  FILE *file = fopen(filename, "r");
  char line[20];
  char *token;
  long wrapping_needed = 0;

  if (file != NULL) {
    while (fgets(line, sizeof(line), file)) {
      if (strlen(line) > 2) { // Cheap way of skipping empty line
        long box_wrapping = ribbon_for_present(line);
        wrapping_needed += box_wrapping;
      }
    }
    fclose(file);
  } else {
    fprintf(stderr, "Unable to open file!\n");
    exit(EXIT_FAILURE);
  }

  printf("Wrapping paper needed: %ld\n", wrapping_needed);
}

int main(int argc, char *argv[]) {
  clock_t start_time, end_time;
  double elapsed_seconds;

  start_time = clock();
  wrapping_paper_needed(argv[1]);
  end_time = clock();

  elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
};

// 3804396 is too high for day 2 part 1
// 101660 is too low for day 2 part 1
// 1607331 is too high

// 1606483 is the right answer for part 1

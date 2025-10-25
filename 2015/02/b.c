#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

long ribbon_for_present(char *input_line) {
  long sides[3];
  long volume, smallest_perimeter;

  sscanf(strtok(input_line, "x"), "%ld", &sides[0]);
  sscanf(strtok(NULL, "x"), "%ld", &sides[1]);
  sscanf(strtok(NULL, "x"), "%ld", &sides[2]);

  volume = sides[0] * sides[1] * sides[2];

  if (sides[0] < sides[1] | sides[0] < sides[2]) {
    if (sides[1] < sides[2]) {
      smallest_perimeter = 2 * sides[0] + 2 * sides[1];
    } else {
      smallest_perimeter = 2 * sides[0] + 2 * sides[2];
    }
  } else {
    smallest_perimeter = 2 * sides[1] + 2 * sides[2];
  }

  return volume + smallest_perimeter;
}

void wrapping_paper_needed(char *filename) {

  FILE *file = fopen(filename, "r");
  char line[20];
  long total_ribbon_needed = 0;

  if (file != NULL) {
    while (fgets(line, sizeof(line), file)) {
      if (strlen(line) > 2) { // Cheap way of skipping empty line
        long ribbon = ribbon_for_present(line);
        total_ribbon_needed += ribbon;
      }
    }
    fclose(file);
  } else {
    fprintf(stderr, "Unable to open file!\n");
    exit(EXIT_FAILURE);
  }

  printf("Ribbon needed: %ld\n", total_ribbon_needed);
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

// 3842356 is the right answer for part 2

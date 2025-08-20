#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int determine_niceness(char *input_line) {
  int i, j;
  bool has_spaced_repeat = false, has_repeat_double = false;

  for (i = 1; i < strlen(input_line); i++) {

    // Check for skipped repeat
    if (!has_spaced_repeat && 2 <= i) {
      if (input_line[i - 2] == input_line[i]) {
        has_spaced_repeat = true;
      }
    }

    // Check for reapeated double
    if (!has_repeat_double) {
      for (j = 1; j < i - 1; j += 1) {
        if (input_line[j - 1] == input_line[i - 1] &&
            input_line[j] == input_line[i]) {
          has_repeat_double = true;
        }
      }
    }
    if (has_spaced_repeat && has_repeat_double) {
      return 1;
    }
  }
  return 0;
}

void count_nice_strings(char *filename) {
  int buf_size = 200, nice_strings = 0;
  FILE *file = fopen(filename, "r");
  char line[buf_size];

  while (fgets(line, buf_size, file)) {
    line[strcspn(line, "\r\n")] = 0;
    nice_strings += determine_niceness(line);
  }

  fclose(file);
  printf("Number Nice Strings: %d\n", nice_strings);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  count_nice_strings(argv[1]);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 53 is the right answer for part 2

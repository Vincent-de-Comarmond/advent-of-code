#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int determine_niceness(char *input_line, int buffer_length) {
  int i = 0, j = 0, vowel_count = 0;
  bool has_double = false;
  char a, b;
  char vowels[] = {'a', 'e', 'i', 'o', 'u'};

  for (i = 1; i < buffer_length; i++) {
    a = input_line[i - 1], b = input_line[i];

    if (i == 1) {
      for (j = 0; j < 5; j++) {
        if (a == vowels[j]) {
          vowel_count++;
          break;
        }
      }
    }
    for (j = 0; j < 5; j++) {
      if (b == vowels[j]) {
        vowel_count++;
        break;
      }
    }

    if (a == b) {
      has_double = true;
    }

    if (((a == 'a') && (b == 'b')) || ((a == 'c') && (b == 'd')) ||
        ((a == 'p') && (b == 'q')) || ((a == 'x') && (b == 'y'))) {
      return 0;
    }
  }

  if ((vowel_count >= 3) && has_double) {
    return 1;
  }
  return 0;
}

void count_nice_strings(char *filename) {
  int buf_size = 200, nice_strings = 0;
  FILE *file = fopen(filename, "r");
  char line[buf_size];

  while (fgets(line, buf_size, file)) {
    line[strcspn(line, "\r\n")] = 0;
    nice_strings += determine_niceness(line, strlen(line));
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

// 217 is too low for part 1
// 258 is the right answer for part 1

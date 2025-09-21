#include <stdio.h>
#include <stdlib.h>
#include <time.h>

long sum(char *filename) {
  int char_val = 0, idx = 0;
  char buffer[20] = {[0 ... 19] = '\0'};
  long total = 0;

  FILE *file = fopen(filename, "r");
  if (file != NULL) {
    while (char_val != EOF) {
      char_val = fgetc(file);
      while (('0' <= char_val && char_val <= '9') || char_val == '-') {
        buffer[idx++] = char_val;
        char_val = fgetc(file);
      }
      if (0 < idx) {
        total += atoi(buffer);
      }
      while (idx > 0) {
        buffer[--idx] = '\0';
      }
    }
  }

  fclose(file);
  return total;
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  long total = sum(argv[1]);
  printf("Total is: %ld\n", total);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n\n\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 214938 is too high for part 1
// 191164 is the right answer for part 1
// Execution time: 0.000400 seconds

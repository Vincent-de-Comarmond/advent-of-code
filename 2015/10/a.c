#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void solve(char input_string[5000000], char output_string[5000000], int calls) {
  char current = '\0', previous = '\0';
  int i = 0, current_num = 0, idx = 0;

  int stop = strlen(input_string);
  for (i = 0; i < stop; i++) {
    if (i == 0) {
      current = input_string[0], previous = input_string[0];
      current_num++;
      continue;
    }
    current = input_string[i];
    if (current == previous) {
      current_num++;
    } else {
      output_string[idx++] = current_num + '0';
      output_string[idx++] = previous;

      current = input_string[i], previous = input_string[i];
      current_num = 1;
    }
  }

  output_string[idx++] = current_num + '0';
  output_string[idx++] = current;

  if (calls == 0) {
    printf("Call %d, output length: %d\n", calls, idx);
  } else {
    return solve(output_string, input_string, calls - 1);
  }
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  char input[5000000] = {[0 ... 4999999] = '\0'};
  char output[5000000] = {[0 ... 4999999] = '\0'};
  strcpy(input, argv[1]);
  solve(input, output, atoi(argv[2]) - 1);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 329356 is the right answer for part 1
// Execution time: 0.004290 seconds

// 4666278 is the right answer for part 2
// Execution time: 0.060848 seconds

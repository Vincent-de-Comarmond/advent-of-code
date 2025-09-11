#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int *parse_line(char *line) {
  int i = 0;
  int *rep_vs_actual = malloc(2 * sizeof(int));
  rep_vs_actual[0] = strlen(line);
  rep_vs_actual[1] = rep_vs_actual[0] - 2; // -2 for enclosing parentheses

  char a = '\0', b = '\0';
  for (i = 1; i < strlen(line); i++) {
    a = line[i - 1], b = line[i];
    if (a == '\\') {
      switch (b) {
      case '\\':
        rep_vs_actual[1] -= 1;
        i++;
        break;
      case '\"':
        rep_vs_actual[1] -= 1;
        break;
      case 'x':
        rep_vs_actual[1] -= 3;
        break;
      }
    }
  }
  return rep_vs_actual;
}

int solve(char *file_path) {
  int buffer_size = 250;
  char line[buffer_size];
  FILE *file = fopen(file_path, "r");

  int total = 0;
  while (fgets(line, buffer_size, file)) {
    line[strcspn(line, "\r\n")] = 0;
    int *parsedline = parse_line(line);
    total += parsedline[0] - parsedline[1];
    free(parsedline);
  }

  fclose(file);
  return total;
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  printf("Literal vs Memory Diff: %d\n", solve(argv[1]));
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 1360 is too high for part 1
// 1333 is the right answer for part 1
// Execution time: 0.000094 seconds

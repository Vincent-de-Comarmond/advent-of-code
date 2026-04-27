#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Note these are relatively prime ... We can use Fermat's little theorem
// (possibly)
static unsigned long INITIAL = 20151125;
static unsigned long MULTIPLIER = 252533;
static unsigned long MODULO = 33554393;

unsigned long long item_number(uint row, uint col) {
  return ((row + col) * (row + col) - col - 3 * row + 2) / 2;
}

int solve(char *filename) {
  FILE *file = fopen(filename, "r");
  char line[1000];
  if (fgets(line, 1000, file) == NULL) {
    fclose(file);
    return EXIT_FAILURE;
  }
  fclose(file);

  uint i, row, col;
  sscanf(line,
         "To continue, please consult the code grid in the manual.  Enter the "
         "code at row %u, column %u.",
         &row, &col);

  unsigned long long power = item_number(row, col) - 1;
  // Try apply Fermat's little theorem
  while (MODULO < power)
    power /= MODULO;

  unsigned long long result = INITIAL;
  for (i = 0; i < power; i++)
    result = (result * MULTIPLIER) % MODULO;

  printf("Desired code is %llu\n", result);
  return EXIT_SUCCESS;
}

int main(int argc, char *argv[]) {
  clock_t start;
  start = clock();
  int solved = solve(argv[1]);
  if (solved == EXIT_FAILURE) {
    printf("Program FAILED\n");
  }

  printf("Execution time is %.3f s",
         (clock() - start) / (double)CLOCKS_PER_SEC);
  return solved;
}


// 9132360 is the right answer
// Execution time is 0.068 s



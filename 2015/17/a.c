#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void sortarray(int size, int source[size], int dest[size]) {
  int i, j;

  int num_less[size];
  for (i = 0; i < size; i++)
    num_less[i] = 0;

  for (i = 0; i < size; i++)
    for (j = i + 1; j < size; j++)
      num_less[source[j] > source[i] ? i : j]++;

  for (i = 0; i < size; i++) {
    j = num_less[i];
    dest[j] = source[i];
  }
}

int min_contributors(int target, int num, int sorted[num]) {
  int i = 0, total = 0;
  for (i = 0; i < num; i++) {
    total += sorted[i];
    if (target <= total)
      break;
  }
  return i + 1;
}

int max_contributors(int target, int num, int sorted[num]) {
  int i = 0, total = 0;
  for (i = 0; i < num; i++) {
    total += sorted[num - 1 - i];
    if (target <= total)
      break;
  }
  return i + 1;
}

void solve_i(int idx, int remaining_target, int remaining_choices, int num,
             int containers[num], int *counter) {

  bool is_last = remaining_choices == 1;

  if (idx < num) {

    if (is_last && remaining_target == containers[idx]) {
      (*counter)++;
    }

    solve_i(idx + 1, remaining_target, remaining_choices, num, containers,
            counter);

    if (containers[idx] < remaining_target) {
      solve_i(idx + 1, remaining_target - containers[idx],
              remaining_choices - 1, num, containers, counter);
    }
  }
}

int count_combos(int target, int num, int containers[num]) {
  int min, max, sorted[num];
  sortarray(num, containers, sorted);
  min = min_contributors(target, num, sorted);
  max = max_contributors(target, num, sorted);

  int counter = 0;
  for (int i = min; i <= max; i++) {

    solve_i(0, target, i, num, containers, &counter);
  }

  return counter;
}

void solve(int litres, char *filepath) {
  FILE *file = fopen(filepath, "r");
  if (file == NULL)
    printf("FAIL - could not open file.\n");

  char linebuf[10];
  int idx = 0;
  int containers[100] = {0};

  while (fgets(linebuf, 10, file))
    containers[idx++] = atoi(linebuf);
  fclose(file);

  int combos = count_combos(litres, idx, containers);
  printf("Valid combinations: %d\n", combos);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  solve(atoi(argv[1]), argv[2]);
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// 4372 is the right answer for part 1
// Execution time: 0.007460 seconds

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void get_instructions(char *filename, int buffersize, char *instructions) {
  FILE *file = fopen(filename, "r");

  if (file != NULL) {
    fgets(instructions, buffersize, file);
  }
  fclose(file);
}

void interpret_instruction(char instruction, int *location) {
  switch (instruction) {
  case '^':
    location[0]--;
    break;
  case '>':
    location[1]++;
    break;
  case 'v':
    location[0]++;
    break;
  case '<':
    location[1]--;
    break;
  }
}

void houses_got_presents(char *filename) {

  int idx, idx2;
  int numchars = 10000;
  int santa_loc[2] = {0, 0};
  int robosanta_loc[2] = {0, 0};
  char instructions[numchars];
  get_instructions(filename, numchars, instructions);

  int is[numchars];
  int js[numchars];
  int head = 1;

  is[0] = 0, js[0] = 0;

  for (idx = 0; idx < (int)strlen(instructions); idx++) {
    if (idx % 2 == 0) {
      interpret_instruction(instructions[idx], santa_loc);
      is[head] = santa_loc[0];
      js[head] = santa_loc[1];
    } else {
      interpret_instruction(instructions[idx], robosanta_loc);
      is[head] = robosanta_loc[0];
      js[head] = robosanta_loc[1];
    }
    head++;
  }

  bool broken = false;
  int i, j, i2, j2, deliveries = 0;

  for (idx = 0; idx < head; idx++) {
    broken = false;
    i = is[idx], j = js[idx];

    for (idx2 = 0; idx2 < idx; idx2++) {
      i2 = is[idx2], j2 = js[idx2];
      if (i == i2 && j == j2) {
        broken = true;
        break;
      }
    }

    if (!broken) {
      deliveries++;
    }
  }

  printf("Houses getting presents: %d\n", deliveries);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  houses_got_presents(argv[1]);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 1505 is too low for part 2
// 2639 is the right answer for part 2

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

  int numchars = 10000;
  int location[2] = {0, 0};
  char instructions[numchars];
  get_instructions(filename, numchars, instructions);

  int is[numchars];
  int js[numchars];
  int presents[numchars];
  bool broken = false;

  is[0] = 0;
  js[0] = 0;
  presents[0] = 1;
  int idx, idx2, delivered = 1;

  for (idx = 0; idx < strlen(instructions); idx++) {
    interpret_instruction(instructions[idx], location);
    broken = false;

    for (idx2 = 0; idx2 < delivered; idx2++) {
      if (is[idx2] == location[0] && js[idx2] == location[1]) {
        presents[idx2]++;
        broken = true;
        break;
      }
    }

    if (!broken) {
      is[delivered] = location[0];
      js[delivered] = location[1];
      delivered++;
    }
  }

  printf("Houses getting presents: %d\n", delivered);
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

// 5108 is too high for part 1
// 2565 is the right answer for part 1

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int REGISTERS[2] = {0, 0};
static int INSTRUCTIONS[1000][3] = {[0 ... 999] = {[0 ... 2] = -1}};
typedef enum { HALF, TRIPLE, INCREMENT, JUMP, JUMP_EVEN, JUMP_IF_ONE } Actions;

int load_instructions(char *filename) {

  int reg;
  int num = 0;
  char dummy = '\0';

  FILE *file = fopen(filename, "r");
  char lbuf[1000] = {[0 ... 999] = '\0'};

  while (fgets(lbuf, 1000, file)) {
    reg = (lbuf[4] == 'a') ? 0 : (lbuf[4] == 'b') ? 1 : -1;

    switch (lbuf[0]) {
    case 'j':
      if (lbuf[1] == 'm') {
        INSTRUCTIONS[num][0] = JUMP;
        sscanf(lbuf, "jmp %d", &INSTRUCTIONS[num][2]);
      } else if (lbuf[2] == 'e') {
        INSTRUCTIONS[num][0] = JUMP_EVEN;
        INSTRUCTIONS[num][1] = reg;
        sscanf(lbuf, "jie %c, %d", &dummy, &INSTRUCTIONS[num][2]);
      } else {
        INSTRUCTIONS[num][0] = JUMP_IF_ONE;
        INSTRUCTIONS[num][1] = reg;
        sscanf(lbuf, "jio %c, %d", &dummy, &INSTRUCTIONS[num][2]);
      }
      break;
    case 'h':
      INSTRUCTIONS[num][0] = HALF;
      INSTRUCTIONS[num][1] = reg;
      INSTRUCTIONS[num][2] = 1;
      break;
    case 't':
      INSTRUCTIONS[num][0] = TRIPLE;
      INSTRUCTIONS[num][1] = reg;
      INSTRUCTIONS[num][2] = 1;
      break;
    case 'i':
      INSTRUCTIONS[num][0] = INCREMENT;
      INSTRUCTIONS[num][1] = reg;
      INSTRUCTIONS[num][2] = 1;
      break;
    }

    num++;
  }

  fclose(file);
  return num;
}

void solve(char *filename) {
  int i = 0;
  int action, reg, inc;
  int nlines = load_instructions(filename);

  while ((0 <= i) && (i < nlines)) {
    action = INSTRUCTIONS[i][0];
    reg = INSTRUCTIONS[i][1];
    inc = INSTRUCTIONS[i][2];

    switch (action) {
    case HALF:
      REGISTERS[reg] /= 2;
      break;
    case TRIPLE:
      REGISTERS[reg] *= 3;
      break;
    case INCREMENT:
      REGISTERS[reg]++;
      break;
    case JUMP:
      break;
    case JUMP_EVEN:
      if (REGISTERS[reg] % 2 != 0) // i.e. not even then normal increment
        inc = 1;
      break;
    case JUMP_IF_ONE:
      if (REGISTERS[reg] != 1) // i.e. not equal to one then normal increment
        inc = 1;
      break;
    }

    i += inc;
  }

  printf("Value of register 'b' at end of program is %d\n", REGISTERS[1]);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// 0 is the wrong answer
// 307 is the correct answer for part 1
// Execution time is 0.000060 seconds

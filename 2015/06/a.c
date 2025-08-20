#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int grid[1000][1000] = {{0}};

void turn_on(int r0, int c0, int r1, int c1) {
  int i, j;
  for (i = r0; i <= r1; i++) {
    for (j = c0; j <= c1; j++) {
      grid[i][j] = 1;
    }
  }
}

void turn_off(int r0, int c0, int r1, int c1) {
  int i, j;
  for (i = r0; i <= r1; i++) {
    for (j = c0; j <= c1; j++) {
      grid[i][j] = 0;
    }
  }
}

void toggle(int r0, int c0, int r1, int c1) {
  int i, j;
  for (i = r0; i <= r1; i++) {
    for (j = c0; j <= c1; j++) {
      grid[i][j] = 1 - grid[i][j];
    }
  }
}

int count_lights_turned_on() {
  int i, j, on = 0;
  for (i = 0; i < 1000; i++) {
    for (j = 0; j < 1000; j++) {
      on += grid[i][j];
    }
  }
  return on;
}

void make_display_and_count(char *filename) {
  int buf_size = 200;
  FILE *file = fopen(filename, "r");
  char line[buf_size];

  int r0, c0, r1, c1;
  char *dimensions;

  while (fgets(line, buf_size, file)) {
    /* printf("%s", line); */
    if (strstr(line, "on") != NULL) {
      sscanf(line, "turn on %d,%d through %d,%d", &r0, &c0, &r1, &c1);
      turn_on(r0, c0, r1, c1);
      continue;
    }

    if (strstr(line, "off") != NULL) {
      sscanf(line, "turn off %d,%d through %d,%d", &r0, &c0, &r1, &c1);
      turn_off(r0, c0, r1, c1);
      continue;
    }

    sscanf(line, "toggle %d,%d through %d,%d", &r0, &c0, &r1, &c1);
    toggle(r0, c0, r1, c1);
  }

  fclose(file);
  printf("Number lights turned on: %d\n", count_lights_turned_on());
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  make_display_and_count(argv[1]);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}
// 78099 is too low for part 1
// 377891 is the right answer for part 1

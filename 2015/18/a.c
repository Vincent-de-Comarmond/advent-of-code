#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void update(int gridsize, char grid[gridsize][gridsize]) {
  bool state;
  int i, j, k, l, neighbours;

  char newgrid[gridsize][gridsize];
  size_t size = sizeof(char) * gridsize * gridsize;
  memcpy(newgrid, grid, size);

  for (i = 0; i < gridsize; i++)
    for (j = 0; j < gridsize; j++) {
      neighbours = 0;
      state = grid[i][j] == '#';

      for (k = i - 1; k <= i + 1; k++)
        for (l = j - 1; l <= j + 1; l++)
          if (0 <= k && k < gridsize && 0 <= l && l < gridsize &&
              (k != i || l != j) && grid[k][l] == '#')
            neighbours++;

      if (!state && neighbours == 3)
        newgrid[i][j] = '#';
      else if (state && (neighbours == 2 || neighbours == 3)) {
      } else
        newgrid[i][j] = '.';
    }

  memcpy(grid, newgrid, size);
}

int count_on(int gridsize, char grid[gridsize][gridsize]) {
  int i, j, total = 0;

  for (i = 0; i < gridsize; i++)
    for (j = 0; j < gridsize; j++)
      if (grid[i][j] == '#')
        total++;

  return total;
}

void printgrid(int gridsize, char grid[gridsize][gridsize]) {
  for (int i = 0; i < gridsize; i++) {
    for (int j = 0; j < gridsize; j++)
      printf("%c", grid[i][j]);
    printf("\n");
  }
}

void solve(int steps, int gridsize, char *filepath) {
  int row = 0;
  char linebuffer[gridsize + 2];
  char grid[gridsize][gridsize];

  FILE *file = fopen(filepath, "r");
  if (file == NULL)
    printf("FAIL - could not open file.\n");
  while (fgets(linebuffer, gridsize + 2, file))
    memcpy(grid[row++], linebuffer, gridsize * sizeof(char));
  fclose(file);

  for (int i = 0; i < steps; i++)
    update(gridsize, grid);

  int total_on = count_on(gridsize, grid);
  printf("Total lights on: %d\n", total_on);
}

int main(int argc, char *argv[]) {
  time_t start, end;

  start = clock();
  solve(atoi(argv[1]), atoi(argv[2]), argv[3]);
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}


// 1061 is the right answer for part 1
// Execution time: 0.025877 seconds

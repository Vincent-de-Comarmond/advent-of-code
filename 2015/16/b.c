#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void print_sue(int sue[10]) {
  char *names[10] = {"children", "cats",    "samoyeds", "pomeranians",
                     "akitas",   "vizslas", "goldfish", "trees",
                     "cars",     "perfumes"};
  for (int i = 0; i < 10; i++)
    if (sue[i] != -1)
      printf("%s: %d, ", names[i], sue[i]);

  printf("\n");
}

const int GIFT_SUE[10] = {
    3, // children
    7, // cats
    2, // samoyeds
    3, // pomeranians
    0, // akitas
    0, // vizslas
    5, // goldfish
    3, // trees
    2, // cars
    1  // perfumes
};

int determine_index(char *token) {
  if (strcmp(token, "children") == 0)
    return 0;
  if (strcmp(token, "cats") == 0)
    return 1;
  if (strcmp(token, "samoyeds") == 0)
    return 2;
  if (strcmp(token, "pomeranians") == 0)
    return 3;
  if (strcmp(token, "akitas") == 0)
    return 4;
  if (strcmp(token, "vizslas") == 0)
    return 5;
  if (strcmp(token, "goldfish") == 0)
    return 6;
  if (strcmp(token, "trees") == 0)
    return 7;
  if (strcmp(token, "cars") == 0)
    return 8;
  if (strcmp(token, "perfumes") == 0)
    return 9;
  return -1;
}

void solve(char *filepath) {

  FILE *file = fopen(filepath, "r");
  if (file == NULL)
    printf("FAIL - could not open file.\n");

  int sue_idx = 0;
  int char_idx = -1;
  char linebuf[1000] = {[0 ... 999] = '\0'};
  int sues[500][10] = {[0 ... 499] = {[0 ... 9] = -1}};
  char *next_token;

  while (fgets(linebuf, 1000, file)) {
    next_token = strtok(linebuf, ": ");
    while (next_token != NULL) {
      if (char_idx != -1) {
        sues[sue_idx][char_idx] = atoi(next_token);
        char_idx = -1;
      } else {
        char_idx = determine_index(next_token);
      }
      next_token = strtok(NULL, ": ");
    }
    sue_idx++;
  }
  fclose(file);

  bool match = true;
  int i = 0, j = 0;

  for (i = 0; i < sue_idx; i++) {
    match = true;

    for (j = 0; j < 10; j++) {
      if (sues[i][j] == -1)
        continue;

      if (j == 1 || j == 7) {
        // Real sue must have more cats or trees
        if (!(GIFT_SUE[j] < sues[i][j])) {
          match = false;
          break;
        }
      } else if (j == 3 || j == 6) {
        if (!(sues[i][j] < GIFT_SUE[j])) {
          // Real sue must have fewer pomeranians and goldfish
          match = false;
          break;
        }
      } else if (sues[i][j] != GIFT_SUE[j]) {

        match = false;
        break;
      }
    }
    if (match) {
      printf("Gift sue number: %d\n", i + 1);
      break;
    }
  }
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

// Sue 373 is the one that gifted (part 1)
// Execution time: 0.000213 seconds

// 373 is the wrong answer for aprt 2
// 260 is the right answer for part 2
// Execution time: 0.000222 seconds

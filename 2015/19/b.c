#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SRC_SIZE 3
#define _NT 45
#define WIDTH 550
#define MAX_DEST 10

int MIN_SO_FAR = (int)1e6;
int NUM_TRANS = 0;
char TARGET[WIDTH] = {[0 ... WIDTH - 1] = '\0'};
char SOURCES[_NT][3] = {[0 ... _NT - 1] = {'\0', '\0', '\0'}};
char DESTINATIONS[_NT][MAX_DEST + 1] = {
    [0 ... _NT - 1] = {[0 ... MAX_DEST] = '\0'}};

void parse_input(char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    printf("FAILED - could not open file");
    exit(EXIT_FAILURE);
  }

  bool istarget = false;
  char buffer[WIDTH] = {[0 ... WIDTH - 1] = '\0'};

  while (fgets(buffer, WIDTH, file)) {
    buffer[strcspn(buffer, "\n")] = 0;

    if (strlen(buffer) == 0) {
      istarget = true;
      continue;
    }

    if (istarget) {
      memcpy(TARGET, buffer, WIDTH);
      break;
    }

    // Reverse source and destination from part 1
    char *source = strtok(buffer, " => ");
    char *dest = strtok(NULL, " => ");
    memcpy(SOURCES[NUM_TRANS], source, SRC_SIZE * sizeof(char));
    memcpy(DESTINATIONS[NUM_TRANS], dest, strlen(dest) * sizeof(char));
    NUM_TRANS++;
  }
  fclose(file);
}

char *limited_search_replace(char target[WIDTH], char *search, char *replace,
                             int start, int limit) {

  char *replaced = malloc(WIDTH * sizeof(char));
  memset(replaced, '\0', WIDTH * sizeof(char));

  int i, j, rlen = strlen(replace), slen = strlen(search);
  for (i = start; i < limit; i++) {
    bool match = true;
    for (int j = 0; j < slen; j++) {
      if (search[j] != target[i + j]) {
        match = false;
        break;
      }
    }

    if (match) {
      for (j = 0; j < i; j++)
        replaced[j] = target[j];
      for (j = 0; j < rlen; j++)
        replaced[i + j] = replace[j];
      for (j = i + rlen; j < WIDTH; j++)
        replaced[j] = target[j + slen - rlen];
      break;
    }
  }

  return replaced;
}

void solve(char *filename) {
  parse_input(filename);

  int i, j, k, idx = 0, idx_cpy = 0, gen = 0;
  bool duplicate = false;

  int GEN_SIZE = (int)1e6;

  char(*targets)[WIDTH] = malloc(sizeof(char[GEN_SIZE][WIDTH]));
  memset(targets, '\0', sizeof(char[GEN_SIZE][WIDTH]));
  strcpy(targets[idx], TARGET);
  idx++;

  char(*targcpy)[WIDTH] = malloc(sizeof(char[GEN_SIZE][WIDTH]));
  memset(targcpy, '\0', sizeof(char[GEN_SIZE][WIDTH]));

  while (gen < (int)1e6) {
    for (i = 0; i < idx; i++) {
      for (j = 0; j < NUM_TRANS; j++) {
        char *source = SOURCES[j];
        char *dest = DESTINATIONS[j];

        for (k = 0; k < 2 * MAX_DEST; k++) {
          char *replacement;
          replacement =
              limited_search_replace(targets[i], dest, source, k, 2 * MAX_DEST);
          if (0 < strlen(replacement)) {
            strcpy(targcpy[idx_cpy], replacement);
            idx_cpy++;
            if (strlen(replacement) == 1) {
              printf("Generations: %d\n", gen + 1);
              return;
            }
          }
          free(replacement);
        }
      }
    }

    idx = 0;
    memset(targets, '\0', sizeof(char[GEN_SIZE][WIDTH]));

    for (i = 0; i < idx_cpy; i++) {
      duplicate = false;

      for (j = 0; j < idx; j++) {
        if (strcmp(targets[j], targcpy[i]) == 0) {
          duplicate = true;
          break;
        }
      }

      if (!duplicate) {
        strcpy(targets[idx], targcpy[i]);
        idx++;
      }
    }

    idx_cpy = 0;
    memset(targcpy, '\0', sizeof(char[GEN_SIZE][WIDTH]));
    gen++;
  }
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

// 206 is too low
// 207 is the correct answer
// Execution time: 934.684603

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SRC_SIZE 3
#define _NT 45
#define WIDTH 550
#define MAX_DEST 10

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

int limited_search_replace(char target[WIDTH], char *search, char *replace,
                           int start, int limit) {
  int targlen = strlen(target);
  int searchlen = strlen(search);
  int repllen = strlen(replace);

  char copy[WIDTH];
  strcpy(copy, target);
  int end = limit < targlen ? limit - searchlen : targlen - searchlen;

  int i = 0;
  for (i = start; i < end; i++) {
    bool match = true;
    for (int j = 0; j < searchlen; j++) {
      if (search[j] != target[i + j]) {
        match = false;
        break;
      }
    }

    if (!match)
      continue;

    for (int j = 0; j < repllen; j++)
      target[i + j] = replace[j];

    for (int j = i + repllen; j < targlen + repllen - searchlen; j++)
      target[j] = target[j + repllen - searchlen];

    printf("%s\n", copy);
    printf("%s\n", target);
  }

  // IDEA is stupid-simple ... if returned index is limit nothing has been
  // replaced AND nothing can be replace. If index is less than final we have to
  // try all replacements on the next character from the index
  return i + searchlen;
}

void solve(char *filename) {
  parse_input(filename);

  int idx = 0, idx_cpy = 0, gen = 0;
  char tmp[WIDTH];
  char(*targets)[WIDTH] = malloc(sizeof(char[(int)1e3][WIDTH]));
  memset(targets, '\0', sizeof(char[(int)1e3][WIDTH]));

  char(*targcpy)[WIDTH] = malloc(sizeof(char[(int)1e3][WIDTH]));
  memset(targcpy, '\0', sizeof(char[(int)1e3][WIDTH]));

  strcpy(targets[idx], TARGET);
  idx++;

  while (gen < (int)1e6) {
    for (int i = 0; i < idx; i++) {
      for (int j = 0; j < NUM_TRANS; j++) {
        char *source = SOURCES[j];
        char *dest = DESTINATIONS[j];
        int start_idx = 0;

        while (start_idx < MAX_DEST) {
          memset(tmp, '\0', sizeof(tmp));
          strcpy(tmp, targets[i]);

          start_idx = limited_search_replace(tmp, dest, source, start_idx + 1,
                                             MAX_DEST);

          if (-1 < start_idx && start_idx < MAX_DEST) {
            printf("Start idx: %d\n", start_idx);
            printf("Tried to replace %s -> %s\n", dest, source);
            printf("Input: %s\n", targets[i]);
            printf("Output: %s\n", tmp);

            strcpy(targcpy[idx_cpy], tmp);
            idx_cpy++;
          }
        }
      }
    }

    idx = 0;
    memset(targets, '\0', sizeof(char[(int)1e3][WIDTH]));

    for (int i = 0; i < idx_cpy; i++) {
      bool duplicate = false;

      for (int j = 0; j < idx; j++) {
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
    memset(targcpy, '\0', sizeof(char[(int)1e3][WIDTH]));
  }
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

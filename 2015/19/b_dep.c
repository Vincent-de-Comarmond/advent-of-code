#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define LENGTH 1000000
#define WIDTH 550

struct TransmutationStruct {
  char element[11];
  int num_output;
  char outputs[10][11];
};

typedef struct TransmutationStruct Transmuation;

int deconstruct(int num_sources, int gen, int num_transforms,
                Transmuation transmutations[50], char sources[LENGTH][WIDTH],
                char destinations[LENGTH][WIDTH]

) {
  bool match = false;
  int i, j, k, l, m, reductions = 0;

  for (i = 0; i < LENGTH; i++)
    for (j = 0; j < WIDTH; j++)
      destinations[i][j] = '\0';

  printf("Generations: %d\n", gen);
  printf("Num sources: %d\n", num_sources);

  char *target, substitute[11] = {[0 ... 10] = '\0'};
  char new_word[WIDTH] = {[0 ... WIDTH - 1] = '\0'};

  for (i = 0; i < num_sources; i++) {
    target = sources[i];
    int target_len = strlen(target);
    if (strcmp("e", target) == 0)
      return gen;

    for (j = 0; j < target_len; j++) {
      for (k = 0; k < num_transforms; k++) {
        Transmuation t = transmutations[k];
        int swap_len = strlen(t.element);

        for (l = 0; l < 11; l++)
          substitute[l] = l < swap_len ? sources[i][j + l] : '\0';

        if (strcmp(t.element, substitute) != 0)
          continue;

        for (l = 0; l < t.num_output; l++) {
          char *replacement = t.outputs[l];
          int repl_len = strlen(replacement);

          for (m = 0; m < j; m++)
            new_word[m] = target[m];
          for (m = j; m < j + repl_len; m++)
            new_word[m] = replacement[m - j];
          for (m = j + swap_len; m < target_len; m++)
            new_word[m - swap_len + repl_len] = target[m];
          new_word[target_len - strlen(substitute) + repl_len] = '\0';

          match = false;
          for (m = 0; m < reductions; m++)
            if (strcmp(new_word, destinations[m]) == 0) {
              match = true;
              break;
            }

          if (!match) {
            strcpy(destinations[reductions++], new_word);
            if (reductions % 10000 == 0) {
              printf("%% complete: %.2f\n", 100.0 * (i + 1) / num_sources);
              printf("Number destinations: %d\n", reductions);
            }
          }
        }
      }
    }
  }

  return deconstruct(reductions, gen + 1, num_transforms, transmutations,
                     destinations, sources

  );
}

void solve(char *filename) {

  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    printf("FAILED - could not open file");
  }

  int i = 0;
  bool found = false;
  bool istarget = false;

  char target[1000], buffer[1000];
  int idx = 0;
  char *source, *transition;
  Transmuation transmutations[1000];

  while (fgets(buffer, 1000, file)) {
    buffer[strcspn(buffer, "\n")] = 0;
    if (strlen(buffer) == 0) {
      istarget = true;
      continue;
    }

    if (istarget) {
      memcpy(target, buffer, 1000);
      break;
    } else {
      // Reverse source and destination from part 1
      transition = strtok(buffer, " => ");
      source = strtok(NULL, " => ");

      found = false;
      for (i = 0; i < idx; i++)
        if (strcmp(source, transmutations[i].element) == 0) {
          found = true;
          break;
        }

      if (found) {

        strcpy(transmutations[i].outputs[transmutations[i].num_output],
               transition);
        transmutations[i].num_output++;
      } else {
        strcpy(transmutations[idx].element, source);
        strcpy(transmutations[idx].outputs[0], transition);
        transmutations[idx].num_output = 1;
        idx++;
      }
    }
  }
  fclose(file);

  char(*sources)[WIDTH] = malloc(sizeof(char[LENGTH][WIDTH]));
  char(*destinations)[WIDTH] = malloc(sizeof(char[LENGTH][WIDTH]));

  strcpy(sources[0], target);

  int generations =
      deconstruct(1, 0, idx, transmutations, sources, destinations);
  printf("Min synthesis generations: %d\n", generations);
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

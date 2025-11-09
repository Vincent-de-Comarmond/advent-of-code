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

float ave_str_len(int num_elements, char array_of_strings[LENGTH][WIDTH]) {
  float result = 0;
  for (int i = 0; i < num_elements; i++)
    result += (float)strlen(array_of_strings[i]) / (float)num_elements;

  return result;
}

int construct(int generation, char *target, int num_transforms,
              Transmuation transmutations[50], int num_sources,
              char inputs[LENGTH][WIDTH], char outputs[LENGTH][WIDTH]

) {

  int num_outputs = 0;
  int target_length = strlen(target);

  for (int i = 0; i < LENGTH; i++)
    for (int j = 0; j < WIDTH; j++)
      outputs[i][j] = '\0';

  printf("Generations: %d\n", generation);
  printf("Num sources: %d\n", num_sources);
  printf("Ave source len /Target Length: %f/%d\n",
         ave_str_len(num_sources, inputs), target_length);

  for (int i = 0; i < num_sources; i++) {
    char *source = inputs[i];
    int word_len = strlen(source);
    for (int j = 0; j < word_len; j++) {
      for (int k = 0; k < num_transforms; k++) {
        bool matches = true;
        Transmuation transform = transmutations[k];
        int rem_len = strlen(transform.element);

        for (int l = 0; l < rem_len; l++)
          if (transform.element[l] != source[j + l]) {
            matches = false;
            break;
          }

        if (!matches)
          continue;

        for (int l = 0; l < transform.num_output; l++) {
          char new_word[WIDTH] = {[0 ... WIDTH - 1] = '\0'};
          char *replacement = transform.outputs[l];
          int rep_len = strlen(replacement);

          for (int m = 0; m < j; m++)
            new_word[m] = source[m];
          for (int m = j; m < j + rep_len; m++)
            new_word[m] = replacement[m - j];
          for (int m = j + rem_len; m < word_len; m++)
            new_word[m - rem_len + rep_len] = source[m];
          new_word[word_len - rem_len + rep_len] = '\0';

          if (strcmp(new_word, target) == 0)
            return generation;
          if (strlen(target) <= strlen(new_word))
            continue;

          matches = false;
          for (int m = 0; m < num_outputs; m++)
            if (strcmp(new_word, outputs[m]) == 0) {
              matches = true;
              break;
            }

          if (!matches) {
            strcpy(outputs[num_outputs++], new_word);
            /* printf("Added: %s\n", outputs[num_outputs - 1]); */
          }
        }
      }
    }
  }

  return construct(generation + 1, target, num_transforms, transmutations,
                   num_outputs, outputs, inputs);
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
      source = strtok(buffer, " => ");
      transition = strtok(NULL, " => ");

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

  char(*inputs)[WIDTH] = malloc(sizeof(char[LENGTH][WIDTH]));
  char(*outputs)[WIDTH] = malloc(sizeof(char[LENGTH][WIDTH]));

  for (int i = 0; i < LENGTH; i++)
    for (int j = 0; j < WIDTH; j++) {
      inputs[i][j] = '\0';
      outputs[i][j] = '\0';
    }

  inputs[0][0] = 'e';

  printf("Target: %s\n", target);
  int generations =
      construct(0, target, idx, transmutations, 1, inputs, outputs);

  /* deconstruct(1, 0, idx, transmutations, sources, destinations); */
  printf("Min synthesis generations: %d\n", generations);
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

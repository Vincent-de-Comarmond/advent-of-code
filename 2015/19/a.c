#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

struct TransmutationStruct {
  char element[3];
  int num_output;
  char outputs[10][11];
};

typedef struct TransmutationStruct Transmuation;

int possible_modifications(char *target, int num_transforms,
                           Transmuation transmutations[1000]) {

  int i, j, k, l, idx = 0;
  char *output;
  char to_replace[3];
  char(*replacements)[1000] = malloc(sizeof(char[(int)1e4][1000]));
  Transmuation transformation;

  int target_len = strlen(target);

  for (i = 0; i < target_len; i++) {
    for (j = 0; j < num_transforms; j++) {

      transformation = transmutations[j];
      to_replace[0] = '\0', to_replace[1] = '\0', to_replace[2] = '\0';
      int torep_len = strlen(transformation.element);

      for (k = 0; k < torep_len; k++)
        to_replace[k] = target[i + k];

      if (strcmp(transformation.element, to_replace) == 0) {

        for (k = 0; k < transformation.num_output; k++) {

          output = transformation.outputs[k];
          int output_len = strlen(output);

          for (l = 0; l < i; l++)
            replacements[idx][l] = target[l];

          for (l = i; l < i + output_len; l++)
            replacements[idx][l] = output[l - i];

          for (l = i + torep_len; l < target_len; l++)
            replacements[idx][l - torep_len + output_len] = target[l];

          replacements[idx][target_len - torep_len + output_len] = '\0';
          idx++;
        }
      }
    }
  }

  int idx2 = 0;
  bool match = false;
  char(*uniques)[1000] = malloc(sizeof(char[idx][1000]));

  for (i = 0; i < idx; i++) {
    for (j = 0; j < idx2; j++) {
      match = false;
      if (strcmp(replacements[i], uniques[j]) == 0) {
        match = true;
        break;
      }
    }
    if (!match)
      strcpy(uniques[idx2++], replacements[i]);
  }
  return idx2;
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

  int num_modifications = possible_modifications(target, idx, transmutations);
  printf("Number of possible modifications is: %d\n", num_modifications);
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

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

void possible_modifications(char *target, int num_transforms,
                            Transmuation transmutations[1000]) {

  int i, j, k, l, idx = 0;
  char *output;
  char to_replace[3];
  char(*replacements)[1000] = malloc(sizeof(char[(int)1e5][1000]));
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

          printf("Input -> Output: %s -> %s\n", to_replace, output);

          for (l = 0; l < i; l++) {
            replacements[idx][l] = target[l];
            printf("\talpha:\treplacements[%d][%d] = %c\n", idx, l,
                   replacements[idx][l]);
          }
          for (l = i; l < i + output_len; l++) {
            printf("l -i: %d", l - i);
            replacements[idx][l] = output[l - i];
            printf("\tbeta:\treplacements[%d][%d] = %c\n", idx, i + l,
                   replacements[idx][l]);
          }
          for (l = i + torep_len; l < target_len; l++) {
            replacements[idx][l - torep_len + output_len] = target[l];
            printf("\tgamma:\treplacements[%d][%d] = %c\n", idx,
                   l - torep_len + output_len,
                   replacements[idx][l - torep_len + output_len]);
          }

          printf("Final idx: %d\n", target_len - torep_len + output_len);
          replacements[idx][target_len - torep_len + output_len] = '\0';
          printf("Final: %s\n", replacements[idx]);
          idx++;
        }
      }
    }
  }

  


  
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

  /* for (i = 0; i < idx; i++) { */
  /*   printf("%s\n", transmutations[i].element); */
  /*   printf("\t%s", transmutations[i].outputs[0]); */
  /*   for (int j = 1; j < transmutations[i].num_output; j++) */
  /*     printf(", %s", transmutations[i].outputs[j]); */
  /*   printf("\n"); */
  /* } */
  printf("Target:%s\n", target);
  /* printf("Num transformations: %d\n", idx); */

  possible_modifications(target, idx, transmutations);

  fclose(file);
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

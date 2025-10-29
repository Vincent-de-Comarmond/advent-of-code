#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define EL_SIZE 3
#define WIDTH 550
#define TRANSFORMS 50
#define MSIZE 10
#define MAX (int)1e6

typedef char Element[EL_SIZE];
typedef char Molecule[WIDTH][EL_SIZE];

static char dests[TRANSFORMS][MSIZE][EL_SIZE] = {
    [0 ... TRANSFORMS - 1] = {[0 ... MSIZE - 1] = {'\0', '\0', '\0'}}};
static int dest_sizes[TRANSFORMS] = {[0 ... TRANSFORMS - 1] = 0};

static char sources[TRANSFORMS][EL_SIZE] = {
    [0 ... TRANSFORMS - 1] = {'\0', '\0', '\0'}};

static char target[WIDTH][EL_SIZE] = {[0 ... WIDTH - 1] = {'\0', '\0', '\0'}};

int read_element(char *mol_str, Element element) {
  element[0] = mol_str[0];
  if (strlen(mol_str) == 1)
    return 1;

  if ('a' <= mol_str[1] && mol_str[1] <= 'z') {
    element[1] = mol_str[1];
    return 2;
  }
  return 1;
}

int read_molecule(char *mol_str, Molecule molecule, int number) {
  int accum = 0, idx = 0, offset = 0;
  char copy[WIDTH] = {[0 ... WIDTH - 1] = '\0'};
  strcpy(copy, mol_str);

  if (number == -1)
    while (0 < strlen(copy)) {
      offset = read_element(copy, molecule[idx]);
      accum += offset;
      strncpy(copy, mol_str + accum, EL_SIZE);
      idx++;
    }
  else {
    while (idx < number && 0 < strlen(copy)) {
      offset = read_element(copy, molecule[idx]);
      accum += offset;
      strncpy(copy, mol_str + accum, EL_SIZE);
      idx++;
    }
  }
  return idx;
}

typedef struct _NBNUMS {
  int max_expand;
  int num_poss_react;
  int target_size;
} NBNUMS;

NBNUMS define_problem(char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL)
    exit(EXIT_FAILURE);

  int idx = 0, max_expansion = 0, targ_size = 0, tmp = 0;
  bool is_targ = false;
  char buffer[WIDTH];
  char *destination;

  while (fgets(buffer, WIDTH, file)) {
    buffer[strcspn(buffer, "\n")] = 0;
    if (strlen(buffer) == 0) {
      is_targ = true;
      continue;
    }

    if (is_targ) {
      targ_size = read_molecule(buffer, target, -1);
      printf("Target molecules: %d\n", targ_size);
      break;
    } else {
      strcpy(sources[idx], strtok(buffer, " => "));
      destination = strtok(NULL, " => ");
      tmp = read_molecule(destination, dests[idx], -1);
      max_expansion = max_expansion < tmp ? tmp : max_expansion;
      dest_sizes[idx] = tmp;
      idx++;
    }
  }
  fclose(file);

  NBNUMS nbnums;
  nbnums.max_expand = max_expansion;
  nbnums.num_poss_react = idx;
  nbnums.target_size = targ_size;
  return nbnums;
}

bool can_reduce(int targ_size, char this_target[targ_size][EL_SIZE],
                int reduction_size,
                char this_reduction[reduction_size][EL_SIZE], int targ_offset,
                int stop_idx) {

  if (stop_idx < targ_offset + reduction_size)
    return false;
  for (int i = 0; i < reduction_size; i++)
    if (strcmp(this_target[targ_offset + i], this_reduction[i]) != 0)
      return false;
  return true;
}

void solve(char *filename) {
  NBNUMS nbnums = define_problem(filename);

  /* printf("Max size: %d\nNum transforms: %d\nTarget size: %d\n", */
  /*        nbnums.max_expand, nbnums.num_poss_react, nbnums.target_size); */

  for (int i = 0; i < nbnums.num_poss_react; i++) {
    printf("Source: %s\n", sources[i]);
    for (int j = 0; j < dest_sizes[i]; j++)
      printf("\t-> %s\n", dests[i][j]);
  }

  /* for (int i = 0; i < nbnums.target_size; i++) */
  /*   printf(i == 0 ? "%s" : " %s", target[i]); */
  /* printf("\n"); */

  int gens = 0, max_gen = 1e4, targ_idx = 0, targ_cpy_idx = 0;
  size_t size = MAX * nbnums.target_size * EL_SIZE * sizeof(char);

  int targ_sizes[MAX] = {[0 ... MAX - 1] = 0};
  int targ_size_copy[MAX] = {[0 ... MAX - 1] = 0};
  targ_sizes[0] = nbnums.target_size;

  char(*targs)[nbnums.target_size][EL_SIZE];
  char(*targs_cpy)[nbnums.target_size][EL_SIZE];

  targs = malloc(MAX * sizeof(*targs));
  targs_cpy = malloc(MAX * sizeof(*targs_cpy));
  char tmp[nbnums.target_size][EL_SIZE];

  memset(targs, '\0', size);
  memset(targs_cpy, '\0', size);
  memset(tmp, '\0', nbnums.target_size * EL_SIZE * sizeof(char));

  for (int i = 0; i < nbnums.target_size; i++)
    strcpy(targs[targ_idx][i], target[i]);
  targ_idx++;

  while (gens < max_gen) {
    for (int i = 0; i < targ_idx; i++) {
      /* for (int j = 0; j < targ_sizes[i]; j++) */
      /*   printf("%s ", targs[i][j]); */
      printf("\nNum candidates: %d\n", targ_idx);
      printf("\nsize %d\n", targ_sizes[i]);

      for (int j = 0; j < nbnums.max_expand; j++) {
        for (int k = 0; k < nbnums.num_poss_react; k++) {
          if (can_reduce(nbnums.target_size, targs[i], dest_sizes[k], dests[k],
                         j, nbnums.max_expand)) {

            /* printf("Replacing: "); */
            /* for (int a = 0; a < dest_sizes[k]; a++) */
            /*   printf("%s ", dests[k][a]); */
            /* printf("\nWith: %s\n", sources[k]); */

            int new_size = targ_sizes[i] + 1 - dest_sizes[k];
            strcpy(tmp[0], sources[k]);

            if ((new_size == 1) && (tmp[0][0] == 'e')) {
              printf("Number generations: %d\n", gens);
              return;
            }

            /* printf("Here with new size %d\n", new_size); */
            for (int l = 1; l < new_size; l++)
              strcpy(tmp[l], targs[i][dest_sizes[k] + l - 1]);

            bool is_dup = false;
            for (int l = 0; l < targ_cpy_idx; l++) {
              is_dup = true;
              for (int m = 0; m < new_size; m++)
                if (strcmp(targs_cpy[l][m], tmp[m]) != 0) {
                  is_dup = false;
                  break;
                }
              if (is_dup)
                break;
            }

            if (!is_dup) {
              memcpy(targs_cpy[targ_cpy_idx], tmp, sizeof(tmp));
              targ_size_copy[targ_cpy_idx] = new_size;
              targ_cpy_idx++;
            }

            memset(tmp, '\0', sizeof(tmp));
          }
        }
      }
    }
    memcpy(targs, targs_cpy, size);
    memcpy(targ_sizes, targ_size_copy, MAX * sizeof(int));
    targ_idx = targ_cpy_idx;

    targ_cpy_idx = 0;
    memset(targ_size_copy, 0, MAX * sizeof(int));
    memset(targs_cpy, '\0', size);
    gens++;
  }
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

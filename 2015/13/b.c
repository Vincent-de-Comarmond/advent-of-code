#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

const int GUEST_NUM = 100;
const int NAME_LEN = 25;
const int NEG_INF = -(INT_MAX / 4); // big, and addition-safe

int populate_cost_matrix(char *filename,
                         int immediate_cost_matrix[GUEST_NUM][GUEST_NUM]) {
  int i = 0, j = 0, name_idx = 0;
  char names[GUEST_NUM][NAME_LEN];

  FILE *file;
  file = fopen(filename, "r");
  if (file == NULL)
    printf("FAIL: Could not open file.");

  bool known = false;
  char sign[5] = {[0 ... 4] = '\0'};
  int d_happy = 0;
  char line[500] = {[0 ... 499] = '\0'};

  char person1[NAME_LEN], person2[NAME_LEN];
  for (i = 0; i < NAME_LEN; i++)
    person1[i] = '\0', person2[i] = '\0';

  while (fgets(line, 100, file)) {
    sscanf(line, "%s would %s %d happiness units by sitting next to %s.\n",
           person1, sign, &d_happy, person2);

    // Remove full stop
    person2[strcspn(person2, ".")] = '\0';
    d_happy *= strcmp(sign, "gain") == 0 ? 1 : -1;

    known = false;
    for (i = 0; i < name_idx; i++) {
      if (strcmp(names[i], person1) == 0) {
        known = true;
        break;
      }
    }
    if (!known)
      strcpy(names[name_idx++], person1);

    known = false;
    for (j = 0; j < name_idx; j++)
      if (strcmp(names[j], person2) == 0) {
        known = true;
        break;
      }
    if (!known)
      strcpy(names[name_idx++], person2);

    immediate_cost_matrix[i][j] = d_happy;
  }
  fclose(file);

  /****************************************************************/
  /* Oh ... look at that I forgot to add myself to the guest list */
  /*   Let me quickly do that with 0 cost and see what changes    */
  /****************************************************************/
  // I know I've already set this in the caller ... but whatever
  for (i = 0; i < name_idx; i++) {
    immediate_cost_matrix[i][name_idx] = 0;
    immediate_cost_matrix[name_idx][i] = 0;
  }
  immediate_cost_matrix[name_idx][name_idx] = 0;
  return name_idx + 1;
}

void solve(char *filename) {
  int i = 0, j = 0, k = 0, cm[GUEST_NUM][GUEST_NUM];
  for (i = 0; i < GUEST_NUM; i++)
    for (j = 0; j < GUEST_NUM; j++)
      cm[i][j] = 0;
  int real_num_guests = populate_cost_matrix(filename, cm);

  // Seems like held-karp will work
  int arr_happiness = 0;
  int seated_subset = 0;
  int total_arrangements = 1 << real_num_guests;
  int seating_arr_cost[total_arrangements][real_num_guests];

  for (i = 0; i < total_arrangements; i++)
    for (j = 0; j < real_num_guests; j++)
      seating_arr_cost[i][j] = NEG_INF;
  seating_arr_cost[1][0] = 0; // Sit arbitrary person first

  for (i = 1; i < total_arrangements; i++) {
    for (j = 0; j < real_num_guests; j++) {
      if (!(i & (1 << j)))
        continue; // if person j is not seated, skip

      for (k = 0; k < real_num_guests; k++) {
        if (i & (1 << k))
          continue; // if person k is seated, skip

        if (seating_arr_cost[i][j] == NEG_INF)
          continue;

        seated_subset = i | (1 << k);
        arr_happiness = seating_arr_cost[i][j] + cm[j][k] + cm[k][j];

        if (arr_happiness > seating_arr_cost[seated_subset][k])
          seating_arr_cost[seated_subset][k] = arr_happiness;
      }
    }
  }

  int best = 0;
  int all_seated = total_arrangements - 1;
  for (j = 0; j < real_num_guests; j++) {
    seating_arr_cost[all_seated][j] += cm[0][j] + cm[j][0];
    best = seating_arr_cost[all_seated][j] > best
               ? seating_arr_cost[all_seated][j]
               : best;
  }

  printf("Optimal happiness: %d\n", best);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// Optimal happiness: 668
// Execution time: 0.000243



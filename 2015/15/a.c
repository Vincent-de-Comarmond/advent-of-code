#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>

static long num_recipies = 0;
void make_recipies(uint8_t remaining, uint8_t num_ingred, uint8_t idx,
                   uint8_t props[num_ingred], uint8_t recipies[(int)1e7]) {
  uint8_t i;
  if (idx == num_ingred - 1) {
    props[idx] = remaining;
    for (i = 0; i < num_ingred; i++)
      recipies[num_recipies++] = props[i];
  } else {
    for (i = 0; i <= remaining; ++i) {
      props[idx] = i;
      make_recipies(remaining - i, num_ingred, idx + 1, props, recipies);
    }
  }
}

void solve(char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL)
    printf("FAIL - could not open file.\n");

  int num_ingred = 0;
  int teaspoons = 100;
  char names[10][25] = {[0 ... 9] = {[0 ... 24] = '\0'}};
  int capacity[10] = {[0 ... 9] = 0};
  int durability[10] = {[0 ... 9] = 0};
  int flavor[10] = {[0 ... 9] = 0};
  int texture[10] = {[0 ... 9] = 0};
  int calories[10] = {[0 ... 9] = 0};
  char linebuf[1000] = {[0 ... 999] = '\0'};

  while (fgets(linebuf, 1000, file)) {
    sscanf(linebuf,
           "%s capacity %d, durability %d, flavor %d, texture %d, calories %d",
           names[num_ingred], &capacity[num_ingred], &durability[num_ingred],
           &flavor[num_ingred], &texture[num_ingred], &calories[num_ingred]);
    names[num_ingred][strcspn(names[num_ingred], ":")] = '\0';
    num_ingred++;
  }
  fclose(file);

  int i = 0, j = 0;

  uint8_t proportions[num_ingred];
  for (i = 0; i < num_ingred; i++)
    proportions[i] = 0;

  uint8_t all_recipies[(int)1e7];

  make_recipies((int8_t)teaspoons, (int8_t)num_ingred, (int8_t)0, proportions,
                all_recipies);
  /* printf("Number recipies: %ld\n", num_recipies); */

  long tmp = 1, best_unrestricted = 0, best_restricted = 0;
  int mult = 0, stats[5];
  for (i = 0; i < num_recipies; i += num_ingred) {

    for (j = 0; j < 5; j++)
      stats[j] = 0;

    for (j = 0; j < num_ingred; j++) {
      mult = all_recipies[i + j];
      stats[0] += mult * capacity[j];
      stats[1] += mult * durability[j];
      stats[2] += mult * flavor[j];
      stats[3] += mult * texture[j];
      stats[4] += mult * calories[j];
    }

    tmp = 1;
    for (j = 0; j < 4; j++)
      if (stats[j] <= 0) {
        tmp = 0;
        break;
      } else
        tmp *= stats[j];

    if (tmp > best_unrestricted)
      best_unrestricted = tmp;
    if (tmp > best_restricted && stats[4] == 500)
      best_restricted = tmp;
  }

  printf("Part 1 best score: %ld\n", best_unrestricted);
  printf("Part 2 best score: %ld\n", best_restricted);
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

// 2146993088 is too high for part 1
// 13882464 is the right answer for part 1
// 11171160 is the right answer for part 2
// Execution time: 0.008643 seconds

#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

const int weapon[5][3] = {
    {8, 4, 0}, {10, 5, 0}, {25, 6, 0}, {40, 7, 0}, {74, 8, 0}};

const int armor[6][3] = {{0, 0, 0},  {13, 0, 1}, {31, 0, 2},
                         {53, 0, 3}, {75, 0, 4}, {102, 0, 5}};

const int rings[8][3] = {{0, 0, 0},  {0, 0, 0},  {20, 0, 1}, {25, 1, 0},
                         {40, 0, 2}, {50, 2, 0}, {80, 0, 3}, {100, 3, 0}};

typedef struct Character {
  int hp;
  int atk;
  int def;
  int cost;
} character;

character *read_boss(char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    printf("FAILED - could not open file");
    exit(EXIT_FAILURE);
  }

  character *boss = malloc(sizeof(character));
  char buffer[100];
  char *attr, *value;

  while (fgets(buffer, 100, file)) {
    attr = strtok(buffer, ":");
    value = strtok(NULL, ":");

    if (strcmp(attr, "Hit Points") == 0)
      boss->hp = atoi(value);
    else if (strcmp(attr, "Damage") == 0)
      boss->atk = atoi(value);
    else if (strcmp(attr, "Armor") == 0)
      boss->def = atoi(value);
  }
  fclose(file);
  return boss;
}

bool iwin(character *me, character *boss) {

  int myhp = me->hp;
  int myeffect = me->atk - boss->def;
  myeffect = myeffect < 1 ? 1 : myeffect;

  int bosshp = boss->hp;
  int bosseffect = boss->atk - me->def;
  bosseffect = bosseffect < 1 ? 1 : bosseffect;

  int boss_turns_to_die = ceil((float)bosshp / (float)myeffect);
  int my_turns_to_die = ceil((float)myhp / (float)bosseffect);

  return boss_turns_to_die <= my_turns_to_die;
}

void solve(char *filename) {

  character me;
  me.hp = 100, me.cost = 0, me.atk = 0, me.def = 0;
  character *boss = read_boss(filename);

  int i, j, k, l, max_cost = -(int)1e9;
  /* int w = -1, a = -1, r1 = -1, r2 = -1; */

  for (i = 0; i < sizeof(weapon) / (3 * sizeof(int)); i++)
    for (j = 0; j < sizeof(armor) / (3 * sizeof(int)); j++)
      for (k = 0; k < sizeof(rings) / (3 * sizeof(int)); k++)
        for (l = 0; l < sizeof(rings) / (3 * sizeof(int)); l++) {
          if (l == k)
            continue;

          me.cost = weapon[i][0] + armor[j][0] + rings[k][0] + rings[l][0];
          me.atk = weapon[i][1] + armor[j][1] + rings[k][1] + rings[l][1];
          me.def = weapon[i][2] + armor[j][2] + rings[k][2] + rings[l][2];

          if (!iwin(&me, boss) && max_cost < me.cost) {
            max_cost = me.cost;
            /* w = i, a = j, r1 = k, r2 = l; */
          }
        }
  printf("Most expensive loss is: %d\n", max_cost);
  /* printf("Setup is %d, %d, %d, %d\n", w, a, r1, r2); */
  return;
}

int main(int argc, char *argv[]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// 158 is the correct answer
// Execution time: 0.000053 seconds

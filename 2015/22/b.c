#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define BUFFER_SIZE (int)1e6

static int BEST = INT_MAX; // global best for pruning
typedef enum {
  TURNS,
  MANA_USED,
  PLAYER_TURN,
  PLAYER_HP,
  PLAYER_MANA,
  BOSS_HP,
  BOSS_ATK,
  SHIELD_TURNS,
  POISON_TURNS,
  RECHARGE_TURNS,
  STATE_VEC_LENGTH
} StateVector;

const int INITIAL_VALUES[] = {
    [TURNS] = 0,         [MANA_USED] = 0,     [PLAYER_TURN] = 1,
    [PLAYER_HP] = 50,    [PLAYER_MANA] = 500, [BOSS_HP] = 55,
    [BOSS_ATK] = 8,      [SHIELD_TURNS] = 0,  [POISON_TURNS] = 0,
    [RECHARGE_TURNS] = 0};

/* Spells: {cost, immediate_damage}
   0: Magic Missile (53, 4)
   1: Drain         (73, 2) + heal 2
   2: Shield        (113, 0) -> armor +7 via shield timer
   3: Poison        (173, 3/turn for 6 turns)
   4: Recharge      (229, +101 mana/turn for 5 turns)
*/

typedef enum { PLAYER_WON, BOSS_WON, UNCONCLUDED } Result;
typedef enum { MMISSILE, DRAIN, SHIELD, POISON, RECHARGE } Action;
typedef enum { COST, DAMAGE, DURATION } ActionAttributes;
const int actions[5][3] = {
    {53, 4, 0},  // magic missile
    {73, 2, 0},  // drain
    {113, 0, 6}, // shield
    {173, 0, 6}, // poison (3 damage per-turn effect)
    {229, 0, 5}  // recharge
};

int turn(int num_current_states, int current_states[][STATE_VEC_LENGTH],
         int next_states[][STATE_VEC_LENGTH]) {

  int num_next = 0;
  memset(next_states, 0, BUFFER_SIZE * STATE_VEC_LENGTH * sizeof(int));

  for (int i = 0; i < num_current_states; i++) {

    // Skip if all states use more mana than the best
    // printf("Mana used: %d\n", current_states[i][MANA_USED]);
    if (BEST < current_states[i][MANA_USED])
      continue;

    int active_armor = 0;
    int state_copy[] = {[TURNS] = current_states[i][TURNS] + 1,
                        [MANA_USED] = current_states[i][MANA_USED],
                        [PLAYER_TURN] =
                            (1 + current_states[i][PLAYER_TURN]) % 2,
                        [PLAYER_HP] = current_states[i][PLAYER_HP],
                        [PLAYER_MANA] = current_states[i][PLAYER_MANA],
                        [BOSS_HP] = current_states[i][BOSS_HP],
                        [BOSS_ATK] = current_states[i][BOSS_ATK],
                        [SHIELD_TURNS] = current_states[i][SHIELD_TURNS],
                        [POISON_TURNS] = current_states[i][POISON_TURNS],
                        [RECHARGE_TURNS] = current_states[i][RECHARGE_TURNS]};

    if (state_copy[PLAYER_TURN] == 0) {
      if (state_copy[PLAYER_HP] < 2)
        continue;
      state_copy[PLAYER_HP]--;
    }

    /*
    for (int j = 0; j < STATE_VEC_LENGTH; j++) {
      printf("current_states[%d][%d]: %d\n", i, j, current_states[i][j]);
    }
    */

    // Effects are active at the start of each turn.
    if (0 < state_copy[SHIELD_TURNS])
      active_armor = 7;
    if (0 < state_copy[POISON_TURNS])
      state_copy[BOSS_HP] -= 3;
    if (0 < state_copy[RECHARGE_TURNS])
      state_copy[PLAYER_MANA] += 101;

    state_copy[SHIELD_TURNS] = MAX(0, state_copy[SHIELD_TURNS] - 1);
    state_copy[POISON_TURNS] = MAX(0, state_copy[POISON_TURNS] - 1);
    state_copy[RECHARGE_TURNS] = MAX(0, state_copy[RECHARGE_TURNS] - 1);

    if (state_copy[BOSS_HP] <= 0) {
      BEST = MIN(state_copy[MANA_USED], BEST);
      continue;
    }

    // Remember, we've already switched whose turn it is
    if (state_copy[PLAYER_TURN] == 1) {
      // printf("BOSSES TURN\n");
      state_copy[PLAYER_HP] -= (state_copy[BOSS_ATK] - active_armor);
      // Player has died ... no point continuing on this branch
      if (state_copy[PLAYER_HP] <= 0)
        continue;
      // Else
      for (int j = 0; j < STATE_VEC_LENGTH; j++) {
        next_states[num_next][j] = state_copy[j];
      }
      num_next++;
    } else {
      // printf("PLAYERS TURN\n");

      int mana = state_copy[PLAYER_MANA];

      if (actions[MMISSILE][COST] <= mana) {
        // Won ... no point continuing
        if (state_copy[BOSS_HP] <= actions[MMISSILE][DAMAGE]) {
          BEST = MIN(BEST, state_copy[MANA_USED] + actions[MMISSILE][COST]);
        } else {
          for (int j = 0; j < STATE_VEC_LENGTH; j++) {
            next_states[num_next][j] = state_copy[j];
          }
          next_states[num_next][MANA_USED] += actions[MMISSILE][COST];
          next_states[num_next][PLAYER_MANA] -= actions[MMISSILE][COST];
          next_states[num_next][BOSS_HP] -= actions[MMISSILE][DAMAGE];
          num_next++;
        }
      }

      if (actions[DRAIN][COST] <= mana) {

        if (state_copy[BOSS_HP] <= actions[DRAIN][DAMAGE]) {
          BEST = MIN(BEST, state_copy[MANA_USED] + actions[DRAIN][COST]);
        } else {
          for (int j = 0; j < STATE_VEC_LENGTH; j++) {
            next_states[num_next][j] = state_copy[j];
          }
          next_states[num_next][MANA_USED] += actions[DRAIN][COST];
          next_states[num_next][PLAYER_MANA] -= actions[DRAIN][COST];
          next_states[num_next][BOSS_HP] -= actions[DRAIN][DAMAGE];
          next_states[num_next][PLAYER_HP] += actions[DRAIN][DAMAGE];
          num_next++;
        }
      }

      if ((actions[SHIELD][COST] <= mana) & (state_copy[SHIELD_TURNS] == 0)) {

        for (int j = 0; j < STATE_VEC_LENGTH; j++) {
          next_states[num_next][j] = state_copy[j];
        }
        next_states[num_next][SHIELD_TURNS] = actions[SHIELD][DURATION];
        next_states[num_next][MANA_USED] += actions[SHIELD][COST];
        next_states[num_next][PLAYER_MANA] -= actions[SHIELD][COST];
        num_next++;
      }

      if ((actions[POISON][COST] <= mana) & (state_copy[POISON_TURNS] == 0)) {

        for (int j = 0; j < STATE_VEC_LENGTH; j++) {
          next_states[num_next][j] = state_copy[j];
        }
        next_states[num_next][POISON_TURNS] = actions[POISON][DURATION];
        next_states[num_next][MANA_USED] += actions[POISON][COST];
        next_states[num_next][PLAYER_MANA] -= actions[POISON][COST];
        num_next++;
      }

      if ((actions[RECHARGE][COST] <= mana) &
          (state_copy[RECHARGE_TURNS] == 0)) {

        for (int j = 0; j < STATE_VEC_LENGTH; j++) {
          next_states[num_next][j] = state_copy[j];
        }
        next_states[num_next][RECHARGE_TURNS] = actions[RECHARGE][DURATION];
        next_states[num_next][MANA_USED] += actions[RECHARGE][COST];
        next_states[num_next][PLAYER_MANA] -= actions[RECHARGE][COST];
        num_next++;
      }
    }
  }
  return num_next;
};

int solve() {
  int(*states_1)[STATE_VEC_LENGTH] = calloc(BUFFER_SIZE, sizeof(*states_1));
  int(*states_2)[STATE_VEC_LENGTH] = calloc(BUFFER_SIZE, sizeof(*states_2));

  for (int i = 0; i < STATE_VEC_LENGTH; i++) {
    states_1[0][i] = INITIAL_VALUES[i];
    // printf("INITIAL_VALUES[%d]: %d\n", i, INITIAL_VALUES[i]);
  }

  int generation = 0;
  int num_states = 1;
  int max_states = 0;

  while (0 < num_states) {
    generation++;
    max_states = MAX(max_states, num_states);

    /*
    printf("----------------------------\n");
    printf("Number of states: %d\n", num_states);
    printf("Generation: %d\n", generation);
    */

    if (generation % 2 == 1) {
      num_states = turn(num_states, states_1, states_2);
    } else {
      num_states = turn(num_states, states_2, states_1);
    }
  }
  // printf("Max states: %d\n", max_states);

  free(states_1);
  free(states_2);

  return BEST;
};

int main(int argc, char *argv[]) {
  time_t start, end;

  start = clock();
  printf("Least mana victory is: %d\n", solve());
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// 1020 is too low
// 1289 is the correct answer for day 22
// Execution time is 0.102 seconds

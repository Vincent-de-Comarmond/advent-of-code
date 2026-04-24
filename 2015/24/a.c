#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BUFFER_SIZE (int)1e5
static uint PRESENTS[BUFFER_SIZE];
static uint NUM_PRESENTS = 0;

uint read_input(char *filename) {
  uint presents = 0;
  char linebuf[100];
  FILE *file = fopen(filename, "r");

  while (fgets(linebuf, 100, file))
    PRESENTS[presents++] = atoi(linebuf);

  fclose(file);
  return presents;
}

uint sum_array(uint num_opts, uint numbers[num_opts]) {
  uint i, total = 0;
  for (i = 0; i < num_opts; i++)
    total += numbers[i];
  return total;
}

uint int_sqrt(uint input) {
  uint power = 0, copy = input;
  while (1 < copy) {
    copy >>= 1;
    power++;
  }
  return power;
}

uint bit_count(uint input) {
  uint count = 0;
  while (0 < input) {
    input &= (input - 1);
    count++;
  }
  return count;
}

int bitsum_comparitor(const void *a, const void *b) {
  return bit_count(*(uint *)a) - bit_count(*(uint *)b);
}

void reconstruct(uint bitmask, uint num_presents, uint *numbers) {
  uint i;
  for (i = 0; i < num_presents; i++)
    if (((1 << i) & bitmask) != 0)
      printf("%d ", numbers[i]);
}

ulong quantum_entanglement(uint bitmask, uint num_presents, uint *numbers) {
  uint i;
  ulong qe = 1;
  for (i = 0; i < num_presents; i++)
    if (((1 << i) & bitmask) != 0)
      qe *= numbers[i];
  return qe;
}

uint make_valid_groups(uint num_presents, uint *inputs, uint *outputs) {
  uint target = sum_array(num_presents, inputs) / 3;
  uint i, combos = (uint)powl(2, num_presents);
  uint *all_stacks = calloc(combos, sizeof(uint));
  uint num_valid = 0;

  for (i = 0; i < num_presents; i++)
    all_stacks[1 << i] = inputs[i];

  printf("Target: %d\n", target);
  uint report = (uint)5e7;
  for (i = 0; i < combos; i++) {

    if (i % report == 0)
      printf("Testing combination: %.2f complete\n",
             ((float)i / (float)combos));

    int lead = 1 << int_sqrt(i);
    int rest = ~lead;
    all_stacks[i] = all_stacks[i & lead] + all_stacks[i & rest];

    if (all_stacks[i] == target)
      outputs[num_valid++] = i;
  }
  free(all_stacks);
  return num_valid;
}

uint extract_compact_groups(uint num_valids, uint *groups,
                            uint *compact_groups) {
  uint i, grp_size, min_grp_size = UINT_MAX;

  for (i = 0; i < num_valids; i++) {
    grp_size = bit_count(groups[i]);
    min_grp_size = (grp_size < min_grp_size) ? grp_size : min_grp_size;
  }

  uint minimal_present_groups = 0;
  for (i = 0; i < num_valids; i++)
    if (bit_count(groups[i]) == min_grp_size)
      compact_groups[minimal_present_groups++] = groups[i];
  return minimal_present_groups;
}

uint extract_least_ent_groups(uint num_presents, uint *present_weights,
                              uint num_lightest_grps, uint *light_groups,
                              uint *best_groups) {
  uint i;
  ulong grp_entropy, least_entropy = ULONG_MAX;

  for (i = 0; i < num_lightest_grps; i++) {
    grp_entropy =
        quantum_entanglement(light_groups[i], num_presents, present_weights);
    least_entropy = grp_entropy < least_entropy ? grp_entropy : least_entropy;
  }

  uint num_final_groups = 0;
  for (i = 0; i < num_lightest_grps; i++)
    if (quantum_entanglement(light_groups[i], num_presents, present_weights) ==
        least_entropy)
      best_groups[num_final_groups++] = light_groups[i];
  return num_final_groups;
}

uint extract_orthogonal(uint value, uint *input_groups, uint num_input,
                        uint *output_groups) {
  uint i, num_groups = 0;
  for (i = 0; i < num_input; i++)
    if ((value & input_groups[i]) == 0)
      output_groups[num_groups++] = input_groups[i];

  return num_groups;
}

int solve(char *filename) {
  // Phase 0 readin input
  NUM_PRESENTS = read_input(filename);
  // Phase 1 determining all possible valid groups
  uint puzzle_size = (uint)powl(2, NUM_PRESENTS);
  uint *valid_groups = calloc(puzzle_size, sizeof(uint));
  uint num_valid_groups =
      make_valid_groups(NUM_PRESENTS, PRESENTS, valid_groups);

  // Phase 3 determining lightest groups
  uint *light_groups = calloc(num_valid_groups, sizeof(uint));
  uint num_light_groups =
      extract_compact_groups(num_valid_groups, valid_groups, light_groups);

  // Phase 4 getting least entropy groups
  uint *le_groups = calloc(num_light_groups, sizeof(uint));
  uint num_least_entanglement = extract_least_ent_groups(
      NUM_PRESENTS, PRESENTS, num_light_groups, light_groups, le_groups);
  // Solution with least entanglement exists
  uint i, j, num_orth1, num_orth2;
  uint ortho_groups1[num_valid_groups];
  uint ortho_groups2[num_valid_groups];
  for (i = 0; i < num_least_entanglement; i++) {
    memset(ortho_groups1, 0, sizeof(ortho_groups1));
    memset(ortho_groups2, 0, sizeof(ortho_groups2));

    num_orth1 = extract_orthogonal(le_groups[i], valid_groups, num_valid_groups,
                                   ortho_groups1);
    for (j = 0; j < num_orth1; j++) {
      num_orth2 = extract_orthogonal(ortho_groups1[j], ortho_groups1, num_orth1,
                                     ortho_groups2);
      if (0 < num_orth2) {
        printf("Minimal quantum entanglement: %lu\n",
               quantum_entanglement(le_groups[i], NUM_PRESENTS, PRESENTS));
        return EXIT_SUCCESS;
      }
    }
  }
  return EXIT_FAILURE;
}

int main(int argc, char *argv[argc]) {
  clock_t start, end;
  start = clock();
  int status = solve(argv[1]);
  end = clock();
  printf("Execution time was: %ld s\n", (end - start) / CLOCKS_PER_SEC);
  return status;
}

// 3311502079 is too low
// 364088754943 is too high (relaxing unsigned int to unsigned long)

// 10723906903 is the right answer
// Execution time is 6 seconds

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define WIDTH 550
#define MAX_CHOP 10
#define NUM_TRANS 50
#define ELEMENT_LEN 3
#define TRANSFORM_MAX_SIZE 20
#define MAX_PER_GEN (int)1e7

static int num_elements = 0;
static char elements[NUM_TRANS][ELEMENT_LEN] = {
    [0 ... NUM_TRANS - 1] = {[0 ... 2] = '\0'}};

static int transform_nums[NUM_TRANS] = {[0 ... NUM_TRANS - 1] = 0};
static char transforms[NUM_TRANS][MAX_CHOP][MAX_CHOP] = {
    [0 ... NUM_TRANS -
     1] = {[0 ... MAX_CHOP - 1] = {[0 ... MAX_CHOP - 1] = '\0'}}};

static int syn_len;
static char synthesis[WIDTH];

int regsiter_and_chop(char *input_str, char split[MAX_CHOP]) {
  int idx = 0;
  char minibuf[3];
  bool found = false;

  for (int j = 0; j < strlen(input_str); j++) {
    minibuf[0] = '\0', minibuf[1] = '\0', minibuf[2] = '\0';
    if (input_str[j] == 'e' && input_str[j + 1] == '\0')
      minibuf[0] = 'e';
    else if ('A' <= input_str[j] && input_str[j] <= 'Z') {
      minibuf[0] = input_str[j];
      if ('a' <= input_str[j + 1] && input_str[j + 1] <= 'z') {
        minibuf[1] = input_str[j + 1];
        j++;
      }
    }

    found = false;
    for (int i = 0; i < num_elements; i++)
      if (strcmp(minibuf, elements[i]) == 0) {
        split[idx++] = 'a' + i;
        found = true;
        break;
      }
    if (!found) {
      split[idx++] = 'a' + num_elements;
      strcpy(elements[num_elements], minibuf);
      num_elements++;
    }
  }
  return idx;
}

void print_debug_info() {
  printf("Dictionary:\n");
  for (int i = 0; i < num_elements; i++) {
    printf("%d: %s <-> %c\n", i, elements[i], 'a' + i);
  }

  printf("Transformations:\n");
  for (int i = 0; i < NUM_TRANS; i++) {
    if (transform_nums[i] == 0)
      continue;
    printf("%c:\n[ ", 'a' + i);
    for (int j = 0; j < transform_nums[i]; j++) {
      printf("%s", transforms[i][j]);
      if (j != transform_nums[i] - 1)
        printf(", ");
      else
        printf(" ]\n");
    }
  }
  printf("Hello\n");
  printf("Redefined Target: %s\n", synthesis);
}

void redefine_problem(char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL)
    printf("FAILED - could not open file");

  bool istarg = false;
  char buffer[WIDTH];

  while (fgets(buffer, WIDTH, file)) {
    buffer[strcspn(buffer, "\n")] = 0;

    if (strlen(buffer) == 0) {
      istarg = true;
      continue;
    }

    if (istarg) {
      syn_len = regsiter_and_chop(buffer, synthesis);
    } else {
      char source[2] = {'\0', '\0'};
      regsiter_and_chop(strtok(buffer, " => "), source);

      char dest[10] = {[0 ... 9] = '\0'};
      regsiter_and_chop(strtok(NULL, " => "), dest);

      int offset = source[0] - 'a';
      strcpy(transforms[offset][transform_nums[offset]], dest);
      transform_nums[offset]++;
    }
  }
  fclose(file);
  /* print_debug_info(); */
}

int solve_recursive(int num_gen, int num_in, char inputs[MAX_PER_GEN][syn_len],
                    char outputs[MAX_PER_GEN][syn_len]) {

  int i, j, k, l;
  char(*tmp)[syn_len] = malloc(sizeof(char[MAX_PER_GEN][syn_len]));
  for (i = 0; i < MAX_PER_GEN; i++)
    for (j = 0; j < syn_len; j++) {
      tmp[i][j] = '\0';
      outputs[i][j] = '\0';
    }

  int num_out = 0, dup_num_out = 0, idx = 0;
  for (i = 0; i < num_in; i++) {
    for (j = 0; j < strlen(inputs[i]); j++) {

      int offset = inputs[i][j] - 'a';

      for (k = 0; k < transform_nums[offset]; k++) {
        idx = 0;
        for (l = 0; l < j; l++)
          tmp[dup_num_out][idx++] = inputs[i][j];

        for (l = 0; l < strlen(transforms[offset][k]); l++)
          tmp[dup_num_out][idx++] = transforms[offset][k][l];

        for (l = j + 1; l < strlen(inputs[i]); l++)
          tmp[dup_num_out][idx++] = inputs[i][l];

        if (strcmp(synthesis, tmp[dup_num_out]) == 0)
          return num_gen;
        dup_num_out++;
      }
    }
  }

  bool found = false;
  for (i = 0; i < dup_num_out; i++) {
    found = false;
    for (j = 0; j < num_out; j++) {
      if (strcmp(tmp[i], tmp[j]) == 0) {
        found = true;
        break;
      }
    }
    if (!found) {
      strcpy(outputs[num_out], tmp[i]);
      num_out++;
    }
  }
  free(tmp);

  int max_len = 0, len_;
  for (i = 0; i < num_out; i++) {
    len_ = strlen(outputs[i]);
    max_len = len_ > max_len ? len_ : max_len;
    /* printf("%s\n", outputs[i]); */
  }

  printf("Generation: %d\n", num_gen);
  printf("Number outputs: %d\n", num_out);
  printf("Target length: %d\n", syn_len);
  printf("Max length: %d\n\n", max_len);

  return solve_recursive(num_gen + 1, num_out, outputs, inputs);
}

void solve(char *filename) {
  redefine_problem(filename);
  int i, j;
  char start;
  for (i = 0; i < num_elements; i++)
    if (strcmp(elements[i], "e") == 0) {
      start = i;
      break;
    }

  char(*in)[syn_len] = malloc(sizeof(char[MAX_PER_GEN][syn_len]));
  char(*out)[syn_len] = malloc(sizeof(char[MAX_PER_GEN][syn_len]));

  for (i = 0; i < MAX_PER_GEN; i++)
    for (j = 0; j < syn_len; j++)
      in[i][j] = '\0';
  in[0][0] = 'a' + start;

  // Start counting generations from 1
  solve_recursive(1, 1, in, out);
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

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

static int num_elements = 0;
static char elements[NUM_TRANS][ELEMENT_LEN] = {
    [0 ... NUM_TRANS - 1] = {[0 ... 2] = '\0'}};

static int transform_nums[NUM_TRANS] = {[0 ... NUM_TRANS - 1] = 0};
static char transforms[NUM_TRANS][MAX_CHOP][MAX_CHOP] = {
    [0 ... NUM_TRANS -
     1] = {[0 ... MAX_CHOP - 1] = {[0 ... MAX_CHOP - 1] = '\0'}}};

static char synthesis[WIDTH];

struct TransmutationStruct {
  char element;
  int num_output;
  char outputs[10][10];
};

typedef struct TransmutationStruct Transmuation;

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

  printf("Redefined Target:\n%s", synthesis);
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

    if (istarg)
      regsiter_and_chop(buffer, synthesis);
    else {
      char source[2] = {'\0', '\0'};
      regsiter_and_chop(strtok(buffer, " => "), source);

      char dest[10] = {[0 ... 9] = '\0'};
      int dest_size = regsiter_and_chop(strtok(NULL, " => "), dest);

      int offset = source[0] - 'a';
      strcpy(transforms[offset][transform_nums[offset]], dest);
      transform_nums[offset]++;
    }
  }
  fclose(file);

  print_debug_info();
}

int main(int argc, char *argv[argc]) {
  time_t start, end;

  start = clock();
  redefine_problem(argv[1]);
  end = clock();

  printf("Execution time: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
}

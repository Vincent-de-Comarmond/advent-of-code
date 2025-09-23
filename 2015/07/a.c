#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

bool set_elements[700] = {false};
uint16_t known_elements[700] = {0};

enum BitwiseOperation {
  AND = 1,
  LSHIFT = 2,
  NOT = 3,
  OR = 4,
  RSHIFT = 5,
  ASSIGN = 6
};

int determine_operation(char *line) {
  return strstr(line, "AND") != NULL      ? AND
         : strstr(line, "LSHIFT") != NULL ? LSHIFT
         : strstr(line, "NOT") != NULL    ? NOT
         : strstr(line, "OR") != NULL     ? OR
         : strstr(line, "RSHIFT") != NULL ? RSHIFT
                                          : ASSIGN;
}

struct Equation {
  enum BitwiseOperation operation;
  char left[4];
  char right[4];
  char output[4];
};

int cheap_hash(char *input_string) {
  int idx = 0, total = 0, multiplier = 1;

  while (input_string[idx] != '\0') {
    total += ((int)input_string[idx++] - 96) * multiplier;
    multiplier *= 26;
  }
  return total;
}

char *unhash(int hashed) {
  int idx = 0, letter_val = 0;
  char *result = malloc(10 * sizeof(char));

  if (!result)
    return NULL;

  while (hashed > 0) {
    letter_val = hashed % 26;
    letter_val = letter_val == 0 ? 26 : letter_val;
    result[idx++] = (char)(letter_val + 96);
    hashed = (hashed - letter_val) / 26;
    if (hashed == 0)
      break;
  }
  result[idx] = '\0';
  return result;
}

bool is_numeric(const char *str) {
  if (str == NULL || *str == '\0') {
    return false; // Empty or NULL string is not considered numeric
  }
  while (*str != '\0') {
    if (!isdigit((unsigned char)*str)) {
      return false; // Found a non-digit character
    }
    str++;
  }
  return true; // All characters are digits
}

void solve_recursive(struct Equation *equation_buffer, int num_equations) {
  int unknown_idx = 0, eq_idx = 0;
  struct Equation equations[400];
  int hashleft = 0, hashright = 0, hashoutput = 0;

  for (eq_idx = 0; eq_idx < num_equations; eq_idx++) {
    struct Equation eq = equation_buffer[eq_idx];

    hashleft = cheap_hash(eq.left);
    hashright = cheap_hash(eq.right);
    hashoutput = cheap_hash(eq.output);

    bool binary_solvable = false;
    uint16_t leftnumeric =
        is_numeric(eq.left) ? atoi(eq.left) : known_elements[hashleft];
    uint16_t rightnumeric =
        is_numeric(eq.right) ? atoi(eq.right) : known_elements[hashright];

    if ((is_numeric(eq.left) || set_elements[hashleft]) &&
        (is_numeric(eq.right) || set_elements[hashright])) {
      binary_solvable = true;
    }

    switch (eq.operation) {
    case ASSIGN: {
      if (is_numeric(eq.left) || set_elements[hashleft]) {
        known_elements[hashoutput] = leftnumeric;
        set_elements[hashoutput] = true;
      } else {
        equations[unknown_idx++] = equation_buffer[eq_idx];
      }
      break;
    }
    case NOT: {
      if (is_numeric(eq.left) || set_elements[hashleft]) {
        known_elements[hashoutput] = ~leftnumeric;
        set_elements[hashoutput] = true;
      } else {
        equations[unknown_idx++] = equation_buffer[eq_idx];
      }
      break;
    }
    case AND: {
      if (binary_solvable) {
        known_elements[hashoutput] = leftnumeric & rightnumeric;
        set_elements[hashoutput] = true;
      } else {
        equations[unknown_idx++] = equation_buffer[eq_idx];
      }
      break;
    }
    case LSHIFT: {
      if (binary_solvable) {
        known_elements[hashoutput] = leftnumeric << rightnumeric;
        set_elements[hashoutput] = true;
      } else {
        equations[unknown_idx++] = equation_buffer[eq_idx];
      }
      break;
    }
    case OR: {
      if (binary_solvable) {
        known_elements[hashoutput] = leftnumeric | rightnumeric;
        set_elements[hashoutput] = true;
      } else {
        equations[unknown_idx++] = equation_buffer[eq_idx];
      }
      break;
    }
    case RSHIFT: {
      if (binary_solvable) {
        known_elements[hashoutput] = leftnumeric >> rightnumeric;
        set_elements[hashoutput] = true;
      } else {
        equations[unknown_idx++] = equation_buffer[eq_idx];
      }
      break;
    }
    };
  }
  if (unknown_idx > 0) {
    solve_recursive(equations, unknown_idx);
  }
}

void solve(char *filename) {

  int i = 0;
  for (i = 0; i < 26 * 26; i++) {
    known_elements[i] = 0;
  }

  FILE *file = fopen(filename, "r");
  int buf_size = 200;
  char line[buf_size];

  int equation_idx = 0;
  enum BitwiseOperation operation = 0;
  struct Equation equations[400];

  while (fgets(line, buf_size, file)) {

    operation = determine_operation(line);
    switch (operation) {
    case AND: {
      struct Equation eq = {.operation = AND};
      sscanf(line, "%s AND %s -> %s", eq.left, eq.right, eq.output);
      equations[equation_idx++] = eq;
      break;
    }
    case LSHIFT: {
      struct Equation eq = {.operation = LSHIFT};
      sscanf(line, "%s LSHIFT %s -> %s", eq.left, eq.right, eq.output);
      equations[equation_idx++] = eq;
      break;
    }
    case NOT: {
      struct Equation eq = {.operation = NOT};
      sscanf(line, "NOT %s -> %s", eq.left, eq.output);

      if (!is_numeric(eq.left)) {
        equations[equation_idx++] = eq;
      } else {
        known_elements[cheap_hash(eq.output)] = ~(uint16_t)atoi(eq.left);
        set_elements[cheap_hash(eq.output)] = true;
      }
      break;
    }
    case OR: {
      struct Equation eq = {.operation = OR};
      sscanf(line, "%s OR %s -> %s", eq.left, eq.right, eq.output);
      equations[equation_idx++] = eq;
      break;
    }
    case RSHIFT: {
      struct Equation eq = {.operation = RSHIFT};
      sscanf(line, "%s RSHIFT %s -> %s", eq.left, eq.right, eq.output);
      equations[equation_idx++] = eq;
      break;
    }
    case ASSIGN: {
      struct Equation eq = {.operation = ASSIGN};
      sscanf(line, "%s -> %s", eq.left, eq.output);
      if (!is_numeric(eq.left)) {
        equations[equation_idx++] = eq;
      } else {
        known_elements[cheap_hash(eq.output)] = (uint16_t)atoi(eq.left);
        set_elements[cheap_hash(eq.output)] = true;
      }
      break;
    }
    }
  }
  fclose(file);
  solve_recursive(equations, equation_idx);
  /* print_dump(); */
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  solve(argv[1]);
  printf("a = %d\n", known_elements[cheap_hash("a")]);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 3840 is too high for wire a for part 1
// 956 is the right answer for part 1
// runs in 0.0017

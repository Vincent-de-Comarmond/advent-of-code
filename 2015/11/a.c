#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char valid_letters[24] = {'\0', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
                          'h',  'j', 'k', 'm', 'n', 'p', 'q', 'r',
                          's',  't', 'u', 'v', 'w', 'x', 'y', 'z'};

long pow23(int exponent) {
  long total = 1;
  for (int i = 0; i < exponent; i++)
    total *= 23;
  return total;
}

long to_numeric(char *password) {
  int i, j;
  long numeric_password = 0;
  int length = strlen(password);

  // We are working with a restricted 23 character alphabet ... so adjust
  for (i = 0; i < length; i++) {
    j = password[i] - 'a' + 1;
    j = j >= 15 ? j - 3 : j >= 12 ? j - 2 : j >= 9 ? j - 1 : j;
    numeric_password += pow23(length - i - 1) * j;
  }
  return numeric_password;
}

char *to_string(long numeric_value) {
  int char_val = 0, idx = 0;
  long value = numeric_value;
  char reversed_string[20] = {[0 ... 19] = '\0'};

  while (value > 0) {
    char_val = value % 23;
    char_val = char_val == 0 ? 23 : char_val;
    reversed_string[idx++] = valid_letters[char_val];
    value = (value - char_val) / 23;
  }

  char *string = malloc(20 * sizeof(char));
  int length = strlen(reversed_string);
  for (int idx = 0; idx < length; idx++)
    string[idx] = reversed_string[length - 1 - idx];
  string[length] = '\0';
  return string;
}

bool passes_condition_1(long numeric_password) {
  // Condition 1 translates to x+2 = x%23 +1= x%(23*23) having the same numeric
  // value and not including the missing i, l, o
  long value = numeric_password, og_value;
  int char_val = 0;
  char a, b, c;

  while (value > 0) {
    char_val = value % 23 == 0 ? 23 : value % 23;
    og_value = value - char_val;
    a = valid_letters[char_val];

    value = (value - char_val) / 23;
    if (value <= 0)
      break;

    char_val = value % 23 == 0 ? 23 : value % 23;
    b = valid_letters[char_val];

    value = (value - char_val) / 23;
    if (value <= 0)
      break;

    char_val = value % 23 == 0 ? 23 : value % 23;
    c = valid_letters[char_val];

    /* printf("%c, %c, %c\n", c, b, a); */
    if (b - c == 1 && a - b == 1)
      return true;

    value = og_value / 23;
  }
  return false;
}

bool passes_condition_3(long numeric_password) {
  // Condition 3 translates to x%23  = x%(23*23) for two places with no overlap

  char seen[20] = {[0 ... 19] = '\0'};
  int seen_idx = 0, char_val_1 = 0, char_val_2;
  long value = numeric_password;

  while (value > 0) {
    char_val_1 = value % 23;
    char_val_1 = char_val_1 == 0 ? 23 : char_val_1;
    value = (value - char_val_1) / 23;
    if (value <= 0)
      break;

    char_val_2 = value % 23;
    char_val_2 = char_val_2 == 0 ? 23 : char_val_2;

    if (char_val_1 == char_val_2) {
      value = (value - char_val_2) / 23;
      seen[seen_idx++] = char_val_1;

      // The two pairs must be different
      for (int i = 0; i < seen_idx - 1; i++) {
        if (seen[i] != char_val_1) {
          return true;
        }
      }
    }
  }
  return false;
}

void solve(char *password) {
  bool part1_solved = false;
  long numeric_password = to_numeric(password);
  numeric_password++; // old one has expired
  long calls = 0;
  printf("Numeric Password: %ld\n", numeric_password);

  while (calls < 1e12) {

    if (passes_condition_1(numeric_password) &&
        passes_condition_3(numeric_password)) {
      if (part1_solved) {
        char *part2_soln = to_string(numeric_password);
        printf("Soltuion to part 2 is: %s\n", part2_soln);
        free(part2_soln);
        break;
      } else {
        char *part1_soln = to_string(numeric_password);
        printf("Soltuion to part 1 is: %s\n", part1_soln);
        free(part1_soln);
        part1_solved = true;
      }
    }
    calls++;
    numeric_password++;
  }
  if (calls == 1e12) {
    printf("FAILED\n");
  }
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  solve(argv[1]);
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n\n\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// Apparently heqqqqrs is not the right answer ???
// Apparently heqqnpqq is also wrong (this is what you get if you say n is next
// to p rather than o)

// hepxxyzz is the right answer (I was mis-reading condition 3)
// Execution time: 0.014595 seconds

// heqaabcc is the right answer for part 2
// Execution time: 0.036561 seconds

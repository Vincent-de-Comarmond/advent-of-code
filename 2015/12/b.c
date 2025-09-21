#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/// Constant string representing the word `"red"` with a preceding colon.
/// Used to detect the presence of `"red"` in JSON-like objects.
const char red[7] = {':', '"', 'r', 'e', 'd', '"', '\0'};

/**
 * @brief Moves the file pointer back by one byte.
 *
 * This is used after reading ahead when parsing numbers or characters,
 * allowing the previous character to be re-read in subsequent operations.
 *
 * @param fp A pointer to an open file stream.
 */
void reverse_file_pointer_pos(FILE *fp) { fseek(fp, -1L, SEEK_CUR); }

/**
 * @brief Implements a circular shift in a 7-character buffer.
 *
 * Shifts all characters in the buffer one position to the left and
 * inserts a new character at the end. Used to track a rolling window
 * of characters for detecting specific patterns like `":red"`.
 *
 * @param str_buffer A fixed-size character array of length 7.
 * @param push_char The new character to insert at the end.
 */
void circle_buffer(char str_buffer[7], char push_char) {
  for (int idx = 0; idx < 5; idx++)
    str_buffer[idx] = str_buffer[idx + 1];
  str_buffer[5] = push_char;
}

/**
 * @brief Parses a number (integer) from a file stream.
 *
 * Reads characters from the file as long as they form a valid integer,
 * which may include a leading negative sign (`-`).
 * Once a non-numeric character is encountered, the file pointer is
 * reversed by one position to not lose track of it.
 *
 * @param file A pointer to an open file stream.
 * @param starting_char The first character that is already read, known to be
 *                      either '-' or a digit.
 *
 * @return The parsed integer as an `int`.
 */
int pass_number(FILE *file, char starting_char) {
  int idx = 0;
  char char_val = starting_char;
  char num_buffer[20] = {[0 ... 19] = '\0'};

  while (char_val == '-' || ('0' <= char_val && char_val <= '9')) {
    num_buffer[idx++] = char_val;
    char_val = fgetc(file);
  }
  reverse_file_pointer_pos(file);
  return atoi(num_buffer);
}

/**
 * @brief Recursively parses a JSON-like dictionary and computes the sum of its
 * numbers.
 *
 * This function handles nested JSON objects. If any object contains the
 * key-value pair with the value `"red"`, the entire object is treated as having
 * a value of 0.
 *
 * @param file A pointer to an open file stream positioned at the start of a
 * dictionary.
 * @param is_zero A flag indicating whether the current object should be ignored
 * (value 0).
 *
 * @return The computed sum as a `long`. Returns 0 if the current dictionary is
 * ignored.
 */
long pass_dictionary(FILE *file, bool is_zero) {
  long total = 0;
  int char_val = '{';
  char str_buffer[7] = {[0 ... 6] = '\0'};

  while (char_val != EOF && char_val != '}') {
    char_val = fgetc(file);

    // Recursively process nested dictionaries
    if (char_val == '{')
      total += pass_dictionary(file, is_zero);

    if (is_zero)
      continue;

    circle_buffer(str_buffer, char_val);

    // If ":red" is detected, mark this dictionary to be ignored
    if (strcmp(red, str_buffer) == 0) {
      is_zero = true;
      continue;
    }

    // If a number is found, add it to the total
    if (char_val == '-' || ('0' <= char_val && char_val <= '9'))
      total += pass_number(file, char_val);
  }

  return is_zero ? 0 : total;
}

/**
 * @brief Computes the total sum of numbers in a JSON-like file.
 *
 * Opens the given file and iterates through it, summing up all numbers.
 * JSON objects are handled recursively. Any dictionary containing the string
 * `"red"` is completely ignored (sum of that dictionary is treated as 0).
 *
 * @param filename The path to the file to read.
 *
 * @return The total sum as a `long`. Returns `EXIT_SUCCESS` (0) if the file
 * cannot be opened.
 */
long sum(char *filename) {
  int char_val = 0;
  long total = 0;
  FILE *file = fopen(filename, "r");

  if (file == NULL) {
    return EXIT_SUCCESS;
  }

  while (char_val != EOF) {
    char_val = fgetc(file);

    if (char_val == '{')
      total += pass_dictionary(file, false);

    if (char_val == '-' || ('0' <= char_val && char_val <= '9'))
      total += pass_number(file, char_val);
  }

  fclose(file);
  return total;
}

/**
 * @brief Entry point of the program.
 *
 * This function:
 * 1. Reads a JSON-like file from the command-line argument.
 * 2. Computes the total sum of numbers, skipping objects containing `"red"`.
 * 3. Prints the total and the execution time.
 *
 * @param argc The argument count (should be at least 2).
 * @param argv The argument vector. `argv[1]` must be the path to the input
 * file.
 *
 * @return `EXIT_SUCCESS` on success, `EXIT_FAILURE` on error.
 */
int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  long total = sum(argv[1]);
  if (total == EXIT_FAILURE) {
    printf("FAILED\n");
    return EXIT_FAILURE;
  } else {
    printf("Total is: %ld\n", total);
  }
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

/*
 * 161680 is too high for part 2
 * 5956 is too low for part 2
 * 5172 is too low for part 2
 * 125519 is wrong for part 2
 *
 * Correct output:
 * 87842 is the right answer for part 2
 * Execution time: 0.000653 seconds
 */

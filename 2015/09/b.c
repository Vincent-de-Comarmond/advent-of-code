#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void print_name_matrix(char name_matrix[20][20], int number_of_names) {
  int i;
  for (i = 0; i < number_of_names; i++) {
    printf("%d: %s\n", i, name_matrix[i]);
  }
}

void print_distance_matrix(int distance_matrix[20][20], int number_of_names) {
  int i, j;
  for (i = 0; i < number_of_names; i++) {
    for (j = 0; j < number_of_names; j++) {
      printf("%7d", distance_matrix[i][j]);
    }
    printf("\n");
  }
}

long shortest_path_held_karp(int distance_matrix[20][20], int number_cities) {
  int i = 0, j = 0;
  long mod_distances[20][20];

  for (i = 0; i <= number_cities; i++)
    for (j = 0; j <= number_cities; j++) {
      if (i == number_cities || j == number_cities) {
        mod_distances[i][j] = 0;
      } else {
        mod_distances[i][j] = distance_matrix[i][j];
      }
    }

  long city_2 = 0, city_1 = 0, city_subset = 1;
  long all_visits = 1 << (number_cities + 1);
  long city_visit_dp_table[all_visits][number_cities + 1];

  for (city_subset = 0; city_subset < all_visits; city_subset++)
    for (j = 0; j <= number_cities; j++) {
      city_visit_dp_table[city_subset][j] = 0;
    }
  city_visit_dp_table[1 << number_cities][number_cities] = 0;

  for (city_subset = 1; city_subset < all_visits; city_subset++) {
    for (city_1 = 0; city_1 <= number_cities; city_1++) {
      if (city_subset & (1 << city_1)) { // is the city in the subset
        for (city_2 = 0; city_2 <= number_cities; city_2++) {
          if (!(city_subset & (1 << city_2))) {
            // Only do something if we haven't already visited this city
            long another_subset = city_subset | (1 << city_2);
            long new_distance = city_visit_dp_table[city_subset][city_1] +
                                mod_distances[city_1][city_2];
            if (new_distance > city_visit_dp_table[another_subset][city_2]) {
              city_visit_dp_table[another_subset][city_2] = new_distance;
            }
          }
        }
      }
    }
  }

  long best = 0;
  for (city_1 = 0; city_1 < number_cities; city_1++) {
    if (city_visit_dp_table[all_visits - 1][city_1] > best) {
      best = city_visit_dp_table[all_visits - 1][city_1];
    }
  }

  return best;
}

long solve(char *file_path) {
  int buffer_size = 250;
  char line[buffer_size];
  FILE *file = fopen(file_path, "r");

  // Technically we only need 8
  int idx = 0, idx2 = 0;
  bool added_name = false;

  char name_matrix[20][20] = {[0 ... 19] = {[0 ... 19] = '\0'}};
  int distance_matrix[20][20] = {[0 ... 9] = {[0 ... 9] = 0}};

  while (fgets(line, buffer_size, file)) {
    char a[20] = "", b[20] = "";
    int i = 0, j = 0, d = 0;
    sscanf(line, "%s to %s = %d", a, b, &d);

    added_name = true;
    for (idx = 0; idx < idx2; idx++) {
      if (strcmp(a, name_matrix[idx]) == 0) {
        i = idx, added_name = false;
        break;
      }
    }

    if (added_name) {
      i = idx2, strcpy(name_matrix[idx2++], a);
    }

    added_name = true;
    for (idx = 0; idx < idx2; idx++) {
      if (strcmp(b, name_matrix[idx]) == 0) {
        j = idx, added_name = false;
        break;
      }
    }

    if (added_name) {
      j = idx2, strcpy(name_matrix[idx2++], b);
    }

    distance_matrix[i][j] = d;
    distance_matrix[j][i] = d;
  }

  fclose(file);
  return shortest_path_held_karp(distance_matrix, idx2);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  printf("Shortest Distance: %ld\n", solve(argv[1]));
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 117 is the right answer for part 1
// Execution time: 0.000249 seconds

// 909 is the right answer for part 2
// Execution time: 0.000228 seconds

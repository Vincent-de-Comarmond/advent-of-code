#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void solve(int target) {
  int i = 0, n = 0, sum = 0;
  int *sums = malloc((int)1e7 * sizeof(int));
  for (i = 0; i < (int)1e6; i++)
    sums[i] = 0;

  for (n = 1; n < target; n++) {
    /* printf("%.2f\n", (float)n / (float)target); */
    sum = 0;
    for (i = 1; i <= 50; i++) {
      if (n % i == 0) {
        sum += n / i;
        if (target <= sum) {
          printf("N is: %d\n", n);
          return;
        }
      }
    }
  }
}

int main(int argc, char *argv[]) {
  time_t start, end;

  start = clock();
  solve((int)(atoi(argv[1]) / 11));
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

/* N is: 200011
   Execution time: 0.860974 seconds
   This is too low ... it is based of some future i*/

/*
  N is: 786240
  Execution time: 0.067083 seconds - with no extra printing
  Yay ... this is the correct answer
*/

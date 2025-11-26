#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int *make_primes(int to_value) {
  int i, j, num_prime = 0;
  bool is_prime[to_value + 1];
  for (i = 0; i <= to_value; i++)
    is_prime[i] = true;

  for (i = 2; i <= to_value; i++) {
    if (is_prime[i]) {
      num_prime++;
      for (j = 2 * i; j <= to_value; j += i)
        is_prime[j] = false;
    }
  }

  j = 0;
  int *primes = malloc((num_prime + 1) * sizeof(int));

  for (i = 2; i <= to_value; i++)
    if (is_prime[i])
      primes[j++] = i;
  primes[j] = 0;

  return primes;
}

int *factor(int target, int *primes) {
  int idx = 0, prime_idx = 0, remaining = target;
  int *factors = calloc((int)1e6, sizeof(int));

  while (1 < remaining) {
    if (remaining % primes[prime_idx] == 0) {
      factors[idx++] = primes[prime_idx];
      remaining /= primes[prime_idx];
    } else {
      prime_idx++;
    }
  }
  return factors;
}

void solve(int target) {
  int idx = 0, prime, *primes = make_primes((int)sqrt(target));
  printf("Here\n");
  int *factors = factor(target, primes);
  do
    printf("factor: %d\n", factors[idx]);
  while (factors[++idx] != 0);

  free(primes);
  free(factors);
}

int main(int argc, char *argv[]) {
  time_t start, end;

  start = clock();
  printf("%s -> %d\n", argv[1], atoi(argv[1]));
  int max_number = (atoi(argv[1]) / 10);
  printf("Max Number: %d\n", max_number);
  solve(max_number);
  /* for (int i = 0; i < max_number; i++) */
  /*   printf("%d, ", primes[i]); */
  printf("\n");

  /* solve(atoi(argv[1]) / 10); */
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

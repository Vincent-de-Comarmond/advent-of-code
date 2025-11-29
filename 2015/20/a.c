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
    if (remaining % primes[prime_idx] != 0)
      prime_idx++;
    else {
      factors[idx++] = primes[prime_idx];
      remaining /= primes[prime_idx];
    }
  }
  return factors;
}

int factor_sum(int target, int *primes) {

  // printf("#####\nTarget: %d\n#####\n", target);
  int idx = 0, power = 1, current = 0, previous = 0;
  int *factors = factor(target, primes);

  float result = 1;
  current = factors[idx++];
  do {
    if (current == previous)
      power++;
    else {
      // printf("Previous: %d, Power: %d\n", previous, power);
      result *= (pow(previous, power + 1) - 1) / (previous - 1);
      power = 1;
    }

    // printf("%d, ", current);
    previous = current;
    current = factors[idx++];
  } while (current != 0);
  // printf("\n");
  result *= (pow(previous, power + 1) - 1) / (previous - 1);
  free(factors);

  /* printf("%d -> %.2f\n", target, result); */
  return (int)result;
}

/*
  Sum of factors is given by
  S = POW (a^(l+1) - 1) / (a - 1)
  We are looking for n such that
  sum_of_factors(n) =  target
  At worst n is prime and sum_of_factors(n) = n + 1
  So n is at most target-1
 */

void solve(int target) {
  int n = 0, sum = 0;
  int *primes = make_primes(target - 1);

  for (n = 1; n < target; n++) {
    /* printf("Target: %d, max_factors: %d\n", target, (int)sqrt(target - 1));
     */
    sum = factor_sum(n, primes);
    if (n % 10000 == 0) {
      printf("%d/%d -> %.2f\n", n, target, (float)n / (float)target);
    }
    if (target <= sum) {
      free(primes);
      printf("N is: %d\n", n);
      return;
    }
  }

  free(primes);
  return;
}

int main(int argc, char *argv[]) {
  time_t start, end;

  start = clock();
  solve(atoi(argv[1]) / 10);
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// 2476767 is the wrong answer (too high)
// run time for this is 253.277507 seconds

// 776160 is the correct answer (misread the question)
// Execution time: 71.706068 seconds

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct ReindeerStruct {
  char name[20];
  int speed;
  int stamina;
  int recovery;
  int cycle;
  int dist;
} Reindeer;

void print_deer(Reindeer deer) {
  printf("name: %s,\nspeed: %d,\nstamina: %d,\nrecovery: %d,\ncycle: %d,\n "
         "dist: %d\n",
         deer.name, deer.speed, deer.stamina, deer.recovery, deer.cycle,
         deer.dist);
}

long distance_after(Reindeer *deer, int time) {
  int cycles = time / deer->cycle;
  int leftover = time % deer->cycle;

  long dist = deer->dist * cycles;
  dist += leftover > deer->stamina ? deer->dist : deer->speed * leftover;

  return dist;
}

void solve(char *filename, int race_time) {
  FILE *file = fopen(filename, "r");
  if (file == NULL)
    printf("FAIL - could not open file.\n");

  int idx = 0;
  char linebuf[1000] = {[0 ... 999] = '\0'};
  Reindeer deer[100];

  while (fgets(linebuf, 1000, file)) {
    sscanf(
        linebuf,
        "%s can fly %d km/s for %d seconds, but then must rest for %d seconds.",
        deer[idx].name, &deer[idx].speed, &deer[idx].stamina,
        &deer[idx].recovery);

    deer[idx].cycle = deer[idx].stamina + deer[idx].recovery;
    deer[idx].dist = deer[idx].speed * deer[idx].stamina;
    idx++;
  }

  long best = 0, tmp = 0;

  for (int i = 0; i < idx; i++) {
    tmp = distance_after(&deer[i], race_time);
    best = tmp > best ? tmp : best;
  }

  printf("Winning distance is: %ld\n", best);
  fclose(file);
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  solve(argv[1], atoi(argv[2]));
  end = clock();

  printf("Execution time: %f seconds\n",
         (double)(end - start) / CLOCKS_PER_SEC);
  return EXIT_SUCCESS;
}

// 2655 is the right answer for part 1
// Execution time: 0.000062 seconds

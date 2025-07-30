#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

  long counter = 0;
  FILE *filepointer;
  filepointer = fopen(argv[1], "r");

  if (!filepointer) {
    perror("open");
    exit(EXIT_FAILURE);
  }

  int current = fgetc(filepointer);
  while (current != EOF) {
    switch (current) {
    case '(':
      counter++;
      break;
    case ')':
      counter--;
      break;
    }
    current = fgetc(filepointer);
  }

  printf("Floor: %ld\n", counter);
  return EXIT_SUCCESS;
}

// 232 is the right answer for part 1

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
  int character_number = 1;

  while (current != EOF) {
    switch (current) {
    case '(':
      counter++;
      break;
    case ')':
      counter--;
      break;
    }

    if (counter == -1) {
      break;
    }

    current = fgetc(filepointer);
    character_number++;
  }

  printf("Characters to enter basement: %d\n", character_number);
  return EXIT_SUCCESS;
}

// 232 is the right answer for part 1
// 1783 is the right answer for part 2

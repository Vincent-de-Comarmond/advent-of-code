#include <openssl/evp.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// From here
// https://stackoverflow.com/questions/7627723/how-to-create-a-md5-hash-of-a-string-in-c

void bytes2md5(const char *data, int len, char *md5buf) {
  // Based on https://www.openssl.org/docs/manmaster/man3/EVP_DigestUpdate.html
  EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
  const EVP_MD *md = EVP_md5();
  unsigned char md_value[EVP_MAX_MD_SIZE];
  unsigned int md_len, i;
  EVP_DigestInit_ex(mdctx, md, NULL);
  EVP_DigestUpdate(mdctx, data, len);
  EVP_DigestFinal_ex(mdctx, md_value, &md_len);
  EVP_MD_CTX_free(mdctx);
  for (i = 0; i < md_len; i++) {
    snprintf(&(md5buf[i * 2]), 16 * 2, "%02x", md_value[i]);
  }
}

int solve(const char *secret_key) {
  int j = 0, i = 1;
  bool solved = false;
  char as_string[50];
  char modified[1000], md5buffer[1000];

  while (!solved) {
    strcpy(modified, secret_key);
    sprintf(as_string, "%d", i);
    strcat(modified, as_string);

    bytes2md5(modified, strlen(modified), md5buffer);

    solved = true;
    for (j = 0; j < 6; j++) {
      if (md5buffer[j] != '0') {
        solved = false;
        i++;
        break;
      }
    }
  }
  return i;
}

int main(int argc, char *argv[]) {
  clock_t start, end;

  start = clock();
  printf("%d\n", solve(argv[1]));
  end = clock();

  double elapsed_seconds = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Execution time: %f seconds\n", elapsed_seconds);
  return EXIT_SUCCESS;
}

// 346386 is the right answer for part 1
// 9958218 is the right answer for part 2

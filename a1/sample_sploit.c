/*
 * dummy exploit program
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define TARGET "/usr/local/bin/submit" // or submitV2

int main(void) {
  char *args[4];
  char *env[1];

  // one way to invoke submit
  system(TARGET " file.txt \"Hello world!\"");

  // another way
  args[0] = TARGET;
  args[1] = "file.txt"; 
  args[2] = "Hello world!";
  args[3] = NULL;

  env[0] = NULL;

  execve(TARGET, args, env);
  // execve only returns if it fails
  fprintf(stderr, "execve failed\n");
  return 1;
}

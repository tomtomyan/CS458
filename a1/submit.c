/*
 * A very simple program to submit a file - use at your own risk ;)
 *
 */

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <pwd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>
#include <regex.h>
#include <time.h>

#define SUBMIT_DIRECTORY "/usr/share/submit"
#define LOG_FILE "submit.log"
#define VERSION "0.1"

typedef struct {
	unsigned int submitted;
	unsigned int version;
	unsigned int help;
	unsigned int delete;
	char* path;
	char* message;
} submit_args;

//Prints version
static
void print_version(char* version_info) {
	printf(version_info);
	printf("\n");
	printf("Built with gcc version: ");
	printf(__VERSION__);
	printf("\n");
}

static
int run_cmd(char* cmd, ... ) {
	va_list vl;
	char* arg[8];
	pid_t pid;
	int i, status;

	i = 1;
	va_start(vl, cmd);
	while(i < 7 && (arg[i++] = va_arg(vl, char*)));
	va_end(vl);
	arg[7] = NULL;
	arg[0] = rindex(cmd, '/');
	if (arg[0] == NULL)
		arg[0] = cmd;
	else
		arg[0]++;

	pid = fork();
	// error
	if (pid < 0) {
		fprintf(stderr, "Fork failed\n");
		return 1;
	}
	if (pid > 0) {
		waitpid(pid, &status, 0);
		if (WIFEXITED(status) == 0 || WEXITSTATUS(status) != 0)
			return 1;
	}
	else {
		execvp(cmd, arg);
		return 1;
	}
	return 0;
}

static
int copy_file(const char* src_name, const char* dst_name) {
	unsigned int counter, file_len;
	char buf[4000];
	FILE *src_file, *dst_file;
	int c;

	src_file = fopen(src_name, "r");
	if (src_file == NULL) {
		fprintf(stderr, "Failed to open source file: %s\n", src_name);
		return 1;
	}
	counter = 0;
	while ((c = fgetc(src_file)) != EOF) {
		buf[counter] = c;
		counter++;
	}

	file_len = counter;
	fclose(src_file);

	dst_file = fopen(dst_name, "w");
	if (dst_file == NULL) {
		fprintf(stderr, "Failed to open destination file: %s\n", dst_name);
		return 1;
	}
	for (counter=0; counter<file_len; counter++) {
		fputc(buf[counter], dst_file);
	}

	fclose(dst_file);
	return 0;
}

static
int dir_exists(char* dir) {
	struct stat s;
	int err = stat(dir, &s);
	if (err == -1 && errno == ENOENT) {
		return 0;
	} else {
		if (S_ISDIR(s.st_mode)) {
			return 1;
		} else {
			unlink(dir);
			return 0;
		}
	}
	return 0;
}
	
static
char* get_submit_dir() {
	char* subdir_name;
	char* username = getenv("USER");

	if (username == NULL) {
		username = "default";
	}

	subdir_name = malloc(strlen(SUBMIT_DIRECTORY) + 1
		+ strlen(username) + 1);
	if (subdir_name == NULL) {
		fprintf(stderr, "Failed to allocate memory\n");
		return NULL;
	}
	
	strcpy(subdir_name, SUBMIT_DIRECTORY);
	strcat(subdir_name, "/");
	strcat(subdir_name, username);
	if (!dir_exists(subdir_name))
		run_cmd("mkdir", subdir_name, NULL);
	return subdir_name;
}

static
char* get_dst_name(char* src_name) {
	char* dst_name;
	char* subdir_name;

	subdir_name = get_submit_dir();
	if (subdir_name == NULL) {
		return NULL;
	}

	dst_name = malloc(strlen(subdir_name) + 1 + strlen(src_name) + 1);
	if (dst_name == NULL) {
		fprintf(stderr, "Failed to allocate memory\n");
		return NULL;
	}
	
	strcpy(dst_name, subdir_name);
	strcat(dst_name, "/");
	strcat(dst_name, src_name);
	free(subdir_name);

	return dst_name;
}

static
char* get_logfile_name() {
	uid_t userid;
	gid_t groupid;
	struct passwd *entry;
	char *pathname, *safepath, *ptr;
	struct stat buf;
	int fd;

	userid = getuid();
	groupid = getgid();
	entry = getpwuid(userid);
	if (entry == NULL) {
		fprintf(stderr, "Failed to find pwd entry\n");
		return NULL;
	}

	pathname = malloc(6 + strlen(entry->pw_name) + 1
		+ strlen(LOG_FILE) + 1);
	if (pathname == NULL) {
		fprintf(stderr, "Failed to allocate memory\n");
		return NULL;
	}

	safepath = malloc(6 + strlen(entry->pw_name) + 1);
	if (safepath == NULL) {
		fprintf(stderr, "Failed to allocate memory\n");
		return NULL;
	}

	strcpy(pathname, "/home/");
	strcat(pathname, entry->pw_name);
	strcpy(safepath, pathname);
	strcat(pathname, "/");
	strcat(pathname, LOG_FILE);

	ptr = realpath(pathname, NULL);
	if (ptr == NULL) {		
		fd = creat(pathname, S_IWUSR | S_IRUSR);
		if (fd < 0) {
			fprintf(stderr, "Failed to create log file: %s\n",
				pathname);
			return NULL;
		}
		if (fchown(fd, userid, groupid) < 0) {
			fprintf(stderr,
				"Failed to change ownership of log file: %s\n", 
				pathname);
			return NULL;
		}
	}
	else {
		if (strncmp(ptr, safepath, strlen(safepath))) {
			fprintf(stderr, "Invalid log file: %s\n", ptr);
			return NULL;
		}
	
		if (stat(pathname, &buf) != 0) {
			fprintf(stderr, "Failed to stat\n");
			return NULL;
		}
		
		if (buf.st_uid != userid) {
			fprintf(stderr, "Not your log file: %s\n", pathname);
			return NULL;
		}
	}

	return pathname;
}

//Checks for substrings in the program that have been connected to troublesome submissions
static
int check_for_viruses(char* filename) {
	char buf[1024], *p1;
	FILE *src_file;
	int c, ctr;
	regex_t regex;
	int reti;

	printf("Checking %s for viruses...\n", filename);
	
	src_file = fopen(filename, "r");
	if (src_file == NULL) {
		fprintf(stderr, "Failed to open source file: %s\n",
			filename);
		return 1;
	}
	while (c != EOF) {
		memset(buf, 0, sizeof(buf));
		p1 = buf;
		ctr = 0;
		while (((c = fgetc(src_file)) != EOF) && (ctr < sizeof(buf)-1)) {
			*p1 = c;
			p1++;
			ctr++;
		}
	
		if (regcomp(&regex, "bin/sh", 0)) {
			fprintf(stderr, "Could not compile known virus signatures\n");
			return 1;
		}

		reti = regexec(&regex, buf, 0, NULL, 0);
		if (reti == 0) {
			printf("Alert! Detected possibly malicious submission! Terminating.\n");
			return  1;
		}
	}
		
	printf("No viruses found! :)\n");

	return 0;
}

static
int log_message(char* message, char* logfile_name) {
	FILE* logfile;
	time_t t = time(NULL);
	struct tm local_t = *localtime(&t);

	if (message == NULL)
		message = "n/a";

	if ((logfile = fopen(logfile_name, "a")) == NULL)
		return 1;

	fprintf(logfile, "%d-%d-%d %02d:%02d:%02d - ", local_t.tm_year+1900, local_t.tm_mon+1,
	        local_t.tm_mday, local_t.tm_hour, local_t.tm_min, local_t.tm_sec);
	fputs(message, logfile);
	fputs("\n", logfile);
	fclose(logfile);
	return 0;
}

//Parses arguments from commandline
//Returns struct with the appropriate flags set
static
submit_args parse_args(int argc, char* argv[]) {
	int c, opts;
	submit_args args;

	struct option long_options[] = {
		{"submitted", 0, NULL, 's'},
		{"version", 0, NULL, 'v'},
		{"help", 0, NULL, 'h'},
		{0, 0, 0, 0}
	};

	memset(&args, 0, sizeof(submit_args));

	c = 0;
	opts = 0;

	while (1) {
		c = getopt_long(argc, argv, "sdvh", long_options, NULL);
		if (c == -1) break;

		switch (c) {
			case 's':
				opts = 1;
				args.submitted = 1;
				break;
			case 'v':
				opts = 1;
				args.version = 1;
				break;
			default:
				opts = 1;
				args.help = 1;
				break;
		}
		if (args.help) break;
	}
	
	if (!opts && argc-optind >= 1) {
		args.path = argv[optind+0];
		if (argc-optind >= 2) {
			args.message = argv[optind+1];
		}
	} else if (argc <= 1)
		args.help = 1;

	return args;
}

//Prints usage
static
void print_usage(char* cmd) {
	printf("Syntax:\n\t%s <path> [log message]\n"
		"-s, --submitted  Show your submitted files\n"
		"-v, --version    Show version\n"
		"-h, --help       Show this usage message\n", cmd);
}

static
int show_confirmation() {
	char* subdir_name;
	subdir_name = get_submit_dir();
	if (subdir_name != NULL) {
		run_cmd("/usr/bin/find", subdir_name, "-mindepth", "1", NULL);
		free(subdir_name);
	}
	return 0;
}

static
int check_forbidden(char* source) {
	char forbidden_char = '/';

	if (index(source, (int)forbidden_char) != NULL) {
		fprintf(stderr, "File name includes slash\n");
		return 1;
	}

	return 0;
}

int main(int argc, char* argv[]) {
	char *dst, *logfile_name;
	int unsafe = 0;
	char status_msg[160] = {0};
	submit_args args;
	char version[8] = VERSION;
	char version_info[300] = {0};

	strcpy(status_msg, "Status: ");

	//parse arguments
	args = parse_args(argc, argv);
	if (args.help) {
		print_usage(argv[0]);
		return 0;
	}

	if (args.version) {
		sprintf(version_info, "Submission program version %s (%.240s)", version, argv[0]);
		print_version(version_info);
		return 0;
	}

	if (args.submitted) {
		printf("Submitted files:\n");
		show_confirmation();
		return 0;
	}

	//get logfile name
	logfile_name = get_logfile_name();
	if (logfile_name == NULL)
		//error
		return 1;

	//get destination name
	dst = get_dst_name(args.path);
	if (dst == NULL)
		//error
		return 1;

	//check to make sure the source directory doesn't contain invalid characters
	if (!unsafe && check_forbidden(args.path)) {
		unsafe = 1;
		strcpy(status_msg+strlen(status_msg), "Forbidden name: ");
		strncpy(status_msg+strlen(status_msg), args.path, sizeof(status_msg)-strlen(status_msg));
		status_msg[sizeof(status_msg)-1] = '\0';
	}

	//check for viruses
	if (!unsafe && check_for_viruses(args.path)) {
		unsafe = 1;
		strcpy(status_msg+strlen(status_msg), "Possible virus.");
	}

	//copy the file
	if (!unsafe) {
		if (copy_file(args.path, dst))
			//error
			return 1;
		if (log_message(args.message, logfile_name))
			//error
			return 1;
		strcpy(status_msg+strlen(status_msg), "Success!");
	}

	free(logfile_name);
	free(dst);

	printf("%s\n", status_msg);

	printf("Submitted files:\n");
	show_confirmation();

	return 0;
}

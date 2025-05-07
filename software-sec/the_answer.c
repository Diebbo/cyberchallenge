#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int answer = 0xbadc0ffe;

int main(int argc, char **argv) {
  setvbuf(stdout, NULL, _IONBF, 0);
  char name[4096];
  memset(name, 0, sizeof(name));
  printf("What's your name?\n");
  if (!fgets(name, sizeof(name), stdin))
    exit(EXIT_FAILURE);
  printf("Hi, ");
  printf(name);
  if (answer == 42) {
    printf("Exactly! Here's your flag:\n");
    int f = open("flag.txt", O_RDONLY);
    ssize_t n = read(f, name, sizeof name);
    write(1, name, n);
  }
}

// AAAABBBB %p %p %p %p %p %p %p %p %p %p %p

#include <stdio.h>
struct billboard {
  char text[256];
  char devmode;
};

int main() {
  printf("size of struct billboard: %d\n", sizeof(struct billboard));
  return 0;
}

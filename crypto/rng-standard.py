#!/usr/bin/env python3

import signal
import os
import random

TIMEOUT = 300

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("CCIT{"))
assert(FLAG.endswith("}"))


def handle():
    for i in range(625):
        print(f"Round {i+1}")
        guess_count = 10
        to_guess = random.getrandbits(32)
        while True:
            print("What do you want to do?")
            print("1. Guess my number")
            print("2. Give up on this round")
            print("0. Exit")
            choice = int(input("> "))
            if choice == 0:
                exit()
            elif choice == 1:
                guess = int(input("> "))
                if guess == to_guess:
                    print(FLAG)
                    exit()
                elif guess < to_guess:
                    print("My number is higher!")
                    guess_count -= 1
                else:
                    print("My number is lower!")
                    guess_count -= 1
            elif choice == 2:
                print(f"You lost! My number was {to_guess}")
                break
            if guess_count == 0:
                print(f"You lost! My number was {to_guess}")
                break


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()

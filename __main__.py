#!/usr/bin/python

from castcontroller.playlist import run_playlist


if __name__ == "__main__":
    print("Running...")
    run_playlist('/dev/input/event0')

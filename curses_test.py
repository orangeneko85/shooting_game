# curses_test.py

import curses
import time

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Hide the cursor
    curses.curs_set(0)

    # Draw a simple 5x5 grid
    grid = [
        ". . . . .",
        ". . . . .",
        ". . P . .",
        ". . . . .",
        ". . . . .",
    ]

    for i, line in enumerate(grid):
        stdscr.addstr(i, 0, line)

    stdscr.addstr(7, 0, "Press any key to exit")

    stdscr.refresh()

    # Wait for a key press
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)

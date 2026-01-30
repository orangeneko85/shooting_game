import curses
import time

GRID_SIZE = 5

def draw_grid(stdscr, player_pos):
    stdscr.clear()

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (y, x) == player_pos:
                stdscr.addstr(y, x * 2, "P")
            else:
                stdscr.addstr(y, x * 2, ".")

    stdscr.addstr(GRID_SIZE + 1, 0, "Use W/A/S/D to move, Q to quit")
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    player_y, player_x = 2, 2

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('w') and player_y > 0:
            player_y -= 1
        elif key == ord('s') and player_y < GRID_SIZE - 1:
            player_y += 1
        elif key == ord('a') and player_x > 0:
            player_x -= 1
        elif key == ord('d') and player_x < GRID_SIZE - 1:
            player_x += 1

        draw_grid(stdscr, (player_y, player_x))
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)

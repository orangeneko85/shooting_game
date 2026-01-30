import curses
import time
import random

GRID_SIZE = 5
PLAYER_POS = (2, 2)

# ----------------------------
# Enemy spawn (outer ring only)
# ----------------------------
def spawn_enemy():
    edge_positions = []

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (y, x) == PLAYER_POS:
                continue
            if y == 0 or y == GRID_SIZE - 1 or x == 0 or x == GRID_SIZE - 1:
                edge_positions.append((y, x))

    return random.choice(edge_positions)

# ----------------------------
# Bullet path
# ----------------------------
def get_bullet_path(direction):
    py, px = PLAYER_POS
    path = []

    if direction == 'w':
        for y in range(py - 1, -1, -1):
            path.append((y, px))
    elif direction == 's':
        for y in range(py + 1, GRID_SIZE):
            path.append((y, px))
    elif direction == 'a':
        for x in range(px - 1, -1, -1):
            path.append((py, x))
    elif direction == 'd':
        for x in range(px + 1, GRID_SIZE):
            path.append((py, x))

    return path

# ----------------------------
# Drawing functions
# ----------------------------
def draw_grid(stdscr, enemy_pos=None, bullet_path=None):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pos = (y, x)
            char = "."

            if pos == PLAYER_POS:
                char = "P"
            elif bullet_path and pos in bullet_path:
                char = "*"
            elif enemy_pos and pos == enemy_pos:
                char = "E"

            stdscr.addstr(y, x * 2, char)

def draw_menu(stdscr):
    stdscr.clear()
    draw_grid(stdscr)
    stdscr.addstr(1, 12, "press y to start")
    stdscr.addstr(2, 12, "press n to quit")
    stdscr.refresh()

def draw_hud(stdscr, hp, score):
    stdscr.addstr(GRID_SIZE + 1, 0, f"HP: {hp}   Score: {score}")
    stdscr.addstr(GRID_SIZE + 2, 0, "Shoot: W/A/S/D")

def draw_game_over(stdscr, score, best_score):
    stdscr.clear()
    draw_grid(stdscr)
    stdscr.addstr(1, 12, f"score this time: {score}")
    stdscr.addstr(2, 12, f"best score: {best_score}")
    stdscr.addstr(4, 12, "press e to start another game")
    stdscr.addstr(5, 12, "press q to quit")
    stdscr.refresh()

# ----------------------------
# Enemy movement AI
# ----------------------------
def move_enemy(enemy_pos):
    ey, ex = enemy_pos
    py, px = PLAYER_POS
    dy = py - ey
    dx = px - ex

    if abs(dy) <= 1 and abs(dx) <= 1:
        if dy != 0 and dx != 0:
            if abs(dy) >= abs(dx):
                ey += 1 if dy > 0 else -1
            else:
                ex += 1 if dx > 0 else -1
        else:
            ey, ex = py, px
    else:
        if abs(dy) >= abs(dx):
            ey += 1 if dy > 0 else -1
        else:
            ex += 1 if dx > 0 else -1

    return (ey, ex)

# ----------------------------
# Main
# ----------------------------
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    state = "MENU"
    best_score = 0

    while state != "EXIT":

        # -------- MENU --------
        if state == "MENU":
            draw_menu(stdscr)
            while True:
                key = stdscr.getch()
                if key == ord('y'):
                    state = "COUNTDOWN"
                    break
                if key == ord('n'):
                    state = "EXIT"
                    break
                time.sleep(0.1)

        # -------- COUNTDOWN --------
        if state == "COUNTDOWN":
            for i in range(3, 0, -1):
                stdscr.clear()
                draw_grid(stdscr)
                stdscr.addstr(2, 12, f"Starting in {i}")
                stdscr.refresh()
                time.sleep(1)
            state = "PLAYING"

        # -------- PLAYING --------
        if state == "PLAYING":
            hp = 3
            score = 0
            enemy_pos = spawn_enemy()

            while True:
                key = stdscr.getch()

                if key in (ord('w'), ord('a'), ord('s'), ord('d')):
                    direction = chr(key)
                    bullet_path = get_bullet_path(direction)
                    stdscr.clear()
                    draw_grid(stdscr, enemy_pos, bullet_path)
                    draw_hud(stdscr, hp, score)
                    stdscr.refresh()
                    time.sleep(0.1)

                    if enemy_pos in bullet_path:
                        score += 1
                        enemy_pos = spawn_enemy()
                    continue

                enemy_pos = move_enemy(enemy_pos)

                if enemy_pos == PLAYER_POS:
                    hp -= 1
                    if hp == 0:
                        best_score = max(best_score, score)
                        state = "GAME_OVER"
                        break
                    enemy_pos = spawn_enemy()

                stdscr.clear()
                draw_grid(stdscr, enemy_pos)
                draw_hud(stdscr, hp, score)
                stdscr.refresh()
                time.sleep(0.4)

        # -------- GAME OVER --------
        if state == "GAME_OVER":
            draw_game_over(stdscr, score, best_score)
            while True:
                key = stdscr.getch()
                if key == ord('e'):
                    state = "COUNTDOWN"
                    break
                if key == ord('q'):
                    state = "EXIT"
                    break
                time.sleep(0.1)

# ----------------------------
if __name__ == "__main__":
    curses.wrapper(main)

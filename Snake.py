import curses
import random
import time

def main(stdscr):
    # Inisialisasi curses
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(True)
    w.timeout(100)

    # Inisialisasi ular dan makanan
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    food_y = sh // 2
    food_x = sw // 2
    w.addch(food_y, food_x, curses.ACS_PI)

    # Inisialisasi arah
    key = curses.KEY_RIGHT

    while True:
        try:
            next_key = w.getch()
            key = key if next_key == -1 else next_key
        except KeyboardInterrupt:
            break

        # Kondisi kalah
        if snake[0][0] in [0, sh - 1] or snake[0][1] in [0, sw - 1] or snake[0] in snake[1:]:
            msg = "Game Over! Score: " + str(len(snake) - 3)
            w.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            w.refresh()
            time.sleep(2)
            break

        # Pergerakan ular
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # Makan makanan
        if snake[0] == [food_y, food_x]:
            food_y = random.randint(1, sh - 2)
            food_x = random.randint(1, sw - 2)
            while [food_y, food_x] in snake:
                food_y = random.randint(1, sh - 2)
                food_x = random.randint(1, sw - 2)
            w.addch(food_y, food_x, curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Gambar ular
        for y, x in snake:
            w.addch(y, x, curses.ACS_CKBOARD)

        w.refresh()

if __name__ == '__main__':
    curses.wrapper(main)

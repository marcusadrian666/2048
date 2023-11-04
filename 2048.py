import random
import curses

# 初始化游戏板
def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    board = add_random_tile(add_random_tile(board))
    return board

# 在空白位置随机添加一个2或4
def add_random_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4
    return board

# 打印游戏板
def print_board(stdscr, board):
    for i in range(4):
        for j in range(4):
            stdscr.addstr(5 + i * 4, 5 + j * 8, str(board[i][j]))
    stdscr.refresh()

# 检查是否游戏结束
def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

# 移动游戏板
def move_board(board, direction):
    new_board = [row[:] for row in board]
    if direction == 'left':
        for i in range(4):
            new_board[i] = merge(new_board[i])
    elif direction == 'right':
        for i in range(4):
            new_board[i] = merge(new_board[i][::-1])[::-1]
    elif direction == 'up':
        new_board = [list(x) for x in zip(*new_board)]
        for i in range(4):
            new_board[i] = merge(new_board[i])
        new_board = [list(x) for x in zip(*new_board)]
    elif direction == 'down':
        new_board = [list(x) for x in zip(*new_board)]
        for i in range(4):
            new_board[i] = merge(new_board[i][::-1])[::-1]
        new_board = [list(x) for x in zip(*new_board)]
    return new_board

# 合并相同的数字
def merge(row):
    new_row = [0, 0, 0, 0]
    j = 0
    for i in range(4):
        if row[i] != 0:
            if new_row[j] == 0:
                new_row[j] = row[i]
            elif new_row[j] == row[i]:
                new_row[j] *= 2
                j += 1
            else:
                j += 1
                new_row[j] = row[i]
    return new_row

# 主游戏循环
def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    board = initialize_board()
    while not is_game_over(board):
        stdscr.clear()
        print_board(stdscr, board)
        direction = stdscr.getch()
        if direction == curses.KEY_UP:
            board = move_board(board, 'up')
        elif direction == curses.KEY_DOWN:
            board = move_board(board, 'down')
        elif direction == curses.KEY_LEFT:
            board = move_board(board, 'left')
        elif direction == curses.KEY_RIGHT:
            board = move_board(board, 'right')

    stdscr.addstr(12, 5, "Game over! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)

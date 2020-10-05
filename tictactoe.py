# write your code here
import random
from datetime import datetime


def display_board(board):
    print("---------")
    print(f'| {board[0][0]} {board[0][1]} {board[0][2]} |')
    print(f'| {board[1][0]} {board[1][1]} {board[1][2]} |')
    print(f'| {board[2][0]} {board[2][1]} {board[2][2]} |')
    print("---------")


def empty_spots(board):
    empty_spaces = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                empty_spaces.append([i, j])
    return empty_spaces


def check_win(win_lines):
    for line in win_lines.values():
        if len(set(line)) == 1 and ' ' not in line:
            return line[0]
    return False


def user_move(board, token):
    cell = input("Enter the coordinates: ").split()

    if any(char not in '0123456789' for char in cell):
        print("You should enter numbers!")
        return False

    cell = [int(num) for num in cell]

    if any(num > 3 for num in cell) or any(num < 1 for num in cell):
        print("Coordinates should be from 1 to 3!")
        return False

    cell[0] -= 1
    if cell[1] == 1:
        cell[1] = 2
    elif cell[1] == 2:
        cell[1] = 1
    else:
        cell[1] = 0

    if board[cell[1]][cell[0]] != ' ':
        print("This cell is occupied! Choose another one!")
        return False

    board[cell[1]][cell[0]] = token
    return True


def computer_move(token, board):
    while True:
        random.seed(datetime.now())
        row = board.index(random.choice(board))
        space = board[row].index(random.choice(board[row]))
        if board[row][space] != ' ':
            continue
        else:
            board[row][space] = token
            break


def computer_move_med(token, board, win_lines):
    opp_token = 'X' if token == 'O' else 'O'
    moved = False
    for line in win_lines:
        if (win_lines[line].count(token) == 2 or win_lines[line].count(opp_token) == 2) and \
                ' ' in win_lines[line]:
            idx = win_lines[line].index(' ')
            space = board_space(line, idx)
            board[space[0]][space[1]] = token
            moved = True
            break
    if not moved:
        computer_move(token, board)


def computer_move_hard(board, player, computer, opponent):
    empty_spaces = empty_spots(board)
    win_lines = generate_win_lines(board)

    if check_win(win_lines) == computer:
        return {'score': 10}
    elif check_win(win_lines) == opponent:
        return {'score': -10}
    elif len(empty_spaces) == 0:
        return {'score': 0}

    moves = []

    for space in empty_spaces:
        move = {'index': space}
        board[space[0]][space[1]] = player

        if player == computer:
            result = computer_move_hard(board, opponent, computer, opponent)
            move['score'] = result['score']
        else:
            result = computer_move_hard(board, computer, computer, opponent)
            move['score'] = result['score']

        board[space[0]][space[1]] = ' '
        moves.append(move)

    best_move = None
    if player == computer:
        best_score = -1000000
        for i, move in enumerate(moves):
            if move['score'] > best_score:
                best_score = move['score']
                best_move = i
    else:
        best_score = 1000000
        for i, move in enumerate(moves):
            if move['score'] < best_score:
                best_score = move['score']
                best_move = i

    return moves[best_move]


def generate_win_lines(board):
    return {'row1': [board[0][0], board[0][1], board[0][2]], 'row2': [board[1][0], board[1][1], board[1][2]],
            'row3': [board[2][0], board[2][1], board[2][2]], 'col1': [board[0][0], board[1][0], board[2][0]],
            'col2': [board[0][1], board[1][1], board[2][1]], 'col3': [board[0][2], board[1][2], board[2][2]],
            'diag1': [board[0][0], board[1][1], board[2][2]], 'diag2': [board[2][0], board[1][1], board[0][2]]}


def board_space(line, index):
    if line == 'diag1':
        if index == 0:
            return [0, 0]
        elif index == 1:
            return [1, 1]
        else:
            return [2, 2]
    elif line == 'diag2':
        if index == 0:
            return [2, 0]
        elif index == 1:
            return [1, 1]
        else:
            return [0, 2]
    elif line.startswith('row'):
        row = int(line[-1]) - 1
        col = index
        return [row, col]
    else:
        col = int(line[-1]) - 1
        row = index
        return [row, col]


def game_menu():
    while True:
        command = input("Input command: ")
        if command == 'exit':
            break
        else:
            command = command.split()
            if len(command) != 3:
                print('Bad parameters')
                continue
            elif command[1] not in ['easy', 'medium', 'hard', 'user'] or \
                    command[2] not in ['easy', 'medium', 'hard', 'user']:
                print('Bad parameters')
                continue
            else:
                play_game(command[1], command[2])


def play_game(first, second):
    field = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    switch = True
    diff_switch = False
    if first in ['easy', 'medium', 'hard'] and second in ['easy', 'medium', 'hard']:
        turn = 'computer'
        difficulty = first
        if first != second:
            diff_switch = True
            opp_difficulty = second
        switch = False
    elif first == 'user' and second == 'user':
        turn = 'user'
        switch = False
    elif first in ['easy', 'medium', 'hard']:
        turn = 'computer'
        difficulty = first
    else:
        turn = 'user'
        difficulty = second

    current = 'X'
    opponent = 'O'
    filled = 0

    while True:
        display_board(field)
        win_lines = generate_win_lines(field)
        win = check_win(win_lines)

        if win:
            print(f'{win} wins')
            break
        elif filled == 9:
            print("Draw")
            break

        if turn == 'computer':
            if difficulty == 'medium':
                print('Making move level "medium"')
                computer_move_med(current, field, win_lines)
            elif difficulty == 'hard':
                print('Making move level "hard"')
                move = computer_move_hard(field, current, current, opponent)
                index = move['index']
                field[index[0]][index[1]] = current
            else:
                print('Making move level "easy"')
                computer_move(current, field)

            if diff_switch:
                difficulty, opp_difficulty = opp_difficulty, difficulty

            filled += 1
            current, opponent = opponent, current
            if switch:
                turn = 'user'
            continue
        else:
            success = user_move(field, current)
            if not success:
                continue

            filled += 1
            current, opponent = opponent, current
            if switch:
                turn = 'computer'


game_menu()

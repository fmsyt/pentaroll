from define import SIDE_LENGTH
from lib import (Direction, can_insert, check_winner, insert,
                 line_as_matrix_horizontal)


def help():
    pass


def init():
    global line
    line = [0 for _ in range(SIDE_LENGTH ** 2)]

def print_matrix_with_legend():
    matrix = line_as_matrix_horizontal(line)
    for i in range(SIDE_LENGTH):
        for j in range(SIDE_LENGTH):
            print(matrix[i][j], end="")
        print()


def wait_input() -> tuple:

    while True:

        while True:
            direction = input("Enter direction: ")
            if not Direction.is_valid_str(direction):
                print("Invalid direction")
                continue

            break

        while True:
            number = input("Enter number: ")
            if not number.isdigit() or not 1 <= int(number) <= SIDE_LENGTH:
                print("Invalid number")
                continue

            number = int(number)
            break

        direction = Direction.from_str(direction)

        if not can_insert(line, direction, number):
            print("Can't insert")
            continue

        break

    return direction, number


def main():

    global line

    try:
        turn = 1  # 1 | 2
        while True:

            winner = check_winner(line)
            if winner != 0:
                print(f"Winner: {winner}")
                break

            print(f"Turn: {turn}")
            print_matrix_with_legend()
            direction, number = wait_input()
            line = insert(line, turn, direction, number)

            turn = 1 if turn == 2 else 2

            print()

    except KeyboardInterrupt:
        print("Bye!")


if __name__ == "__main__":
    init()
    main()

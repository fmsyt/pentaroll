import itertools
from enum import Enum

from define import SIDE_LENGTH, WIN_CONDITION_COUNT


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @staticmethod
    def from_str(direction: str):
        if direction in ["up", "u", "U"]:
            return Direction.UP
        elif direction in ["down", "d", "D"]:
            return Direction.DOWN
        elif direction in ["left", "l", "L"]:
            return Direction.LEFT
        elif direction in ["right", "r", "R"]:
            return Direction.RIGHT
        else:
            raise ValueError("Invalid direction")

    @staticmethod
    def is_valid_str(direction: str) -> bool:
        try:
            Direction.from_str(direction)
            return True
        except ValueError:
            return False


def line_as_matrix_vertical(line: list[int]) -> list[list[int]]:
    """line_as_matrix

    example:
    ```
    [0, 0, 0, 1, 1, 1, 2, 2, 2]
    ```
    to
    ```
    [[0, 0, 0],
     [1, 1, 1],
     [2, 2, 2]]
    ```
    """
    return [line[i * SIDE_LENGTH: (i + 1) * SIDE_LENGTH] for i in range(SIDE_LENGTH)]


def line_as_matrix_horizontal(line: list[int]) -> list[list[int]]:
    """line_as_matrix

    example:
    ```python
    [0, 0, 0, 1, 1, 1, 2, 2, 2]
    ```
    to
    ```python
    [[0, 1, 2],
     [0, 1, 2],
     [0, 1, 2]]
    ```
    """
    return [line[i::SIDE_LENGTH] for i in range(SIDE_LENGTH)]


def matrix_vertical_as_line(matrix) -> list[int]:
    """matrix_as_line

    example:
    ```
    [[0, 0, 0],
     [1, 1, 1],
     [2, 2, 2]]
    ```
    to
    ```
    [0, 0, 0, 1, 1, 1, 2, 2, 2]
    ```
    """
    return [matrix[i][j] for i in range(SIDE_LENGTH) for j in range(SIDE_LENGTH)]


def matrix_horizontal_as_line(matrix) -> list[int]:
    """matrix_as_line

    example:

    ```python
    [[0, 1, 2],
     [0, 1, 2],
     [0, 1, 2]]
    ```
    to
    ```python
    [0, 0, 0, 1, 1, 1, 2, 2, 2]
    ```
    """
    return [matrix[j][i] for i in range(SIDE_LENGTH) for j in range(SIDE_LENGTH)]


def can_insert(line: list[int], direction: Direction, row: int) -> bool:

    if not 1 <= row <= SIDE_LENGTH:
        return False

    i = row - 1

    if direction == "up" or direction == "down":
        matrix = line_as_matrix_vertical(line)
        # search 0, exists 0, return True

        return True if 0 in matrix[i] else False

    elif direction == "left" or direction == "right":
        matrix = line_as_matrix_horizontal(line)
        # search 0, exists 0, return True

        return True if 0 in matrix[i] else False

    return True


def insert(line: list[int], turn: int, direction: Direction, row: int):

    if not 1 <= row <= SIDE_LENGTH:
        raise ValueError("Invalid number")

    i = row - 1

    if direction == Direction.UP:
        matrix = line_as_matrix_vertical(line)
        # row = 1 の場合、`matrix[0]`の先頭に挿入、末尾を削除
        matrix[i].insert(0, turn)
        matrix[i].pop(-1)
        line = matrix_vertical_as_line(matrix)

    elif direction == Direction.DOWN:
        matrix = line_as_matrix_vertical(line)
        # row = 6 の場合、`matrix[5]`の末尾に挿入、先頭を削除
        matrix[i].append(turn)
        matrix[i].pop(0)
        line = matrix_vertical_as_line(matrix)

    elif direction == Direction.LEFT:
        matrix = line_as_matrix_horizontal(line)
        # row = 1 の場合、`matrix[0]`の先頭に挿入、末尾を削除
        matrix[i].insert(0, turn)
        matrix[i].pop(-1)
        line = matrix_horizontal_as_line(matrix)

    elif direction == Direction.RIGHT:
        matrix = line_as_matrix_horizontal(line)
        # row = 6 の場合、`matrix[5]`の末尾に挿入、先頭を削除
        matrix[i].append(turn)
        matrix[i].pop(0)
        line = matrix_horizontal_as_line(matrix)

    return line


def check_winner(line: list[int]):

    matrix = line_as_matrix_vertical(line)

    # 横方向に、0以外の数字が5つ連続しているかどうか
    for i in range(SIDE_LENGTH):

        grouped = [(k, list(g)) for k, g in itertools.groupby(matrix[i])]
        for k, g in grouped:
            if k == 0:
                continue

            if len(g) >= WIN_CONDITION_COUNT:
                return k

    matrix = line_as_matrix_horizontal(line)

    # 縦方向に、0以外の数字が5つ連続しているかどうか
    for i in range(SIDE_LENGTH):

        grouped = [(k, list(g)) for k, g in itertools.groupby(matrix[i])]
        for k, g in grouped:
            if k == 0:
                continue

            if len(g) >= WIN_CONDITION_COUNT:
                return k

    # 斜め方向に、0以外の数字が5つ連続しているかどうか
    # 左上から右下
    for i in range(SIDE_LENGTH - WIN_CONDITION_COUNT + 1):
        for j in range(SIDE_LENGTH - WIN_CONDITION_COUNT + 1):
            if matrix[i][j] == 0:
                continue

            if all(matrix[i + k][j + k] == matrix[i][j] for k in range(WIN_CONDITION_COUNT)):
                return matrix[i][j]

    # 右上から左下
    for i in range(SIDE_LENGTH - WIN_CONDITION_COUNT + 1):
        for j in range(SIDE_LENGTH - 1, WIN_CONDITION_COUNT - 2, -1):
            if matrix[i][j] == 0:
                continue

            if all(matrix[i + k][j - k] == matrix[i][j] for k in range(WIN_CONDITION_COUNT)):
                return matrix[i][j]

    return 0

import random

class SudokuGenerator:
    def __init__(self, row_length=9, removed_cells=30):
        self.n = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.fill_values()
        self.solution = [row[:] for row in self.board]  # Keep a copy of solution
        self.remove_cells()

    def get_board(self):
        return self.board

    def print_board(self):
        for i in range(self.n):
            print(self.board[i])

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[r][col] != num for r in range(self.n))

    def valid_in_box(self, row_start, col_start, num):
        for r in range(row_start, row_start+3):
            for c in range(col_start, col_start+3):
                if self.board[r][c] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, self.n, 3):
            self.fill_box(i, i)

    def find_empty_location(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == 0:
                    return (r, c)
        return None

    def fill_remaining(self):
        loc = self.find_empty_location()
        if not loc:
            return True  # board full
        row, col = loc
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining():
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1


def generate_sudoku(size=9, removed=30):
    generator = SudokuGenerator(size, removed)
    return generator.get_board(), generator.solution

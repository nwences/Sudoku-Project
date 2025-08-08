import pygame
import sys
from sudoku_generator import generate_sudoku

pygame.init()

WIDTH, HEIGHT = 540, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)
DARK_BLUE = (10, 25, 70)
LIGHT_BLUE = (180, 200, 255)

class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.original = value != 0

    def draw(self, screen):
        x = self.col * self.width
        y = self.row * self.height

        if self.value != 0:
            text = FONT.render(str(self.value), True, BLACK)
            screen.blit(text, (x + (self.width - text.get_width()) // 2,
                               y + (self.height - text.get_height()) // 2))
        elif self.temp != 0:
            text = SMALL_FONT.render(str(self.temp), True, GREY)
            screen.blit(text, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(screen, RED, (x, y, self.width, self.height), 3)

    def set_value(self, val):
        if not self.original:
            self.value = val

    def set_temp(self, val):
        if not self.original:
            self.temp = val

    def clear(self):
        if not self.original:
            self.value = 0
            self.temp = 0

class Board:
    def __init__(self, board, width, height):
        self.rows = 9
        self.cols = 9
        self.board = [[Cell(board[r][c], r, c, width//9, height//9) for c in range(9)] for r in range(9)]
        self.width = width
        self.height = height
        self.selected = None
        self.original = [[cell.value for cell in row] for row in self.board]

    def draw(self, screen):
        gap = self.width // 9
        for i in range(self.rows + 1):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(screen, DARK_BLUE, (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(screen, DARK_BLUE, (i * gap, 0), (i * gap, self.height), thickness)

        for row in self.board:
            for cell in row:
                cell.draw(screen)

    def select(self, row, col):
        if self.selected:
            r, c = self.selected
            self.board[r][c].selected = False

        self.board[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width // 9
            col = pos[0] // gap
            row = pos[1] // gap
            return (row, col)
        return None

    def clear(self):
        if self.selected:
            r, c = self.selected
            self.board[r][c].clear()

    def sketch(self, val):
        if self.selected:
            r, c = self.selected
            self.board[r][c].set_temp(val)

    def place_number(self, val):
        if self.selected:
            r, c = self.selected
            cell = self.board[r][c]
            if not cell.original:
                cell.set_value(val)
                cell.temp = 0

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        return [[cell.value for cell in row] for row in self.board]

    def check_board(self, solution):
        for r in range(9):
            for c in range(9):
                if self.board[r][c].value != solution[r][c]:
                    return False
        return True

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                cell = self.board[r][c]
                if not cell.original:
                    cell.value = 0
                    cell.temp = 0

def draw_start_screen(screen):
    screen.fill(LIGHT_BLUE)
    title = FONT.render("Sudoku", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

    easy_btn = pygame.Rect(WIDTH//2 - 75, 250, 150, 50)
    medium_btn = pygame.Rect(WIDTH//2 - 75, 320, 150, 50)
    hard_btn = pygame.Rect(WIDTH//2 - 75, 390, 150, 50)

    pygame.draw.rect(screen, GREEN, easy_btn)
    pygame.draw.rect(screen, BLUE, medium_btn)
    pygame.draw.rect(screen, RED, hard_btn)

    easy_text = SMALL_FONT.render("Easy", True, BLACK)
    medium_text = SMALL_FONT.render("Medium", True, BLACK)
    hard_text = SMALL_FONT.render("Hard", True, BLACK)

    screen.blit(easy_text, (easy_btn.centerx - easy_text.get_width() // 2, easy_btn.centery - easy_text.get_height() // 2))
    screen.blit(medium_text, (medium_btn.centerx - medium_text.get_width() // 2, medium_btn.centery - medium_text.get_height() // 2))
    screen.blit(hard_text, (hard_btn.centerx - hard_text.get_width() // 2, hard_btn.centery - hard_text.get_height() // 2))

    return easy_btn, medium_btn, hard_btn

def draw_buttons(screen, reset_btn, restart_btn, exit_btn):
    pygame.draw.rect(screen, RED, reset_btn)
    pygame.draw.rect(screen, RED, restart_btn)
    pygame.draw.rect(screen, RED, exit_btn)

    reset_text = SMALL_FONT.render("Reset", True, BLACK)
    restart_text = SMALL_FONT.render("Restart", True, BLACK)
    exit_text = SMALL_FONT.render("Exit", True, BLACK)

    screen.blit(reset_text, (reset_btn.centerx - reset_text.get_width() // 2, reset_btn.centery - reset_text.get_height() // 2))
    screen.blit(restart_text, (restart_btn.centerx - restart_text.get_width() // 2, restart_btn.centery - restart_text.get_height() // 2))
    screen.blit(exit_text, (exit_btn.centerx - exit_text.get_width() // 2, exit_btn.centery - exit_text.get_height() // 2))

def draw_game_over(screen, won):
    screen.fill(LIGHT_BLUE)
    text = "You Won!" if won else "Game Over!"
    msg = FONT.render(text, True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    clock = pygame.time.Clock()
    run = True

    game_state = "start"  # start, play, win, lose
    board = None
    solution = None

    easy_btn = medium_btn = hard_btn = None

    reset_btn = pygame.Rect(WIDTH//6 - 50, HEIGHT - 50, 100, 40)
    restart_btn = pygame.Rect(WIDTH//2 - 50, HEIGHT - 50, 100, 40)
    exit_btn = pygame.Rect(WIDTH * 5//6 - 50, HEIGHT - 50, 100, 40)

    while run:
        clock.tick(30)

        if game_state == "start":
            easy_btn, medium_btn, hard_btn = draw_start_screen(SCREEN)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if easy_btn.collidepoint(pos):
                        board_data, solution = generate_sudoku(9, 30)
                        board = Board(board_data, 540, 540)
                        game_state = "play"
                    elif medium_btn.collidepoint(pos):
                        board_data, solution = generate_sudoku(9, 40)
                        board = Board(board_data, 540, 540)
                        game_state = "play"
                    elif hard_btn.collidepoint(pos):
                        board_data, solution = generate_sudoku(9, 50)
                        board = Board(board_data, 540, 540)
                        game_state = "play"

            elif game_state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if reset_btn.collidepoint(pos):
                        if board:
                            board.reset_to_original()

                    elif restart_btn.collidepoint(pos):
                        game_state = "start"
                        board = None
                        solution = None

                    elif exit_btn.collidepoint(pos):
                        run = False

                    else:
                        clicked = board.click(pos)
                        if clicked:
                            board.select(*clicked)

                if event.type == pygame.KEYDOWN:
                    if board and board.selected:
                        if event.key == pygame.K_1:
                            board.sketch(1)
                        elif event.key == pygame.K_2:
                            board.sketch(2)
                        elif event.key == pygame.K_3:
                            board.sketch(3)
                        elif event.key == pygame.K_4:
                            board.sketch(4)
                        elif event.key == pygame.K_5:
                            board.sketch(5)
                        elif event.key == pygame.K_6:
                            board.sketch(6)
                        elif event.key == pygame.K_7:
                            board.sketch(7)
                        elif event.key == pygame.K_8:
                            board.sketch(8)
                        elif event.key == pygame.K_9:
                            board.sketch(9)
                        elif event.key == pygame.K_RETURN:
                            r, c = board.selected
                            cell = board.board[r][c]
                            if cell.temp != 0:
                                board.place_number(cell.temp)
                                if board.is_full():
                                    if board.check_board(solution):
                                        draw_game_over(SCREEN, True)
                                    else:
                                        draw_game_over(SCREEN, False)
                                    game_state = "start"
                                    board = None
                                    solution = None
                        elif event.key == pygame.K_BACKSPACE:
                            board.clear()

        if game_state == "play" and board:
            SCREEN.fill(LIGHT_BLUE)
            board.draw(SCREEN)
            draw_buttons(SCREEN, reset_btn, restart_btn, exit_btn)
            pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

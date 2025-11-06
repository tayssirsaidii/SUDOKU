import pygame
import copy
import random

# ========== SUDOKU CORE LOGIC ==========

def fill_grid(board):
    empty = [0, 0]
    if not find_empty_location(board, empty):
        return True
    row, col = empty
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if number_checker(board, row, col, num):
            board[row][col] = num
            if fill_grid(board):
                return True
            board[row][col] = 0
    return False

def remove_numbers(board, clues=30):
    filled_positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(filled_positions)
    to_remove = 81 - clues
    for i in range(to_remove):
        row, col = filled_positions[i]
        board[row][col] = 0

def number_checker(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + startRow][j + startCol] == num:
                return False
    return True

def find_empty_location(board, l):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                l[0] = i
                l[1] = j
                return True
    return False

def sudoku_solver(board):
    l = [0, 0]
    if not find_empty_location(board, l):
        return True
    row = l[0]
    col = l[1]
    for num in range(1, 10):
        if number_checker(board, row, col, num):
            board[row][col] = num
            if sudoku_solver(board):
                return True
            board[row][col] = 0
    return False

# ========== DANCING LINKS (DLX) ALGORITHM X FOR SUDOKU ==========

def sudoku_matrix():
    N = 9
    matrix = []
    for r in range(N):
        for c in range(N):
            for n in range(1, N+1):
                row = [0] * (4 * N * N)
                row[N*r + c] = 1
                row[N*N + N*r + (n-1)] = 1
                row[2*N*N + N*c + (n-1)] = 1
                block = (r//3)*3 + (c//3)
                row[3*N*N + N*block + (n-1)] = 1
                matrix.append(row)
    return matrix

def board_to_rows(board):
    N = 9
    rows = []
    for r in range(N):
        for c in range(N):
            num = board[r][c]
            if num != 0:
                idx = (r*N + c)*N + (num - 1)
                rows.append(idx)
    return rows

class DLXNode:
    def __init__(self):
        self.left = self.right = self.up = self.down = self
        self.column = None
        self.row_id = -1
        self.col_id = -1

class DLXColumn(DLXNode):
    def __init__(self, col_id):
        super().__init__()
        self.size = 0
        self.col_id = col_id

def build_dlx(matrix, preset_rows):
    header = DLXColumn("header")
    columns = [DLXColumn(i) for i in range(len(matrix[0]))]
    for i, col in enumerate(columns):
        col.right = columns[(i+1)%len(columns)]
        col.left = columns[(i-1)%len(columns)]
    header.right = columns[0]
    header.left = columns[-1]
    columns[0].left = header
    columns[-1].right = header
    nodes = []
    for i, row in enumerate(matrix):
        last = None
        for j, cell in enumerate(row):
            if cell:
                node = DLXNode()
                node.row_id = i
                node.col_id = j
                node.column = columns[j]
                columns[j].size += 1
                node.down = columns[j]
                node.up = columns[j].up
                columns[j].up.down = node
                columns[j].up = node
                if last:
                    node.left = last
                    node.right = last.right
                    last.right.left = node
                    last.right = node
                else:
                    node.left = node.right = node
                    first = node
                last = node
        if last:
            nodes.append(last)
    for idx in preset_rows:
        row_nodes = []
        for node in nodes:
            if node.row_id == idx:
                start = node
                while True:
                    row_nodes.append(node)
                    node = node.right
                    if node == start:
                        break
                break
        for n in row_nodes:
            cover(n.column)
    return header, columns, nodes

def cover(col):
    col.right.left = col.left
    col.left.right = col.right
    i = col.down
    while i != col:
        j = i.right
        while j != i:
            j.down.up = j.up
            j.up.down = j.down
            j.column.size -= 1
            j = j.right
        i = i.down

def uncover(col):
    i = col.up
    while i != col:
        j = i.left
        while j != i:
            j.column.size += 1
            j.down.up = j
            j.up.down = j
            j = j.left
        i = i.up
    col.right.left = col
    col.left.right = col

def search(k, solution, header, N=9):
    if header.right == header:
        return list(solution)
    c = header.right
    min_size = c.size
    col = c
    while c != header:
        if c.size < min_size:
            min_size = c.size
            col = c
        c = c.right
    cover(col)
    r = col.down
    while r != col:
        solution.append(r.row_id)
        j = r.right
        while j != r:
            cover(j.column)
            j = j.right
        result = search(k+1, solution, header)
        if result is not None:
            return result
        j = r.left
        while j != r:
            uncover(j.column)
            j = j.left
        solution.pop()
        r = r.down
    uncover(col)
    return None

def rows_to_board(sol_rows):
    N = 9
    board = [[0 for _ in range(N)] for _ in range(N)]
    for idx in sol_rows:
        r = idx // (N*N)
        rem = idx % (N*N)
        c = rem // N
        n = rem % N + 1
        board[r][c] = n
    return board

def dancing_links_solver(board):
    base_matrix = sudoku_matrix()
    preset = board_to_rows(board)
    header, columns, nodes = build_dlx(base_matrix, preset)
    sol_rows = search(0, [], header)
    if sol_rows:
        solved = rows_to_board(sol_rows)
        for i in range(9):
            for j in range(9):
                board[i][j] = solved[i][j]
        return True
    return False

# ========== UI FUNCTIONS ==========

def draw_grid(screen):
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * 60), (540, i * 60), thickness)
        pygame.draw.line(screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), thickness)

def draw_numbers(screen, board, original_board, highlight=None):
    font = pygame.font.SysFont(None, 48)
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = (0, 0, 0) if original_board[i][j] != 0 else (0, 0, 255)
                if highlight == (i, j):
                    color = (255, 0, 0)
                num_text = font.render(str(board[i][j]), True, color)
                screen.blit(num_text, (j * 60 + 20, i * 60 + 10))

def draw_buttons(screen):
    font = pygame.font.SysFont(None, 28, bold=True)
    buttons = [
        {"rect": pygame.Rect(560, 290, 200, 56), "text": "Backtracking Solve"},
        {"rect": pygame.Rect(560, 370, 200, 56), "text": "Dancing Links Solve"},
        {"rect": pygame.Rect(560, 450, 200, 56), "text": "New Puzzle"}
    
    ]
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        r = btn["rect"]
        shadow_surf = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 90))
        screen.blit(shadow_surf, (r.x + 4, r.y + 4))
        base_color = (0, 150, 255)
        if r.collidepoint(mouse_pos):
            color = (min(base_color[0] + 30, 255), min(base_color[1] + 30, 255), min(base_color[2] + 30, 255))
        else:
            color = base_color
        pygame.draw.rect(screen, color, r, border_radius=10)
        pygame.draw.rect(screen, (10, 10, 10), r, width=2, border_radius=10)
        text_surf = font.render(btn["text"], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=r.center)
        screen.blit(text_surf, text_rect)
    return buttons

def animate_solution(screen, board, solution, original_board, delay=40):
    for i in range(9):
        for j in range(9):
            if original_board[i][j] == 0:
                board[i][j] = solution[i][j]
                screen.fill((255, 255, 255))
                draw_grid(screen)
                draw_numbers(screen, board, original_board, highlight=(i, j))
                draw_buttons(screen)
                pygame.display.flip()
                pygame.time.delay(delay)

# ========== MAIN LOOP ==========

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sudoku Grid")
    clock = pygame.time.Clock()
    running = True

    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_grid(board)
    remove_numbers(board, clues=30)
    original_board = copy.deepcopy(board)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                buttons = draw_buttons(screen)
                if buttons[0]["rect"].collidepoint(mouse_pos):
                    solution = copy.deepcopy(board)
                    sudoku_solver(solution)
                    animate_solution(screen, board, solution, original_board, delay=40)
                elif buttons[1]["rect"].collidepoint(mouse_pos):
                    solution = copy.deepcopy(board)
                    dancing_links_solver(solution)
                    animate_solution(screen, board, solution, original_board, delay=40)
                elif buttons[2]["rect"].collidepoint(mouse_pos):
                    board = [[0 for _ in range(9)] for _ in range(9)]
                    fill_grid(board)
                    remove_numbers(board, clues=30)
                    original_board = copy.deepcopy(board)

        screen.fill((255, 255, 255))
        draw_grid(screen)
        draw_numbers(screen, board, original_board)
        draw_buttons(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

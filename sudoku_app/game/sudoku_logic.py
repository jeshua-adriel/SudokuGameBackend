"""
Core Sudoku engine: full-board generation, uniqueness-checked puzzle
carving, and a general solver/validator.

No external dependencies -- pure Python backtracking, which is plenty
fast for 9x9 boards.
"""
import random

SIZE = 9
BOX = 3

# Roughly how many cells stay filled (clues) per difficulty.
# Real Sudoku "difficulty" also depends on which techniques are needed
# to solve it, not just clue count, but clue count is a solid, fast
# proxy that's easy to reason about and tune.
DIFFICULTY_CLUES = {
    "easy": 42,
    "medium": 32,
    "hard": 26,
}


def _box_index(row, col):
    return (row // BOX) * BOX + (col // BOX)


def is_valid(grid, row, col, num):
    for i in range(SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    br, bc = BOX * (row // BOX), BOX * (col // BOX)
    for r in range(br, br + BOX):
        for c in range(bc, bc + BOX):
            if grid[r][c] == num:
                return False
    return True


def _find_empty(grid):
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                return r, c
    return None


def solve(grid, randomize=False):
    """Fill `grid` in place with the first solution found. Returns True/False."""
    empty = _find_empty(grid)
    if not empty:
        return True
    row, col = empty
    nums = list(range(1, 10))
    if randomize:
        random.shuffle(nums)
    for num in nums:
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if solve(grid, randomize=randomize):
                return True
            grid[row][col] = 0
    return False


def count_solutions(grid, limit=2):
    """Count solutions up to `limit` (stops early -- we only care whether
    it's exactly 1, i.e. a unique puzzle)."""
    empty = _find_empty(grid)
    if not empty:
        return 1
    row, col = empty
    count = 0
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            count += count_solutions(grid, limit - count)
            grid[row][col] = 0
            if count >= limit:
                break
    return count


def generate_full_board():
    grid = [[0] * SIZE for _ in range(SIZE)]
    solve(grid, randomize=True)
    return grid


def generate_puzzle(difficulty="medium"):
    """Returns (puzzle_grid, solution_grid). puzzle_grid has 0s for blanks.
    Uniqueness of the solution is guaranteed by only removing a clue when
    the resulting board still has exactly one solution."""
    solution = generate_full_board()
    puzzle = [row[:] for row in solution]

    clues_target = DIFFICULTY_CLUES.get(difficulty, DIFFICULTY_CLUES["medium"])
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)

    filled = SIZE * SIZE
    for (r, c) in cells:
        if filled <= clues_target:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0

        test_grid = [row[:] for row in puzzle]
        if count_solutions(test_grid, limit=2) != 1:
            # removing this clue makes the puzzle ambiguous -- put it back
            puzzle[r][c] = backup
        else:
            filled -= 1

    return puzzle, solution


def is_board_valid(grid):
    """Checks the board (which may have 0s for blanks) has no rule
    violations among the filled cells."""
    for r in range(SIZE):
        for c in range(SIZE):
            val = grid[r][c]
            if val == 0:
                continue
            grid[r][c] = 0
            valid = is_valid(grid, r, c, val)
            grid[r][c] = val
            if not valid:
                return False
    return True


def is_board_complete(grid):
    return all(grid[r][c] != 0 for r in range(SIZE) for c in range(SIZE))

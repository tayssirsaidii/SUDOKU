# Sudoku Solver with Visualization

A Python implementation of a Sudoku solver using two different algorithms: Backtracking and Dancing Links (DLX). The program provides a visual interface using Pygame to demonstrate how each algorithm solves the puzzle.

## Algorithms

### 1. Backtracking Algorithm
The backtracking algorithm works by:
- Finding an empty cell in the grid
- Trying digits 1-9 in that cell
- Checking if the digit is valid according to Sudoku rules
- Moving to the next empty cell if valid
- Backtracking (undoing) when a digit leads to an invalid solution

Key functions:
- `sudoku_solver()`: Main recursive solving function
- `number_checker()`: Validates if a number can be placed in a cell
- `find_empty_location()`: Finds the next empty cell to fill

### 2. Dancing Links (DLX) Algorithm
DLX is an efficient algorithm for solving exact cover problems. For Sudoku, it:
- Converts the Sudoku grid into an exact cover matrix
- Uses a sparse matrix representation with doubly-linked lists
- Implements Knuth's Algorithm X for finding solutions

Key components:
- `DLXNode` and `DLXColumn` classes: Represent the sparse matrix
- `build_dlx()`: Constructs the DLX data structure
- `cover()` and `uncover()`: Handle column operations
- `search()`: Implements the recursive search algorithm

## Implementation Details

### Data Structure
- The Sudoku board is represented as a 9x9 2D array
- Empty cells are represented by 0
- The DLX matrix converts Sudoku constraints into a binary matrix

### UI Features
- Interactive graphical interface using Pygame
- Grid visualization with proper Sudoku box formatting
- Three main buttons:
  - Backtracking Solve
  - Dancing Links Solve
  - New Puzzle
- Animation of solving process
- Original numbers in black, solved numbers in blue

### Visualization
- Real-time solving animation
- Highlights current cell being processed
- Clear distinction between given and solved numbers
- Smooth transitions between steps

## Usage

1. Install requirements:
```bash
pip install pygame
```

2. Run the program:
```bash
python sudoku.py
```

3. Interface controls:
- Click "New Puzzle" to generate a new Sudoku puzzle
- Click either solving method to watch the solution process
- Close window to exit

## Performance
- Backtracking: Simple but can be slower for difficult puzzles
- Dancing Links: More complex implementation but generally faster
- Both algorithms guarantee to find a solution if one exists

## Dependencies
- Python 3.x
- Pygame 2.x
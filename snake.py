import abc
import enum
import random
from typing import List, Tuple

MAX_ATTEMPTS_FIND_FRUIT = 50


class SnakeDirection(str, enum.Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4

    def opositive(self):
        if self is SnakeDirection.LEFT:
            return SnakeDirection.RIGHT
        if self is SnakeDirection.RIGHT:
            return SnakeDirection.LEFT
        if self is SnakeDirection.UP:
            return SnakeDirection.DOWN
        if self is SnakeDirection.DOWN:
            return SnakeDirection.UP


class CellType(enum.Enum):
    EMPTY = 0
    WALL = 1
    FOOD = 2
    LEFT = 3
    RIGHT = 4
    UP = 5
    DOWN = 6


class Cell(abc.ABC):
    type: CellType
    pos_x: int
    pos_y: int

    def __init__(self, x: int, y: int, type: CellType = CellType.EMPTY):
        self.pos_x = x
        self.pos_y = y
        self.type = type

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        if self.type is CellType.EMPTY:
            return "."
        if self.type is CellType.WALL:
            return "#"
        if self.type is CellType.FOOD:
            return "W"
        if self.type is CellType.UP:
            return "↑"
        if self.type is CellType.DOWN:
            return "↓"
        if self.type is CellType.LEFT:
            return "←"
        if self.type is CellType.RIGHT:
            return "→"


class Board(abc.ABC):

    cells: List[List[Cell]]
    head: Cell
    tail: Cell
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._reset_cells()

    def _reset_cells(self):
        self.cells = []
        for i in range(self.width):
            self.cells.append([])
            for j in range(self.height):
                self.cells[i].append(Cell(x=i, y=j))

    def cell_at(self, cell: Cell, direction: SnakeDirection):
        if direction is SnakeDirection.LEFT:
            return self.cells[cell.pos_x][cell.pos_y-1]
        if direction is SnakeDirection.RIGHT:
            return self.cells[cell.pos_x][cell.pos_y+1]
        if direction is SnakeDirection.UP:
            return self.cells[cell.pos_x-1][cell.pos_y]
        if direction is SnakeDirection.DOWN:
            return self.cells[cell.pos_x+1][cell.pos_y]

    def head_direction(self) -> SnakeDirection:
        return self.cell_direction_to_direction(self.head)

    def cell_direction_to_direction(self, cell: Cell) -> SnakeDirection:
        if cell.type is CellType.LEFT:
            return SnakeDirection.LEFT
        if cell.type is CellType.RIGHT:
            return SnakeDirection.RIGHT
        if cell.type is CellType.UP:
            return SnakeDirection.UP
        if cell.type is CellType.DOWN:
            return SnakeDirection.DOWN
        raise ValueError("Cell got no direction!")

    def direction_to_cell_direction(self, direction: SnakeDirection) -> CellType:
        if direction is SnakeDirection.LEFT:
            return CellType.LEFT
        if direction is SnakeDirection.RIGHT:
            return CellType.RIGHT
        if direction is SnakeDirection.UP:
            return CellType.UP
        if direction is SnakeDirection.DOWN:
            return CellType.DOWN

    def next_head_cell(self, direction: SnakeDirection) -> Cell:
        head_direction = self.head_direction()
        if direction is head_direction.opositive():
            return self.cell_at(self.head, direction)
        return self.cell_at(self.head, direction)

    def update_head(self, next_head_cell: Cell, direction: SnakeDirection):
        self.head.type = self.direction_to_cell_direction(direction)
        next_head_cell.type = self.direction_to_cell_direction(direction)
        self.head = next_head_cell

    def delete_tail(self):
        last_tail = self.tail
        self.tail = self.cell_at(
            cell=self.tail, direction=self.cell_direction_to_direction(self.tail))
        last_tail.type = CellType.EMPTY

    def get_random_cell(self) -> Cell:
        random_generation = random.Random()
        x_position: int = random_generation.randrange(1, self.width - 1)
        y_position: int = random_generation.randrange(1, self.height - 1)
        return self.cells[x_position][y_position]

    def __repr__(self) -> str:
        representation = ""
        for line in self.cells:
            for cell in line:
                representation += str(cell)
            representation += "\n"
        return representation


class Game(abc.ABC):

    board: Board

    def __init__(self, width: int, height: int) -> None:
        self.board = Board(width, height)
        self._set_random_snake()
        self._set_random_food()

    def _set_random_snake(self):
        random_cell = self.board.get_random_cell()
        self.board.head = random_cell
        self.board.tail = random_cell
        random_cell.type = CellType.RIGHT

    def _set_random_food(self):
        for _ in range(MAX_ATTEMPTS_FIND_FRUIT):
            random_cell = self.board.get_random_cell()
            if random_cell.type is CellType.EMPTY:
                random_cell.type = CellType.FOOD
                return
        raise ValueError("Could not find an empty slot in {} steps".format(
            MAX_ATTEMPTS_FIND_FRUIT))

    def next_tick(self, direction: SnakeDirection):
        next_head_cell = self.board.next_head_cell(direction)
        if next_head_cell.type is CellType.FOOD:
            self.board.update_head(next_head_cell, direction)
            self._set_random_food()
            return
        if next_head_cell.type is CellType.EMPTY:
            self.board.update_head(next_head_cell, direction)
            self.board.delete_tail()
            return
        raise ValueError("Next cell is neither food nor empty")

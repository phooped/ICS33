# queens.py
#
# ICS 33 Winter 2023
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self



Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'



class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position


    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'
class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position


    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'
class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""
    #q=queen
    #a=attacked
    #''=empty

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        self.rows = rows
        self.columns = columns
        self.board = list()

        for n in range(rows):
            self.board.append([])
            for k in range(columns):
                self.board[n].append([])



    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        count = int()
        for m in range(self.rows):
            for k in range(self.columns):
                if self.board[m][k] == 'q':
                    count += 1
        return count


    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        lst = list()
        for m in range(self.rows):
            for k in range(self.columns):
                if self.board[m][k] == 'q':
                    lst.append(Position(m,k))
        return lst


    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        for k in range(self.rows):
            for m in range(self.columns):
                if position.row == k and position.column == m and self.board[k][m] == 'q':
                    return True
        return False


    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        for k in self.queens():
            #vertical
            for m in range(self.rows):
                if m == k.row :
                    pass
                elif self.board[m][k.column] == 'q':
                    return True

            #horizontal
            for n in range(self.columns):
                if n == k.column:
                    pass
                elif self.board[k.row][n] == 'q':
                    return True

            #diagonal coordinates
            diag = list()
            for i in range(max(self.rows,self.columns)):
                if i - k.row + k.column in range(self.rows):
                    diag.append(Position(row=i,column = i - k.row + k.column))

                if k.row + k.column - i in range(self.rows):
                    diag.append(Position(row=i,column = k.row + k .column-i))


            #Check if a queen is in one of the coordinates
            while k in diag: diag.remove(k)
            if any(x in self.queens() for x in diag):
                return True
        return False
    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions.
        Raises a DuplicateQueenException when there is already a queen in at
        least one of the given positions."""
        for m in positions:
            if self.has_queen(m):
                raise DuplicateQueenError(m)
            else:
                self.board[m.row][m.column] = 'q'


    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions.
        Raises a MissingQueenException when there is no queen in at least one of
        the given positions."""
        for m in positions:
            if self.has_queen(m):
                self.board[m.row][m.column] = ''
            else:
                raise MissingQueenError(m)

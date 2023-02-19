# test_queens.py
#
# ICS 33 Winter 2023
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_zero_queen_count_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState, Position
import unittest



class TestQueensState(unittest.TestCase):
    def test_zero_queen_count_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_has_queen(self):
        state = QueensState(8,8)
        pos = Position(0,0)
        state.board[0][0] = 'q'
        self.assertEqual(state.has_queen(position = pos),True)

    def test_with_queens_added(self):
        state = QueensState(8,8)
        lstPos = [Position(0,0),Position(3,2),Position(4,1)]
        state.with_queens_added(lstPos)
        for m in lstPos:
            if state.has_queen(m):
                flag = True
        self.assertEqual(flag,True)

    def test_with_queens_added_exception(self):
        state = QueensState(8, 8)
        lstPos = [Position(0, 0), Position(3, 2), Position(4, 1)]
        state.board[0][0] = 'q'
        try:
            state.with_queens_added(lstPos)
        except Exception as e:
            errorMessage = f'duplicate queen in row {0} column {0}'
            if str(e) == errorMessage:
                correctMessage = True
            raised = True
        self.assertEqual(raised and correctMessage,True)

    def test_with_queens_removed(self):
        state = QueensState(8,8)
        lstPos = [Position(0, 0), Position(3, 2), Position(4, 1)]

        state.with_queens_added(lstPos)
        state.with_queens_removed(lstPos)

        for m in lstPos:
            if not state.has_queen(m):
                flag = True
        self.assertEqual(flag,True)

    def test_with_queens_removed_exception(self):
        state = QueensState(8,8)
        lstPos = [Position(0, 0)]
        try:
            state.with_queens_removed(lstPos)
        except Exception as e:
            errorMessage = f'missing queen in row {0} column {0}'
            if str(e) == errorMessage:
                correctMessage = True
            raised = True
        self.assertEqual(raised and correctMessage, True)

    def test_queen_count_filled(self):
        state = QueensState(8,8)
        lstPos = [Position(0, 0), Position(3, 2), Position(4, 1)]
        state.with_queens_added(lstPos)
        self.assertEqual(len(lstPos) == state.queen_count(),True)

    def test_queens_return_correct(self):
        state = QueensState(8, 8)
        lstPos = [Position(0, 0), Position(3, 2), Position(4, 1)]
        state.with_queens_added(lstPos)
        self.assertEqual(lstPos == state.queens(),True)

    def test_any_queens_unsafe_vertical(self):
        state = QueensState(8, 8)
        state.board[0][0]='q'
        state.board[1][0]='q'
        state.board[2][0]='q'
        self.assertEqual(state.any_queens_unsafe(),True)

    def test_any_queens_unsafe_horizontal(self):
        state = QueensState(8, 8)
        state.board[0][0] = 'q'
        state.board[0][1] = 'q'
        state.board[0][2] = 'q'
        self.assertEqual(state.any_queens_unsafe(), True)

    def test_any_queens_unsafe_diagonal(self):
        state = QueensState(8, 8)
        lstPos = [Position(1,1),Position(3,3),Position(0,6)]
        state.with_queens_added(lstPos)
        self.assertEqual(state.any_queens_unsafe(), True)

    def test_any_queens_unsafe_safe(self):
        state = QueensState(8, 8)
        state.board[7][7]='q'
        state.board[6][5]='q'
        self.assertEqual(state.any_queens_unsafe(), False)


if __name__ == '__main__':
    unittest.main()

import unittest
from TicTacToePractice import *

class TestsTicTacToe(unittest.TestCase):
    def test_check_win(self):
        self.assertTrue(check_win([1, 0, 0, 0, 1, 0, 0, 0, 1], 1))
        self.assertTrue(check_win([1, 1, 1, 0, 0, 0, 0, 0, 0], 1))
        self.assertFalse(check_win([1, 0, 1, 0, 1, 0, 0, 1, 0], 1))
    def test_check_win_sect(self):
        self.assertFalse(check_win_sect(0, [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0]], [0, 0, 0, 0, 0, 0, 0, 0, 0], 1))
        self.assertTrue(check_win_sect(2, [[1, 1, 1, 0, 0, 0, 0, 0, 0],
                                            [1, 1, 1, 0, 0, 0, 0, 0, 0],
                                            [1, 1, 1, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0]], [1, 1, 0, 0, 0, 0, 0, 0, 0], 1))
    def test_heuristic_function(self):
        self.assertEqual(heuristic_function([1, 1], [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 1, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0]], 1, [0, 0, 0, 0, 0, 0, 0, 0, 0]), 3)
        self.assertEqual(heuristic_function([0, 0], [[1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 0, 0]], 1, [1, 0, 0, 0, 1, 0, 0, 0, 0]), 100)


if __name__ == '__main__':
    unittest.main()
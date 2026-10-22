"""File names shared by chess_scan.py, ablation.py and summarize.py."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# boards of task 1 (normal play); their tempo_detail_<board>.json is the normal-play one
TASK1 = ['cyl:5x4', 'cyl:3x7', 'cyl:5x7', 'cyl:3x8', 'cyl:4x7', 'cyl:4x8',
         'flat:4x6', 'flat:3x7', 'cyl:2x6', 'cyl:2x8', 'cyl:6x7']


def tag(board):
    return board.replace(':', '_')


def chess_detail_path(board):
    """tempo_detail_<board>.json for the task 2 boards (as the brief says); tempo_detail_chess_<board>.json for the
    extra chess runs on boards that also belong to task 1, so that the two files cannot overwrite each other."""
    name = ('tempo_detail_chess_%s.json' if board in TASK1 else 'tempo_detail_%s.json') % tag(board)
    return os.path.join(HERE, name)

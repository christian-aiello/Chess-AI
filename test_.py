import pytest, main

game = main.game


def test_perft():
    game.generate_board()
    assert game.perft(3) == 8902
    game.generate_board("r3k2r/p6p/8/B7/1pp1p3/3b4/P6P/R3K2R w KQkq - 0 1")
    assert game.perft(3) == 6666
    game.generate_board("8/5p2/8/2k3P1/p3K3/8/1P6/8 b - - 0 1")
    assert game.perft(3) == 795
    game.generate_board("8/k1P5/8/1K6/8/8/8/8 w - - 0 1")
    assert game.perft(5) == 10857
    game.generate_board("8/5pP1/8/2k5/4K3/8/pP6/8 b - - 0 1")
    assert game.perft(3) == 1896

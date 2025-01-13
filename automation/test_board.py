import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game import Game

@pytest.fixture
def setup_game():
    return Game()

@pytest.mark.usefixtures("setup_game")
def test_red_wins_row(setup_game):
    game = setup_game
    for col in range(4): 
        game.column_click(col)
        if col < 3:
            game.column_click(col + 4) 
    assert game.current_game_state == "win"


@pytest.mark.usefixtures("setup_game")
def test_blue_wins_row(setup_game):
    game = setup_game
    for col in range(4): 
        game.column_click(col // 2 + 4) 
        game.column_click(col)
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_red_wins_column(setup_game):
    game = setup_game
    for col in range(4):  # Red fills the first column
        game.column_click(0)
        if col < 3:
            game.column_click(1)  # Blue plays elsewhere
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_blue_wins_column(setup_game):
    game = setup_game
    for col in range(4):  # Blue fills the second column
        game.column_click(col // 2 + 4)  # Red plays elsewhere
        game.column_click(1)
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_red_wins_diagonal_right(setup_game):
    game = setup_game
    game.column_click(0)
    game.column_click(1)
    game.column_click(1)
    game.column_click(2)
    game.column_click(2)
    game.column_click(3)
    game.column_click(2)
    game.column_click(3)
    game.column_click(3)
    game.column_click(4)
    game.column_click(3)
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_blue_wins_diagonal_right(setup_game):
    game = setup_game
    game.column_click(6)
    game.column_click(0)
    game.column_click(1)
    game.column_click(1)
    game.column_click(2)
    game.column_click(2)
    game.column_click(3)
    game.column_click(2)
    game.column_click(3)
    game.column_click(3)
    game.column_click(4)
    game.column_click(3)
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_red_wins_diagonal_left(setup_game):
    game = setup_game
    game.column_click(4)
    game.column_click(3)
    game.column_click(3)
    game.column_click(2)
    game.column_click(2)
    game.column_click(1)
    game.column_click(2)
    game.column_click(1)
    game.column_click(1)
    game.column_click(0)
    game.column_click(1)
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_blue_wins_diagonal_left(setup_game):
    game = setup_game
    game.column_click(6)
    game.column_click(4)
    game.column_click(3)
    game.column_click(3)
    game.column_click(2)
    game.column_click(2)
    game.column_click(1)
    game.column_click(2)
    game.column_click(1)
    game.column_click(1)
    game.column_click(0)
    game.column_click(1)
    assert game.current_game_state == "win"

@pytest.mark.usefixtures("setup_game")
def test_tie(setup_game):
    game = setup_game
    for col in [0, 1, 2, 4, 5]:
        for row in range(6):
            game.column_click(col)

    for row in range(5):
        game.column_click(6)

    for row in range(6):
        game.column_click(3)

    game.column_click(6)

    assert game.current_game_state == "draw"
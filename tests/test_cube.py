import pytest
import numpy as np
from rubiks.cube import RubiksCube

def test_initial_state_is_solved():
    cube = RubiksCube(size=3)
    # Each face should have the same value across all stickers
    for face in cube.state:
        assert len(set(face)) == 1, f"Face not uniform: {face}"

def test_face_rotation_changes_face():
    cube = RubiksCube(size=3)
    original = cube.state.copy()
    cube.rotate_face('F', clockwise=True)
    assert not np.array_equal(original, cube.state), "State should change after face rotation"

def test_scramble_changes_state():
    cube = RubiksCube(size=3)
    original = cube.state.copy()
    cube.scramble(moves=1)
    assert not np.array_equal(original, cube.state), "State should change after scramble"

def test_invalid_face_rotation_raises():
    cube = RubiksCube(size=3)
    with pytest.raises(ValueError):
        cube.rotate_face('X')  # Invalid face

def test_rotation_is_deterministic():
    cube1 = RubiksCube(size=3)
    cube2 = RubiksCube(size=3)
    cube1.rotate_face('L', clockwise=False)
    cube2.rotate_face('L', clockwise=False)
    assert np.array_equal(cube1.state, cube2.state), "Same rotation should result in same state"

def test_is_not_solved_after_scramble():
    cube = RubiksCube(size=3)
    cube.scramble(moves=19)
    assert not cube.is_solved(), "Cube should not be solved after scramble"
    
def test_is_solved_after_reset():
    cube = RubiksCube(size=3)
    cube.scramble(moves=19)
    cube = RubiksCube(size=3)  # Reset to solved state
    assert cube.is_solved(), "Cube should be solved after reset"

def test_is_solved_after_undoing_move():
    cube = RubiksCube(size=3)
    cube.rotate_face('U', clockwise=True)
    cube.rotate_face('U', clockwise=False)  # Undo the move
    assert cube.is_solved(), "Cube should be solved after undoing the move"

import pytest
from src.analysis.angle import calculate_angle
def test_straight_arm_is_180():
    assert calculate_angle((0,0),(1,0),(2,0))==pytest.approx(180)
def test_right_angle_is_90():
    assert calculate_angle((0,1),(0,0),(1,0))==pytest.approx(90)
def test_fully_loaded_is_0():
    assert calculate_angle((1,0),(0,0),(1,0))==pytest.approx(0)
def test_works_in_3d():
    assert calculate_angle((0,0,1),(0,0,0),(0,1,0))==pytest.approx(90)
def test_same_point_returns_none():
    assert calculate_angle((1,1),(1,1),(2,2)) is None
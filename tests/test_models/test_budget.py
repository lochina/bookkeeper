import pytest
from bookkeeper.models.budget import Budget

def test_create_budget():
    b = Budget(sum=100, budget=200)
    assert b.sum == 100
    assert b.budget == 200
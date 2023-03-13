from datetime import date

import pytest

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense

DB_NAME = 'test.db'

@pytest.fixture
def custom_class():
    return Expense



@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(DB_NAME, custom_class)


def test_create_with_full_args_list():
    e = Expense(amount=100, category=1, expense_date=date.today(),
                added_date=date.today(), comment='test', pk=1)
    assert e.amount == 100
    assert e.category == 1


def test_create_brief():
    e = Expense(100, 1)
    assert e.amount == 100
    assert e.category == 1


def test_can_add_to_repo(repo):
    e = Expense(100, 1)
    pk = repo.add(e)
    assert e.pk == pk

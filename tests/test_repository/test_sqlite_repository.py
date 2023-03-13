from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass
import pytest

DB_NAME = 'test.db'

@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        test_field: str = 'abc'

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(DB_NAME, custom_class)


def test_add_get_and_delete(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    o = repo.get(5555)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    assert o is None
    repo.delete(pk)
    assert repo.get(pk) is None

def test_get_all(repo, custom_class):
    obj_1 = custom_class
    obj_2 = custom_class
    repo.add(obj_1)
    repo.add(obj_2)
    for item in repo.get_all():
        assert item.pk >= 0
        assert item.test_field == 'abc'
    assert repo.get_all()[-1].pk == repo.get_all()[-2].pk + 1

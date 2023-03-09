import sqlite3

from inspect import get_annotations
from typing import List, Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from datetime import date
from dataclasses import field


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.create()

#TODO: проверить, создается ли список категорий и таблица расходов без simple client

    def create(self) -> None:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({names})')
    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({names})') #creates a table if it doesn't exist
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk


    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE id = {pk}')
            result = cur.fetchone()

        con.close()
        return result

    def get_all(self, where: dict[str, any] | None = None) -> list[list[Any]]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if type(where) == type(dict()):
                column_name = list(where.keys())[0]
                condition = list(where.values())[0]
                if condition == 'today':
                    cur.execute(f'SELECT * FROM {self.table_name} WHERE DATE({column_name}) = DATE()')
                elif condition == 'week':
                    params = ('now', '-7 days')
                    cur.execute(f'SELECT * FROM {self.table_name} WHERE DATE({column_name}) > DATE(?, ?)', params)
                elif condition == 'month':
                    params = ('now', '-30 days')
                    cur.execute(f'SELECT * FROM {self.table_name} WHERE DATE({column_name}) > DATE(?, ?)', params)
                else:
                    cur.execute(f'SELECT * FROM {self.table_name} WHERE {column_name} = {condition}')
            else:
                cur.execute(f'SELECT * FROM {self.table_name}')
            result =  [list(x) for x in cur.fetchall()]#cur.fetchall()

        con.close()
        print(result)
        return result

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'UPDATE {self.table_name} SET ({names}) VALUES ({p}) WHERE id = {obj.pk}', values)
            result = cur.fetchone()

        con.close()
        return result

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'DELETE FROM {self.table_name} WHERE id = {pk}')

        con.close()
        return None
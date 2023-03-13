"""
Модуль содержит описание sql-репозитория

Репозиторий реализует хранение объектов определенного класса в файле
с базой данных.
"""
import sqlite3
from inspect import get_annotations
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):
    """
        Класс реализует создание базы данных, добавление,
        обновление, получение и удаление из нее объектов.
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                query = f'CREATE TABLE {self.table_name} ' \
                        f'("pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(query)
        con.close()

    def add(self, obj: T) -> int:
        """ Добавление объекта в базу, возвращает pk """
        names = ', '.join(self.fields.keys())
        number_of_values = ', '.join('?' * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({number_of_values})',
                values
            )
            obj.pk = cur.lastrowid
            con.commit()
        con.close()
        return obj.pk

    def __generate_object(self, db_row: tuple) -> T:
        """ Создание объекта Т из строки базы данных """
        obj = self.cls(self.fields)
        for field, value in zip(self.fields, db_row[1:]):
            setattr(obj, field, value)
        obj.pk = db_row[0]
        return obj

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name} WHERE pk = {pk}')
            row = cur.fetchone()
        con.close()

        if row is None:
            return None

        return self.__generate_object(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if isinstance(where, dict):
                column_name = list(where.keys())[0]
                condition = list(where.values())[0]
                if condition == 'today':
                    cur.execute(f'SELECT * FROM {self.table_name}'
                            f'WHERE DATE({column_name}) = DATE()')
                elif condition == 'week':
                    params = ('now', '-7 days')
                    cur.execute(f'SELECT * FROM {self.table_name}'
                    f'WHERE DATE({column_name}) > DATE(?, ?)', params)
                elif condition == 'month':
                    params = ('now', '-30 days')
                    cur.execute(f'SELECT * FROM {self.table_name} WHERE'
                    f'DATE({column_name}) > DATE(?, ?)', params)
                else:
                    cur.execute(f'SELECT * FROM {self.table_name} WHERE {column_name} = {condition}')
            else:
                cur.execute(f'SELECT * FROM {self.table_name}')
            rows = cur.fetchall()

        con.close()
        if not rows:
            return None

        return [self.__generate_object(row) for row in rows]

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        names = ', '.join(self.fields.keys())
        number_of_values = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'UPDATE {self.table_name} SET ({names}) VALUES'
                        f' ({number_of_values}) WHERE pk = {obj.pk}', values)
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')
        con.close()

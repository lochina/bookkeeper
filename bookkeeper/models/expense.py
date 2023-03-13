"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float = 0.0
    category: int = 0
    expense_date: date = field(default_factory=date.today)
    added_date: date = field(default_factory=date.today)
    comment: str = ''
    pk: int = 0

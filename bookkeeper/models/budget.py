"""
Описан класс, представляющий бюджет
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    sum: потраченная сумма
    budget: бюджет
    """
    sum: float
    budget: float

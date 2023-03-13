"""
Модуль содержит представление таблицы расходов и списка категорий.
Реализует функции обновления таблицы расходов и списка категорий,
а также нажатий на кнопки "Добавить", "Удалить" и "Редактировать".
"""

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

class ExpensePresenter:
    """
        Соединяет базы данных, окна программы и модель.
        Обрабатывает нажатия на кнопки.
    """
    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = None
        self.cat_repo = SQLiteRepository[Category]('test.db', Category)
        self.cat_data = cat_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_expense_delete_button_clicked(self.handle_expense_delete_button_clicked)
        self.view.on_category_edit_button_clicked(self.handle_category_edit_button_clicked)

    def update_expense_data(self):
        """
            Обновить данные в таблице расходов. Если таблицы нет, создать.
            Присвоить имена категориям в таблице (по сравнению pk).
        """
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data is None:
            self.view.set_expense_table(self.exp_data)
        else:
            for exspense in self.exp_data:
                for category in self.cat_data:
                    if category.pk == exspense.category:
                        exspense.category = category.name
                        break
            self.view.set_expense_table(self.exp_data)

    def update_cat_data(self):
        """
            Создать список категорий. Обновить его при редактировании.
        """
        if self.cat_data == None:
            self.create_cat_repo()
            self.cat_data = self.cat_repo.get_all()
    def create_cat_repo(self):
        """
            Создает репозиторий категорий из дерева.
        """
        cats = '''
        продукты
            мясо
                сырое мясо
                мясные продукты
            сладости
        книги
        одежда
        '''.splitlines()
        Category.create_from_tree(read_tree(cats), self.cat_repo)
    def show(self):
        """
            Отрисовка окна.
        """
        self.view.show()
        self.update_cat_data()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        """
            Если кнопка "Добавить" нажата, считать введенную стоимость,
            категорию из списка, добавить в базу данных, обновить таблицу.
        """
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(amount, cat_pk)
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_expense_delete_button_clicked(self) -> None:
        """
            Удаление выбранных ячеек таблицы из базы данных.
        """
        selected = self.view.get_selected_expenses()
        if selected:
            for expense in selected:
                self.exp_repo.delete(expense)
            self.update_expense_data()

    def handle_category_edit_button_clicked(self):
        """
            Если нажата кнопка "Редактировать", выводим диалоговое окно.
        """
        self.view.show_cats_dialog(self.cat_data)

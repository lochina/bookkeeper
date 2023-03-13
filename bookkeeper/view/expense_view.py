"""
Модуль содержит описание окна приложения.

Таблица расходов реализуется с помощью TableModel.
"""
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout
from PySide6.QtWidgets import QComboBox, QLineEdit, QPushButton
from PySide6 import QtWidgets
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from bookkeeper.view.categories_view import CategoryDialog

class TableModel(QAbstractTableModel):
    """
        Модель таблицы.
    """
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.header_names = list(data[0].__dataclass_fields__.keys())

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Написать заголовки в таблице """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        """ Получить данные по индексу"""
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index):
        """ длина внешнего списка"""
        return len(self._data)

    def columnCount(self, index):
        """ длина внутреннего списка (первого) """
        return len(self._data[0].__dataclass_fields__)

class MainWindow(QMainWindow):
    """
        Основное окно. Отрисовка виджетов. Реализоция функционала виджетов.
    """
    def __init__(self):
        super().__init__()

        self.item_model = None
        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(500, 600)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.budget_table = QtWidgets.QTableWidget(3, 3)
        self.budget_table.setColumnCount(3)
        self.budget_table.setRowCount(3)
        self.budget_table.setHorizontalHeaderLabels(
            " :Сумма :Бюджет".split(':'))
        header_2 = self.budget_table.horizontalHeader()
        header_2.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header_2.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header_2.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        self.budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.budget_table.verticalHeader().hide()
        self.budget_table.setItem(0, 0, QTableWidgetItem('День'))
        self.budget_table.setItem(1, 0, QTableWidgetItem('Неделя'))
        self.budget_table.setItem(2, 0, QTableWidgetItem('Месяц'))
        self.layout.addWidget(self.budget_table)

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.expense_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 2, 2)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data):
        """ задает таблицу расходов """
        if data:
            self.item_model = TableModel(data)
            self.expenses_grid.setModel(self.item_model)
            self.expenses_grid.resizeColumnsToContents()

    def set_budget_table(self, data):
        """
            Задает таблицу бюджета, заполняет бюджет
            на день и неделю в зависимости от месячного бюджета.
        """
        budget_month = 30000
        self.budget_table.setItem(2, 2, QTableWidgetItem(str(budget_month)))
        self.budget_table.setItem(1, 2, QTableWidgetItem(str(budget_month/4)))
        self.budget_table.setItem(0, 2, QTableWidgetItem(str(budget_month/30)))
        sum_today = 0
        if data:
            for item in data:
                sum_today += item.amount
        self.budget_table.setItem(0, 1, QTableWidgetItem(str(sum_today)))

    def set_budget_table_week_budget(self, data):
        """ Считает потраченную сумму за неделю """
        sum_week = 0
        if data:
            for item in data:
                sum_week += item.amount
        self.budget_table.setItem(1, 1, QTableWidgetItem(str(sum_week)))

    def set_budget_table_month_budget(self, data):
        """ Считает потраченную сумму за месяц """
        sum_month = 0
        if data:
            for item in data:
                sum_month += item.amount
        self.budget_table.setItem(2, 1, QTableWidgetItem(str(sum_month)))

    def set_category_dropdown(self, data):
        """ Задает выпадающий список """
        for c in data:
            self.category_dropdown.addItem(c.pk)# должно быть c.name, c.pk,

    def on_expense_add_button_clicked(self, slot):
        """ Добавить расход """
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot):
        """ Удалить расход """
        self.expense_delete_button.clicked.connect(slot)

    def get_amount(self) -> float:
        """ Получить стоимость """
        return float(self.amount_line_edit.text())

    def __get_selected_row_indices(self) -> list[int]:
        """ Получить индексы выделенных строк """
        return list(set([qmi.row() for qmi in
                         self.expenses_grid.selectionModel().selection().indexes()]))

    def get_selected_expenses(self) -> list[int] | None:
        """ Получить выбранные расходы """
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        return [self.item_model._data[i].pk for i in idx]

    def get_selected_cat(self) -> int:
        """ Выбрать категорию """
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def on_category_edit_button_clicked(self, slot):
        """ Нажать на редактирование категорий """
        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, data):
        """ Диалоговое окно с редактированием категорий """
        if data:
            cat_dlg = CategoryDialog(data)
            cat_dlg.setWindowTitle('Редактирование категорий')
            cat_dlg.setGeometry(300, 100, 600, 300)
            cat_dlg.exec_()

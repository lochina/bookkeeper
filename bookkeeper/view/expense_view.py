from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role=Qt.DisplayRole) -> str:
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                return str(self._data[index.row()][index.column()])

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def setData(self, index, value, role) -> bool:
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class MainWindow(QMainWindow):
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
        #self.budget_grid = QtWidgets.QTableView()
        #self.budget_grid.resizeColumnsToContents()
        #self.layout.addWidget(self.budget_grid)
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
        # budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.budget_table.verticalHeader().hide()
        self.budget_table.setItem(0, 0, QTableWidgetItem('День'))
        self.budget_table.setItem(1, 0, QTableWidgetItem('Неделя'))
        self.budget_table.setItem(2, 0, QTableWidgetItem('Месяц'))
        self.layout.addWidget(self.budget_table)


        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)  # TODO: добавить валидатор
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data):
        self.item_model = TableModel(data)
        self.expenses_grid.setModel(self.item_model)

    def set_budget_table(self, data):
        budget_month = 30000
        self.budget_table.setItem(2, 2, QTableWidgetItem(str(budget_month)))
        self.budget_table.setItem(1, 2, QTableWidgetItem(str(budget_month/4)))
        self.budget_table.setItem(0, 2, QTableWidgetItem(str(budget_month/30)))
        sum_today = 0
        for item in data:
            sum_today += item[0]
        self.budget_table.setItem(0, 1, QTableWidgetItem(str(sum_today)))

    def set_budget_table_week_budget(self, data):
        sum_week = 0
        for item in data:
            sum_week += item[0]
        self.budget_table.setItem(1, 1, QTableWidgetItem(str(sum_week)))

    def set_budget_table_month_budget(self, data):
        sum_month = 0
        for item in data:
            sum_month += item[0]
        self.budget_table.setItem(2, 1, QTableWidgetItem(str(sum_month)))


    def set_category_dropdown(self, data):
        for tup in data:
            self.category_dropdown.addItem(tup[0], tup[1])

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())  # TODO: обработка исключений


    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())
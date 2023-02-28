import sys
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from PySide6 import QtWidgets
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QDateEdit, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table view demo")
        layout = QVBoxLayout()
        expenses_table = QtWidgets.QTableWidget(4, 20)
        expenses_table.setColumnCount(4)
        expenses_table.setRowCount(20)
        expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        #expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        expenses_table.verticalHeader().hide()

        def set_data(data: list[list[str]]):
            for i, row in enumerate(data):
                for j, x in enumerate(row):
                    expenses_table.setItem(
                        i, j,
                        QtWidgets.QTableWidgetItem(x.capitalize())
                    )
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        layout.addWidget(QtWidgets.QLabel(f'Последние расходы'))
        layout.addWidget(expenses_table)

        layout.addWidget(QtWidgets.QLabel(f'Бюджет'))
        budget_table = QtWidgets.QTableWidget(3, 3)
        budget_table.setColumnCount(3)
        budget_table.setRowCount(3)
        budget_table.setHorizontalHeaderLabels(
            " :Сумма :Бюджет".split(':'))
        header_2 = budget_table.horizontalHeader()
        header_2.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header_2.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header_2.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        #budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        budget_table.verticalHeader().hide()
        layout.addWidget(budget_table)

        layout.addWidget(QtWidgets.QLabel(f'Сумма'))
        sum = QtWidgets.QLineEdit()
        layout.addWidget(sum)

        layout.addWidget(QtWidgets.QLabel(f'Категория'))
        category = QtWidgets.QComboBox()
        layout.addWidget(category)

        button_change = QtWidgets.QPushButton('Редактировать')
        button_add = QtWidgets.QPushButton('Добавить')
        layout.addWidget(button_change)
        layout.addWidget(button_add)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
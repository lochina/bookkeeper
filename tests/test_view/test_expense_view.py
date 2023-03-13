from bookkeeper.view.expense_view import MainWindow
from pytestqt.qt_compat import qt_api
from PySide6.QtCore import Qt

def test_input_expense(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.amount_line_edit, '123')
    assert widget.amount_line_edit.text() == '123'
    assert widget.get_amount() == 123

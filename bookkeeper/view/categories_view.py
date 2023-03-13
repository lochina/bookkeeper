"""
Модуль содержит описание диалогового окна
с иерархией категорий.

"""
from collections import deque
from PySide6.QtWidgets import QDialog, QTreeView, QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem

class CategoryDialog(QDialog):
    """
        Отрисовка окна, связь данных с моделью дерева
    """
    def __init__(self, data):
        super(CategoryDialog, self).__init__()
        self.tree = QTreeView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        data = [{'category_name': c.name, 'parent_id': c.parent, 'unique_id': c.pk,} for c in data]
        print(data)
        self.import_data(data)
        self.tree.expandAll()


    def import_data(self, data, root=None):
        """
            Реализует связь представления данных категорий
            с моделью дерева.
        """
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}   # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['parent_id'] is None:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['category_name'])
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

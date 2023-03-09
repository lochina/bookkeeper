from bookkeeper.models.budget import Budget
from datetime import date
from dataclasses import field

class BudgetPresenter:

    def __init__(self, model, view, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = self.exp_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def update_budget_data(self):
        self.exp_data = self.exp_repo.get_all({"expense_date": "today"})
        self.view.set_budget_table(self.exp_data)

    def update_week_budget_data(self):
        self.exp_data = self.exp_repo.get_all({"expense_date": "week"})
        self.view.set_budget_table_week_budget(self.exp_data)

    def update_month_budget_data(self):
        self.exp_data = self.exp_repo.get_all({"expense_date": "month"})
        self.view.set_budget_table_month_budget(self.exp_data)

    def show(self):
        self.view.show()
        self.update_budget_data()
        self.update_week_budget_data()
        self.update_month_budget_data()

    def handle_expense_add_button_clicked(self):
        self.update_budget_data()
        self.update_week_budget_data()
        self.update_month_budget_data()


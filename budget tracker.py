import csv
from tabulate import tabulate
from datetime import datetime

class BudgetTracker:
    def __init__(self, filename):
        self.filename = filename
        self.transactions = self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                transactions = [transaction for transaction in reader]
            return transactions
        except FileNotFoundError:
            return []

    def save_transactions(self):
        with open(self.filename, 'w', newline='') as file:
            fieldnames = ['Date', 'Type', 'Category', 'Amount']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction)

    def add_transaction(self, transaction_type, category, amount):
        date = datetime.now().strftime('%Y-%m-%d')
        self.transactions.append({
            'Date': date,
            'Type': transaction_type,
            'Category': category,
            'Amount': amount
        })
        self.save_transactions()
        print("Transaction added successfully.")

    def calculate_budget(self):
        income = sum(float(txn['Amount']) for txn in self.transactions if txn['Type'] == 'Income')
        expenses = sum(float(txn['Amount']) for txn in self.transactions if txn['Type'] == 'Expense')
        return income - expenses

    def analyze_expenses(self):
        expenses = {txn['Category']: 0 for txn in self.transactions if txn['Type'] == 'Expense'}
        for txn in self.transactions:
            if txn['Type'] == 'Expense':
                expenses[txn['Category']] += float(txn['Amount'])

        print("Expense Analysis:")
        print(tabulate(expenses.items(), headers=['Category', 'Total Amount']))

def main():
    filename = 'transactions.csv'
    budget_tracker = BudgetTracker(filename)

    while True:
        print("\nBudget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Calculate Budget")
        print("4. Analyze Expenses")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            category = input("Enter income category: ")
            amount = input("Enter income amount: ")
            budget_tracker.add_transaction('Income', category, amount)
        elif choice == '2':
            category = input("Enter expense category: ")
            amount = input("Enter expense amount: ")
            budget_tracker.add_transaction('Expense', category, amount)
        elif choice == '3':
            budget = budget_tracker.calculate_budget()
            print(f"Remaining Budget: {budget}")
        elif choice == '4':
            budget_tracker.analyze_expenses()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

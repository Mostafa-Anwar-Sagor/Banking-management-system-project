import random

class Bank:
    def __init__(self):
        self.users = []
        self.loans = {}
        self.is_loan_enabled = True
        self.highest_loan_amount = 0  

    def create_account(self, name, email, address, account_type, account_number, password):
        user = User(name, email, address, account_type, account_number, password)
        self.users.append(user)
        return user

    def delete_account(self, user):
        self.users.remove(user)

    def get_user_by_account_number(self, account_number):
        for user in self.users:
            if user.account_number == account_number:
                return user
        return None

    def authenticate_user(self, identifier, password):
        for user in self.users:
            if (user.account_number == identifier or user.email == identifier) and user.password == password:
                return user
        return None

    def total_balance(self):
        total = 0
        for user in self.users:
            total += user.balance
        return total

    def total_loan_amount(self):
        return sum(self.loans.values())

    def toggle_loan_feature(self):
        self.is_loan_enabled = not self.is_loan_enabled

    def __str__(self):
        return f"Total Balance: {self.total_balance()}, Total Loan Amount: {self.total_loan_amount()}, Loan Feature: {'Enabled' if self.is_loan_enabled else 'Disabled'}, Highest Loan Amount: {self.highest_loan_amount}"

class User:
    def __init__(self, name, email, address, account_type, account_number, password):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = account_number
        self.password = password
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")
        print("Deposit successful.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrew: {amount}")
            print("Withdrawal successful.")

    def transfer(self, amount, recipient):
        if self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.transactions.append(f"Transferred: {amount} to {recipient.name}")
            recipient.transactions.append(f"Received: {amount} from {self.name}")
            print(f"Successfully sent {amount} to {recipient.name}.")
        else:
            print("Insufficient balance")

    def take_loan(self, amount, bank):
        if bank.is_loan_enabled:
            if len(self.transactions) <= 3:
                self.balance += amount
                bank.loans[self.account_number] = amount
                self.transactions.append(f"Loan Taken: {amount}")
                if amount > bank.highest_loan_amount:
                    bank.highest_loan_amount = amount
                print(" Loan successful.")
                print("Loan amount granted:", bank.highest_loan_amount)
            else:
                print("Maximum loan limit reached")
        else:
            print("Loan feature is currently disabled")

    def check_balance(self):
        return self.balance

    def transaction_history(self):
        return self.transactions

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Address: {self.address}, Account Type: {self.account_type}, Account Number: {self.account_number}, Balance: {self.balance}"

class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, address, account_type, account_number, password):
        user = self.bank.create_account(name, email, address, account_type, account_number, password)
        print("Account created successfully.")
        return user

    def delete_account(self, user):
        self.bank.delete_account(user)

    def list_all_accounts(self):
        return self.bank.users

    def total_balance(self):
        return self.bank.total_balance()

    def total_loan_amount(self):
        return self.bank.total_loan_amount()

    def toggle_loan_feature(self):
        self.bank.toggle_loan_feature()

def main():
    bank = Bank()
    admin = Admin(bank)

    while True:
        print("\nWelcome to the Banking Management System")
        print("1. User")
        print("2. Admin")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_interface(bank)
        elif choice == "2":
            admin_menu(admin)
        elif choice == "3":
            print("Thank you for using our system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def user_interface(bank):
    print("\nWELCOME TO SM BANK LTD:")
    print("1. Create New Account")
    print("2. Login Existing Account")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        account_type = input("Enter account type (Savings/Current): ")
        account_number = int(input("Type your favourite account number: "))
        password = input("Set your password: ")
        user = bank.create_account(name, email, address, account_type, account_number, password)
        print(f"Welcome {name} to SM LTD Banking system.")
        user_menu(bank, user) 
    elif choice == "2":
        identifier = input("Enter your account number or email address: ")
        password = input("Enter your password: ")
        user = bank.authenticate_user(identifier, password)
        if user:
            print(f"Welcome back {user.name}.")
            user_menu(bank, user)
        else:
            print("Authentication failed. Invalid account number, email address, or password.")
    else:
        print("Invalid choice. Please try again.")
        user_interface(bank)


def user_menu(bank, user):
    print("\nSelect your Menu:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transfer")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Take Loan")
    print("7. Logout")

    choice = input("Enter your choice: ")

    if choice == "1":
        amount = float(input("Enter deposit amount: "))
        user.deposit(amount)
    elif choice == "2":
        amount = float(input("Enter withdrawal amount: "))
        user.withdraw(amount)
    elif choice == "3":
        recipient_account = int(input("Enter recipient's account number: "))
        recipient = bank.get_user_by_account_number(recipient_account)
        if recipient:
            amount = float(input("Enter transfer amount: "))
            user.transfer(amount, recipient)
        else:
            print("Recipient account does not exist.")
    elif choice == "4":
        print("Your current balance:", user.check_balance())
    elif choice == "5":
        print("Transaction History:")
        for transaction in user.transaction_history():
            print(transaction)
    elif choice == "6":
        amount = float(input("Enter loan amount: "))
        user.take_loan(amount, bank)
    elif choice == "7":
        return
    else:
        print("Invalid choice. Please try again.")
    user_menu(bank, user)

def admin_menu(admin):
    password = input("Enter admin password: ")  
    if password == "admin":
        while True:
            print("\nAdmin Menu:")
            print("1. Create Account")
            print("2. Delete Account")
            print("3. List All Accounts")
            print("4. Total Balance")
            print("5. Total Loan Amount")
            print("6. Loan Feature")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter user's name: ")
                email = input("Enter user's email: ")
                address = input("Enter user's address: ")
                account_type = input("Enter account type (Savings/Current): ")
                account_number = int(input("Enter account number: "))
                password = input("Enter password: ")
                admin.create_account(name, email, address, account_type, account_number, password)
            elif choice == "2":
                account_number = int(input("Enter account number to delete: "))
                user = admin.bank.get_user_by_account_number(account_number)
                if user:
                    admin.delete_account(user)
                    print("Account deleted successfully.")
                else:
                    print("User not found.")
            elif choice == "3":
                print("All Accounts:")
                for user in admin.list_all_accounts():
                    print(user)
            elif choice == "4":
                print("Total Balance:", admin.total_balance())
            elif choice == "5":
                print("Total Loan Amount:", admin.total_loan_amount())
            elif choice == "6":
                admin.toggle_loan_feature()
                print("Loan feature is off.")
            elif choice == "7":
                return
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Incorrect admin password.")
if __name__ == "__main__":
    main()

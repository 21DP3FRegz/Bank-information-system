import setup

from functions import *
from datetime import *
from console import *
from validation import *
from get_functions import *
from client import Client
from account import Account
from transaction import Transaction
from colors import Colors


def register_user() -> Client:
    clear()
    print("\n======== Create Account =========\n")

    login: str = get_valid_login()
    password: str = get_valid_password()
    password = hash_password(password)

    new_client = Client(
        login=login,
        password=password,
    )
    new_client.save()
    return new_client


def sign_in_user() -> Client:
    clear()
    print("\n========= Login Page ===========")

    get_login = lambda: input("\n" + Colors.BLUE + "Username" + Colors.END + " : ").strip().lower()

    clients = Client.get_clients()
    logins = [client.login for client in clients]

    login: str = get_login()
    while login not in logins:
        print(Colors.FAIL + "This username does not excists!" + Colors.END)
        login = get_login()

    user: Client = next((client for client in clients if client.login == login), None)

    password: str = get_password("\n" + Colors.BLUE + "Password" + Colors.END + " : ")
    while not verify_password(password, user.password):
        if password != '':
            print(Colors.FAIL + "Wrong password!" + Colors.END)
        password = get_password("\n" + Colors.BLUE + "Password" + Colors.END + " : ")
    return user


def sort_accounts(accounts: list[Account]) -> list[Account]:
    while True:
        clear()
        choises = ['Sort by name', 'Sort by balance', 'Sort by date']
        print_menu(choises)

        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            sorted_accounts = sorted(accounts, key=lambda account: account.name)
            return sorted_accounts if sorted_accounts != accounts else sorted_accounts[::-1]

        if answer == '2':
            sorted_accounts = sorted(accounts, key=lambda account: account.balance)
            return sorted_accounts if sorted_accounts != accounts else sorted_accounts[::-1]
        
        if answer == '3':
            sorted_accounts = sorted(accounts, key=lambda account: account.date_opened)
            return sorted_accounts if sorted_accounts != accounts else sorted_accounts[::-1]


def filter_accounts_by_name(accounts: list[Account]) -> list[Account]:
    while True:
        clear()
        print("Please enter the name of the account or the string that it can contain:")
        answer: str = input(">>> ").lower()
        
        specific_account = next((account for account in accounts if account.name == answer), None)
        if not specific_account is None:
            return [specific_account]
        else:
            return list(filter(lambda account: (answer in account.name.lower()), accounts))


def filter_transactions(user: Client) -> list[Transaction]:
    account: Account = user.choose_account("Select the account whose transactions you want to view\n>>> ")
    transactions: list[Transaction] = account.get_transactions()
    
    while True:
        clear()
        print('Select what You want to view:\n')
        
        choises = ['Sent transactions', 'Received transactions', 'Both']
        print_menu(choises)
        
        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            return list(filter(lambda transaction : account.is_transaction_sender(transaction), transactions))
        elif answer == '2':
            return list(filter(lambda transaction : account.is_transaction_recipient(transaction), transactions))
        elif answer == '3':
            return transactions


def sort_transaction(transactions: list[Transaction]) -> list[Transaction]:
    while True:
        clear()
        choises = ['Sort by amount', 'Sort by date']
        print_menu(choises)

        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            sorted_transactions = sorted(transactions, key=lambda transaction: transaction.amount)
            return sorted_transactions if sorted_transactions != transactions else sorted_transactions[::-1]

        if answer == '2':
            sorted_transactions = sorted(transactions, key=lambda transaction: transaction.date)
            return sorted_transactions if sorted_transactions != transactions else sorted_transactions[::-1]


def accounts_summary(accounts: list[Account]) -> list[Account]:
    clear()
    total_balance = sum(account.balance for account in accounts)
    summary: list[dict] = [{"Account count": len(accounts), "Total balance": str(total_balance) + ' $'}]
    print_table(summary)
    input("\nPress Enter to exit...")
    return accounts


def accounts_page(user: Client) -> None:
    clear()
    accounts = user.get_accounts()
    if accounts == []:
        print(Colors.WARNING + "You do not have a bank account at the moment." + Colors.END)
        answer: str = input("\nDo You want to create one? " + Colors.BLUE + "[Y/n]\n" + Colors.END).lower().strip()
        if answer == 'y' or answer == '':
            user.create_account()
            accounts = user.get_accounts()
    
    while True:
        clear()
        if accounts == []:
            print('\nNothing here\n')
        
        accounts_info: list[dict] = [{"name": account.name, "balance": str(account.balance) + ' $', "day_oppened": account.date_opened, "id": account.id} for account in accounts]
        print_table(accounts_info)

        choises = ['Sort', 'Filter', 'Refresh', 'Deposit', 'Summary', 'Back']
        print_menu(choises)
        
        answer: str = input("\nEnter Your choise : ")
        
        options = {
            '1': lambda: sort_accounts(accounts),
            '2': lambda: filter_accounts_by_name(user.get_accounts()),
            '3': lambda: user.get_accounts(),
            '4': lambda: user.make_deposit(),
            '5': lambda: accounts_summary(accounts),
        }

        action = options.get(answer)
        if action:
             accounts = action()
        elif answer == '6':
            return


def transaction_summary(user: Client, transactions: list[Transaction]) -> list[Transaction]:
    clear()
    all_transactions_count = len(user.get_transactions())
    all_income: float = user.count_income(datetime.min)
    
    last_year_transactions_count = all_transactions_count - len(user.get_transactions(datetime.today() - timedelta(days=365)))
    last_year_income: float = user.count_income(datetime.today() - timedelta(days=365))
    
    last_month_transactions_count = all_transactions_count - len(user.get_transactions(datetime.today() - timedelta(days=31)))
    last_month_income: float = user.count_income(datetime.today() - timedelta(days=31))
    
    summary: list[dict] = [{"Transaction count": all_transactions_count, "income": str(all_income) + ' $', "Period": 'All Time'},
                           {"Transaction count": last_year_transactions_count, "income": str(last_year_income) + ' $', "Period": 'Last Year'},
                           {"Transaction count": last_month_transactions_count, "income": str(last_month_income) + ' $', "Period": 'Last Month'}]
    
    print_table(summary)
    
    input("\nPress Enter to exit...")
    
    return transactions


def transactions_page(user: Client):
    clear()
    transactions = user.get_transactions()
    if transactions == []:
            print(Colors.WARNING + 'No transactions were found!' + Colors.END)
            input('\nEnter space to return to the home page...\n')
            return
    
    while True:
        clear()
        if len(transactions) == 0:
            print('\nNothing here\n')
        
        transactions_info: list[dict] = []
        for transaction in transactions:
            transactions_info.append({"amount": f'{str(transaction.amount)}$', "from": transaction.sender, "to": transaction.recipient, "date": str(transaction.date), "information": transaction.info})

        print_table(transactions_info)

        choises = ['Filter', 'Sort', 'Refresh', 'Summary', 'Back']
        print_menu(choises)
        
        answer: str = input("\nEnter Your choise : ")
        
        options = {
            '1': lambda: filter_transactions(user),
            '2': lambda: sort_transaction(transactions),
            '3': lambda: user.get_transactions(),
            '4': lambda: transaction_summary(user, transactions)
        }
        
        action = options.get(answer)
        if action:
             transactions = action()
        elif answer == '5':
            return
    

def main():
    clear()
    print("Welcome!".center(50))
    print("\n[" + Colors.BLUE + "1" + Colors.END + "] Sing/In")
    print("[" + Colors.BLUE + "2" + Colors.END + "] Registration")

    answer: str = input("\nEnter Your choise : ")
    if answer == "1":
        user: Client = sign_in_user()
    elif answer == "2":
        user: Client = register_user()
    else:
        return main()

    while True:
        clear()
        print("\n======== Home page =========\n")
        print("[" + Colors.BLUE + "1" + Colors.END + "] View My Accounts")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Create New Account")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Delete Account")
        print("[" + Colors.BLUE + "4" + Colors.END + "] My Transactions")
        print("[" + Colors.BLUE + "5" + Colors.END + "] New Transaction")
        print("[" + Colors.BLUE + "6" + Colors.END + "] Exit")
        
        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            accounts_page(user)
        elif answer == '2':
            user.create_account()
        elif answer == '3':
            user.delete_account()
        elif answer == '4':
            transactions_page(user)
        elif answer == '5':
            user.make_transaction()
        elif answer == '6':
            clear()
            break


if __name__ == "__main__":
    main()

import setup

import string
import maskpass  # to hide the password

from console import clear
from client import Client
from account import Account
from transaction import Transaction
from colors import Colors


def get_natural_number(message: str, min_value=1) -> int:
    while True:
        try:
            num = int(input(message))
        except ValueError:
            print(Colors.FAIL + "Please enter the numbers!" + Colors.END)
            continue
        if num < min_value:
            print(Colors.WARNING + "Please enter valid number!" + Colors.END)
            continue
        return num


def get_password(message: str) -> str:
    try:
        return maskpass.advpass(message).strip()
    except KeyboardInterrupt:
        pass


def get_valid_login() -> str:
    get_user_input = lambda: input("\n" + Colors.BLUE + "Username" + Colors.END + " : ").strip().lower()
    logins: list = [client.login for client in Client.get_clients()]
    while True:
        login: str = get_user_input()
        if(login in logins):
            print(Colors.WARNING + "This Username already excist! "  + Colors.END + "Please pick another one!")
            continue
        if(not set(login).isdisjoint(set(string.punctuation))):
            print(Colors.WARNING + "Please do not use special symbols!" + Colors.END)
            continue
        if len(login) < 4:
            print(Colors.WARNING + "Username must be 4 symbols or more!" + Colors.END)
            continue
        return login


def get_valid_password() -> str:
    while True:
        password: str = get_password("\n" + Colors.BLUE + "Password" + Colors.END + " : ")
        if len(password) < 6:
            print(Colors.WARNING + "Password must be at least 6 symbols!" + Colors.END)
            continue
        if password != get_password("\n" + Colors.BLUE + "Confirm Password" + Colors.END + " : "):
            print(Colors.FAIL + "Passwords are different!" + Colors.END)
            continue
        return password


def print_table(dicts: list[dict]) -> None:
    if len(dicts) == 0:
        return
    for key in dicts[0].keys():
        print('{:25s}'.format(str(key).replace('_', ' ').capitalize()), end='')
    print('\n' + '-' * 25 * len(dicts[0]))
    for dict in dicts:
        for value in dict.values():
            print('{:25s}'.format(value), end='')
            print(' '*9 if Colors.END in value else '', end='')
        print()
    print('-' * 25 * len(dicts[0]) + '\n')


def register_user() -> Client:
    clear()
    print("\n======== Create Account =========\n")

    login: str = get_valid_login()
    password: str = get_valid_password()

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
    while password != user.password:
        if password != '':
            print(Colors.FAIL + "Wrong password!" + Colors.END)
        password = get_password("\n" + Colors.BLUE + "Password" + Colors.END + " : ")
    return user


def sort_accounts(accounts: list[Account]) -> list[Account]:
    while True:
        clear()
        print("\n[" + Colors.BLUE + "1" + Colors.END + "] Sort by name")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Sort by balance")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Sort by date")

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


def sort_accounts(accounts: list[Account]) -> list[Account]:
    while True:
        clear()
        print("\n[" + Colors.BLUE + "1" + Colors.END + "] Sort by name")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Sort by balance")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Sort by date")

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
    account = user.choose_account("Select the account whose transactions you want to view\n>>> ")
    transactions = account.get_transactions()
    
    while True:
        clear()
        print('Select what You want to view:\n')
        print("[" + Colors.BLUE + "1" + Colors.END + "] Sent transactions")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Received transactions")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Both")
        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            return list(filter(lambda transaction: account.__is_transaction_sender(transaction), transactions))
        elif answer == '2':
            return list(filter(lambda transaction: account.__is_transaction_recipient(transaction), transactions))
        elif answer == '3':
            return transactions


def sort_transaction(transactions: list[Transaction]) -> list[Transaction]:
    while True:
        clear()
        print("\n[" + Colors.BLUE + "1" + Colors.END + "] Sort by amount")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Sort by date")

        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            sorted_transactions = sorted(transactions, key=lambda transaction: transaction.amount)
            return sorted_transactions if sorted_transactions != transactions else sorted_transactions[::-1]

        if answer == '2':
            sorted_transactions = sorted(transactions, key=lambda transaction: transaction.date)
            return sorted_transactions if sorted_transactions != transactions else sorted_transactions[::-1]


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
        
        accounts_info: list[dict] = [{"name": account.name, "balance": str(account.balance) + ' $', "day_oppened": str(account.date_opened), "id": account.id} for account in accounts]
        
        print_table(accounts_info)

        print("[" + Colors.BLUE + "1" + Colors.END + "] Sort")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Search")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Refresh")
        print("[" + Colors.BLUE + "4" + Colors.END + "] Make a Deposit")
        print("[" + Colors.BLUE + "5" + Colors.END + "] Back")

        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            accounts = sort_accounts(accounts)
        elif answer == '2':
            accounts = filter_accounts_by_name(user.get_accounts())
        elif answer == '3':
            accounts = user.get_accounts()
        elif answer == '4':
            user.make_deposit()
            accounts = user.get_accounts()
        elif answer == '5':
            return


def transactions_page(user: Client):
    clear()
    transactions = user.get_transactions()
    if transactions == []:
            print(Colors.WARNING + 'No transactions were found!' + Colors.END)
            input('\nEnter space to return to the home page...\n')
            return
    
    while True:
        clear()
        if transactions == []:
            print('\nNothing here\n')
        
        transactions_info: list[dict] = []
        for transaction in transactions:
            transactions_info.append({"amount": f'{str(transaction.amount)}$', "from": transaction.sender, "to": transaction.recipient, "date": str(transaction.date), "information": transaction.info})

        print_table(transactions_info)

        print("[" + Colors.BLUE + "1" + Colors.END + "] Filter")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Sort")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Refresh")
        print("[" + Colors.BLUE + "4" + Colors.END + "] Back")

        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            transactions = filter_transactions(user)
        elif answer == '2':
            transactions = sort_transaction(transactions)
        elif answer == '3':
            transactions = user.get_transactions()
        elif answer == '4':
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

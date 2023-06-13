from console import clear
from validation import *
from colors import Colors
from id import ID
from savable import Savable
from account import Account
from transaction import Transaction

FILE = "clients.txt"


class Client(Savable):
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def save(self) -> None:
        super().save(FILE)

    def get_accounts(self) -> list[Account]:
        return list(filter(lambda account: self.__is_mine_account(account), Account.get_accounts()))
    
    def get_transactions(self):
        transactions: list = []
        for account in self.get_accounts():
            transactions.extend(account.get_transactions())
        return transactions

    def create_account(self) -> Account:
        clear()
        print("\n======== Create Account ==========\n")
        new_account = Account(
            id=ID.create(16),
            holder=self.login,
            name=input("Create a name for this account:\n").replace(':', '')
        )
        new_account.save()
        return new_account
    
    def delete_account(self) -> None:
        account_to_delete: Account = self.choose_account("\nWhich account do you want to delete?\n>>> ")
        if account_to_delete is None:
            return
        
        id_to_delete = account_to_delete.id
        Account.delete_accont_by_id(id_to_delete)
    
    def choose_account(self, message: str, warning: str = '') -> Account:
        accounts = self.get_accounts()
        if accounts == []:
            print(Colors.WARNING + "You do not have a bank account at the moment." + Colors.END)
            answer: str = input("\nDo You want to create one? " + Colors.BLUE + "[Y/n]\n" + Colors.END).lower().strip()
            if answer == 'y' or answer == '':
                self.create_account()
                accounts = self.get_accounts()
            else:
                return None
        
        clear()
        [print("[" + Colors.BLUE, i+1, Colors.END + "]", account.name) for i, account in enumerate(accounts)]
        print("[" + Colors.BLUE + " B " + Colors.END + "] Back\n")
        print(warning)
        answer: str = input(message).strip().lower()
        
        if answer == 'b':
            return None
        if not answer.isdecimal():
            return self.choose_account(message, warning=Colors.WARNING + "Please input numbers!" + Colors.END)
        
        index: int = int(answer) - 1
        if not 0 <= index < len(accounts):
            return self.choose_account(message, warning=Colors.WARNING + "Index out of range!" + Colors.END)
        return accounts[index]
    
    def make_deposit(self) -> None:
        clear()    
        account: Account = self.choose_account("\nWhich account do you want to deposit into?\n>>> ")
        if account is None:
            return self.get_accounts()

        while True:
            amount = input("Enter the deposit amount: ")
            if is_float(amount) and float(amount) > 0:
                break
            print(Colors.WARNING + "The deposit amount should be a positive number." + Colors.END + " Try again.")
            
        account.update_balance(float(amount))
        return self.get_accounts()
    
    def make_transaction(self) -> None:
        clear()
        print("\n======== New Transaction ==========\n")
        
        account: Account = self.choose_account("\nWhich account do you want to use?\n>>> ")
        if account is None:
            return
        
        transaction_info = input("\nEnter a transaction description: ").replace(':', '')
        print("\nIf id of the recipient will be " + Colors.WARNING + "incorrect" + Colors.END + ", you will simply lose your money")
        recipient = input("Enter the id of the recipient of the transaction: ").replace(':', '')
        while True:     # get amount
            amount = input("\nEnter the transaction amount: ")
            if not is_float(amount) or float(amount) < 0:
                print(Colors.WARNING + "The transaction amount should be a positive number." + Colors.END + " Try again.")
                continue
            if float(amount) > account.balance:
                print(Colors.WARNING + "You don't have that much money." + Colors.END)
                continue
            amount = float(amount)
            break
        
        transaction = Transaction(
            None,
            amount=amount,
            recipient = recipient,
            sender = account.id,
            info=transaction_info,
        )
        transaction.save()
        account.update_balance(-amount)
        Account.update_accounts_balance()
    
    def count_income(self, period) -> float:
        return round(sum(account.count_income(period) for account in self.get_accounts()), 2)
    
    @staticmethod
    def get_clients() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            clients = list()
            for line in file.readlines():
                login, password = line.strip('\n').split(':')
                clients.append(Client(login, password))
            return clients

    def __is_mine_account(self, account: Account) -> bool:
        return True if account.holder == self.login else False

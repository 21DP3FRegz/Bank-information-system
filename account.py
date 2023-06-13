import datetime

from savable import Savable
from transaction import Transaction
from colors import Colors

FILE = "accounts.txt"


class Account(Savable):
    def __init__(
            self,
            id: str,
            holder: str,
            name: str,
            date_opened = datetime.date.today(),
            balance: float = 0
        ):
        self.id = id
        self.holder = holder
        self.balance = balance
        self.date_opened = date_opened
        self.name = name

    def save(self) -> None:
        super().save(FILE)
    
    def update_balance(self, amount: float) -> None:
        self.balance += amount
        self.balance = round(self.balance, 2)
        Account.delete_accont_by_id(self.id)
        self.save()
    
    def get_transactions(self) -> list[Transaction]:
        transactions = []
        for transaction in Transaction.get_transactions():
            is_mine = False
            if self.is_transaction_recipient(transaction):
                transaction.recipient = Colors.BLUE + self.name + Colors.END
                is_mine = True
            elif self.is_transaction_sender(transaction):
                transaction.sender = Colors.BLUE + self.name + Colors.END
                is_mine = True
            if is_mine:
                transactions.append(transaction)
        return transactions

    @staticmethod
    def delete_accont_by_id(id: str) -> None:
        with open(FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(FILE, "w", encoding="utf-8") as f:
            for line in lines:
                account_id = str(line.split(':')[0])
                if account_id != id:
                    f.write(line)

    @staticmethod
    def get_accounts() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            accounts = list()
            for line in file.readlines():
                id, holder, balance, date_opened, name = line.strip('\n').split(':')
                date_opened = datetime.datetime.strptime(date_opened.replace('-', ''), "%Y%m%d").strftime("%Y-%m-%d")
                accounts.append(Account(id, holder, name, date_opened, float(balance)))
            return accounts
    
    @staticmethod
    def update_accounts_balance() -> None:
        accounts = Account.get_accounts()
        last_transaction = Transaction.get_transactions()[-1]
        for account in accounts:
            if account.is_transaction_recipient(last_transaction):
                account.update_balance(last_transaction.amount)

    def count_income(self) -> float:
        return sum(transaction.amount if self.is_transaction_recipient(transaction) else -transaction.amount for transaction in self.get_transactions())

    def is_transaction_sender(self, transaction: Transaction) -> bool:
        return transaction.sender == self.id or transaction.sender == Colors.BLUE + self.name + Colors.END
    
    def is_transaction_recipient(self, transaction: Transaction) -> bool:
        return transaction.recipient == self.id or transaction.sender == Colors.BLUE + self.name + Colors.END

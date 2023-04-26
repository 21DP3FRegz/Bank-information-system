import datetime

from savable import Savable
from transaction import Transaction

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
    
    def get_my_transactions(self) -> list[Transaction]:
        return list(filter(lambda transaction: self.__is_my_transaction(transaction), Transaction.get_transactions()))

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
            if account.__is_transaction_recipient(last_transaction):
                account.update_balance(last_transaction.amount)
    
    def __is_my_transaction(self, transaction: Transaction) -> bool:
        return self.__is_transaction_sender(transaction) or self.__is_transaction_recipient(transaction)

    def __is_transaction_sender(self, transaction: Transaction) -> bool:
        return True if transaction.sender == self.id else False
    
    def __is_transaction_recipient(self, transaction: Transaction) -> bool:
        return True if transaction.recipient == self.id else False


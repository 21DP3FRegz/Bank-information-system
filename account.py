import datetime

from savable import Savable

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

    @staticmethod
    def delete_accont_by_id(id: str):
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

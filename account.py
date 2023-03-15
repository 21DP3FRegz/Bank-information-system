import datetime
from id import ID

FILE = "accounts.txt"


class Account:
    def __init__(
            self,
            holder: str,
            name: str,
            id: str = ID.create(16),
            date_opened = datetime.date.today(),
            balance: int = 0
        ):
        self.id = id
        self.holder = holder
        self.balance = balance
        self.date_opened = date_opened
        self.name = name

    def save(self) -> None:
        with open(FILE, 'a', encoding="utf-8") as file:
            file.write(":".join(str(value) for value in self.__dict__.values()) + "\n")

    @staticmethod
    def get_accounts() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            accounts = list()
            for line in file.readlines():
                id, holder, balance, date_opened, name = line.replace('\n', '').split(':')
                date_opened = datetime.datetime.strptime(date_opened.replace('-', ''), "%Y%m%d").strftime("%Y-%m-%d")
                accounts.append(Account(holder, name, id, date_opened, int(balance)))
            return accounts

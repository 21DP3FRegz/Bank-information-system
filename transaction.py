import datetime

from savable import Savable
from id import ID

FILE = "transactions.txt"


class Transaction(Savable):
    def __init__(
            self,
            id: str,
            amount: float,
            recipient: str,
            sender: str,
            info: str,
            date = datetime.date.today(),
        ):
        if id == None:
            id = ID.auto_increment(FILE)
        self.id = id
        self.amount = amount
        self.recipient = recipient
        self.sender = sender
        self.info = info
        self.date = date

    def save(self) -> None:
        super().save(FILE)
        
    @staticmethod
    def get_transactions() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            transactions = list()
            for line in file.readlines():
                id, amount, recipient, sender, info, date = line.strip('\n').split(':')
                date = datetime.datetime.strptime(date.replace('-', ''), "%Y%m%d").strftime("%Y-%m-%d")
                transactions.append(Transaction(id, float(amount), recipient, sender, info, date))
            return transactions

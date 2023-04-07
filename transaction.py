import datetime

from savable import Savable

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
        self.id = id
        self.amount = amount
        self.recipient = recipient
        self.sender = sender
        self.info = info
        self.date = date

    def save(self) -> None:
        super().save(FILE)
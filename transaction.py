import datetime


class Transaction:
    def __init__(self, amount: float):
        self.amount = amount
        self.date = datetime.date.today()


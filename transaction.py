import datetime


class Transaction:
    def __init__(self, amount: float):
        self.date = datetime.date.today()
        self.amount = amount

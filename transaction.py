import datetime


class Transaction:
    def __init__(self, amount: float) -> None:
        self.id = self.__create_id()
        self.date = datetime.date.today()
        self.amount = amount

    def __create_id(self) -> int:
        ...

import datetime


class Account:
    def __init__(self, name: str, holder: str, account_type: str) -> None:
        self.id = self.__create_id()
        self.date_opened = datetime.date.today()

        self.holder = holder
        self.name = name
        self.type = account_type
        self.details = None

    def __create_id(self) -> int:
        ...

    def add_details(self) -> None:
        ...

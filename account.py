import datetime
from id import ID


class Account:
    def __init__(self, name: str, holder: str, account_type: str):
        self.id = ID.create(16)
        self.date_opened = datetime.date.today()

        self.holder = holder
        self.name = name
        self.type = account_type
        self.details = None

    def add_details(self) -> None:
        ...

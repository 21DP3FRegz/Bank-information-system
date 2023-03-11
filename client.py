import os.path

FILE = "clients.txt"


class Client:
    def __init__(self, login: str, password: str, name: str, phone: int = None, email: str = None):
        self.login = login
        self.password = password
        self.name = name
        self.phone = phone
        self.email = email

    def save(self) -> None:
        with open(FILE, 'a', encoding="utf-8") as file:
            file.write(":".join(value if value is not None else "n\\a" for value in self.__dict__.values()) + "\n")

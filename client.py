FILE = "clients.txt"


class Client:
    def __init__(self, login: str, password: str, name: str, age: int):
        self.login = login
        self.password = password
        self.name = name
        self.age = age

    def save(self) -> None:
        with open(FILE, 'a', encoding="utf-8") as file:
            file.write(":".join(str(value) for value in self.__dict__.values()) + "\n")

    @staticmethod
    def get_clients() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            clients = list()
            for line in file.readlines():
                login, password, name, age = line.replace('\n', '').split(':')
                clients.append(Client(login, password, name, int(age)))
            return clients

from account import Account

FILE = "clients.txt"


class Client:
    def __init__(self, login: str, password: str, name: str, age: int):
        self.login = login
        self.password = password
        self.name = name
        self.age = age

    def save(self) -> None:
        with open(FILE, 'a', encoding="utf-8") as file:
            file.write(":".join(str(value) for value in self.__dict__.values()) + "\n") # "login:password:name:age\n" foreach client

    def create_account(self) -> Account:
        print("\n======== Create Account ==========")
        new_account = Account(
            holder=self.login,
            name=input("\nCreate a name for this account:\n")
        )
        new_account.save()
        return new_account
    
    def delete_account():
        ...
    
    def get_accounts(self) -> list:
        accounts = list(filter(lambda account: self.__is_mine(account), Account.get_accounts()))
        return accounts

    @staticmethod
    def get_clients() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            clients = list()
            for line in file.readlines():
                login, password, name, age = line.replace('\n', '').split(':')
                clients.append(Client(login, password, name, int(age)))
            return clients

    def __is_mine(self, account: Account) -> bool:
        return True if account.holder == self.login else False

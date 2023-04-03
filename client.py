from console import clear
from account import Account
from colors import Colors
from id import ID

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

    def get_accounts(self) -> list:
        accounts = list(filter(lambda account: self.__is_mine(account), Account.get_accounts()))
        return accounts

    def create_account(self) -> Account:
        clear()
        print("\n======== Create Account ==========\n")
        new_account = Account(
            id=ID.create(16),
            holder=self.login,
            name=input("Create a name for this account:\n")
        )
        new_account.save()
        return new_account
    
    def delete_account(self, warning='') -> None:
        clear()
        print("\n======== Delete Account ==========\n")
        print()
        answer: str = self.choose_account(warning + "Enter number of account you want to delete : ")

        accounts = self.get_accounts()
        if answer == 'b':
            return
        if not answer.isdecimal():
            return self.delete_account(warning=Colors.WARNING + "Please input numbers!" + Colors.END)
        
        index: int = int(answer) - 1
        
        if not 0 <= index < len(accounts):
            return self.delete_account(warning=Colors.WARNING + "Index out of range!" + Colors.END)

        account_to_delete: Account = accounts[index]
        id_to_delete = account_to_delete.id
        Account.delete_accont_by_id(id_to_delete)
    
    def choose_account(self, message: str) -> Account:
        accounts = self.get_accounts()
        [print("[" + Colors.BLUE, i+1, Colors.END + "]", account.name) for i, account in enumerate(accounts)]
        print("[" + Colors.BLUE + " B " + Colors.END + "] Back")
        return input(message).strip().lower()
    
    @staticmethod
    def get_clients() -> list:
        with open(FILE, 'r', encoding="utf-8") as file:
            clients = list()
            for line in file.readlines():
                login, password, name, age = line.strip('\n').split(':')
                clients.append(Client(login, password, name, int(age)))
            return clients

    def __is_mine(self, account: Account) -> bool:
        return True if account.holder == self.login else False

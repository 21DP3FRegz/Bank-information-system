import os

from account import Account
from colors import Colors


FILE = "clients.txt"
clear = lambda: os.system('cls') if os.name == "nt" else os.system('clear')


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
        clear()
        print("\n======== Create Account ==========\n")
        new_account = Account(
            holder=self.login,
            name=input("Create a name for this account:\n")
        )
        new_account.save()
        return new_account
    
    def delete_account(self):
        clear()
        print("\n======== Delete Account ==========\n")
        accounts = self.get_accounts()
        [print("[" + Colors.BLUE, i+1, Colors.END + "]", account.name) for i, account in enumerate(accounts)]
        print("[" + Colors.BLUE + " B " + Colors.END + "] Back")
        answer: str = input("\nWhich one account You want to delete : ").strip().lower()

        if answer == 'b':
            return
        try:
            answer: int = int(answer)
        except:
            return self.delete_account()
        
        if not 0 < answer <= len(accounts):
            return self.delete_account()

        account_to_delete: Account = accounts[answer-1]
        id_to_delete = account_to_delete.id
        Account.delete_accont_by_id(id_to_delete)
    
    def get_accounts(self) -> list:
        accounts = list(filter(lambda account: self.__is_mine(account), Account.get_accounts()))
        return accounts

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

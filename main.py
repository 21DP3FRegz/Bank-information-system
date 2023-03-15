import os
import maskpass  # to hide the password

from client import Client
from account import Account


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'


clear = lambda: os.system('cls')


def register_user() -> Client:
    clear()
    print("\n======== Create Account =========")

    get_login = lambda: input("\n" + colors.BLUE + "Username" + colors.END + " : ").strip().lower()
    get_password = lambda: maskpass.advpass("\n" + colors.BLUE + "Password" + colors.END + " : ").strip()

    name: str = input("\n" + colors.BLUE + "Name" + colors.END + " : ").strip()
    age: int = int(input("\n" + colors.BLUE + "Age" + colors.END + " : "))

    # get username
    logins: list = [client.login for client in Client.get_clients()]
    while True:
        login: str = get_login()

        if len(login) < 4:
            print(colors.WARNING + "Username is too short!" + colors.END)
            continue

        if login in logins:
            print(colors.FAIL + "This username is already taken!" + colors.END)
            continue
        break

    # get password
    while True:
        password: str = get_password()

        if len(password) < 4:
            print(colors.WARNING + "Password is too short!" + colors.END)
            continue

        if password != maskpass.advpass("\n" + colors.BLUE + "Confirm password" + colors.END + " : ").strip():
            print(colors.FAIL + "Password are different!" + colors.END)
            continue
        break

    new_client = Client(
        login=login,
        password=password,
        name=name,
        age=age
    )

    clear()
    print(colors.GREEN + "\nYou are successfully registered!\n" + colors.END)

    new_client.save()
    return new_client


def sign_in_user() -> Client:
    clear()
    print("\n========= Login Page ===========")

    get_login = lambda: input("\n" + colors.BLUE + "Username" + colors.END + " : ").strip().lower()
    get_password = lambda: maskpass.advpass("\n" + colors.BLUE + "Password" + colors.END + " : ").strip()

    clients = Client.get_clients()
    logins = [client.login for client in clients]

    login: str = get_login()
    while login not in logins:
        print(colors.FAIL + "This username does not excists!" + colors.END)
        login = get_login()
    
    user: Client = next((client for client in clients if client.login == login), None)  # returns 1st user with login == login

    password: str = get_password()
    while password != user.password:
        print(colors.FAIL + "Wrong password!" + colors.END)
        password = get_password()

    return user


def main():
    clear()
    print("Welcome!".center(50))
    print("\n[" + colors.BLUE + "1" + colors.END + "] Sing in")
    print("[" + colors.BLUE + "2" + colors.END + "] Registration")
    
    answer: str = input()
    if answer == "1":
        user: Client = sign_in_user()
    elif answer == "2":
        user: Client = register_user()
    else:
        exit()
    
    clear()
    user.create_account()
    clear()
    print(*[account.__dict__.values() for account in Account.get_accounts()], sep="\n")


if __name__ == "__main__":
    main()

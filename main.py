import os
import maskpass  # to hide the password

from client import Client
from colors import Colors

clear = lambda: os.system('cls') if os.name == "nt" else os.system('clear')


def register_user() -> Client:
    clear()
    print("\n======== Create Account =========")

    get_login = lambda: input("\n" + Colors.BLUE + "Username" + Colors.END + " : ").strip().lower()
    get_password = lambda: maskpass.advpass("\n" + Colors.BLUE + "Password" + Colors.END + " : ").strip()

    name: str = input("\n" + Colors.BLUE + "Name" + Colors.END + " : ").strip()
    age: int = int(input("\n" + Colors.BLUE + "Age" + Colors.END + " : "))

    # get valid username
    logins: list = [client.login for client in Client.get_clients()]
    while True:
        login: str = get_login()

        if len(login) < 4:
            print(Colors.WARNING + "Username is too short!" + Colors.END)
            continue
        break

    # get valid password
    while True:
        password: str = get_password()

        if len(password) < 4:
            print(Colors.WARNING + "Password is too short!" + Colors.END)
            continue

        if password != maskpass.advpass("\n" + Colors.BLUE + "Confirm Password" + Colors.END + " : ").strip():
            print(Colors.FAIL + "Password are different!" + Colors.END)
            continue
        break

    new_client = Client(
        login=login,
        password=password,
        name=name,
        age=age
    )
    new_client.save()
    return new_client


def sign_in_user() -> Client:
    clear()
    print("\n========= Login Page ===========")

    get_login = lambda: input("\n" + Colors.BLUE + "Username" + Colors.END + " : ").strip().lower().replace(":", "")
    get_password = lambda: maskpass.advpass("\n" + Colors.BLUE + "Password" + Colors.END + " : ").strip()

    clients = Client.get_clients()
    logins = [client.login for client in clients]

    login: str = get_login()
    while login not in logins:
        print(Colors.FAIL + "This username does not excists!" + Colors.END)
        login = get_login()

    user: Client = next((client for client in clients if client.login == login), None)

    password: str = get_password()
    while password != user.password:
        print(Colors.FAIL + "Wrong password!" + Colors.END)
        password = get_password()
    return user


def accounts_page(user: Client) -> None:
    accounts = user.get_accounts()
    while True:
        clear()
        print("\n\t\t========= Accounts ==========\n")
        print('{:25s} {:20s} {:30s} '.format("Name", "Balance", "Day oppened"))
        print('-' * 75)
        [print("{:25s} {:20s} {:30s} ".format(account.name, str(account.balance), str(account.date_opened))) for account in accounts]

        print("\n[" + Colors.BLUE + "1" + Colors.END + "] Sort")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Search")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Make a Deposit")
        print("[" + Colors.BLUE + "4" + Colors.END + "] Back")

        answer: str = input("\nEnter Your choise : ")
        if answer == '4':
            return


def main():
    clear()
    print("Welcome!".center(50))
    print("\n[" + Colors.BLUE + "1" + Colors.END + "] Sing/In")
    print("[" + Colors.BLUE + "2" + Colors.END + "] Registration")

    answer: str = input("\nEnter Your choise : ")
    if answer == "1":
        user: Client = sign_in_user()
    elif answer == "2":
        user: Client = register_user()
    else:
        exit()

    while True:
        clear()
        print("\n======== Home page =========\n")
        print("[" + Colors.BLUE + "1" + Colors.END + "] My Accounts")
        print("[" + Colors.BLUE + "2" + Colors.END + "] Create New Account")
        print("[" + Colors.BLUE + "3" + Colors.END + "] Delete Account")
        print("[" + Colors.BLUE + "4" + Colors.END + "] My Payments")
        print("[" + Colors.BLUE + "5" + Colors.END + "] New Payments")
        print("[" + Colors.BLUE + "6" + Colors.END + "] Exit")
        
        answer: str = input("\nEnter Your choise : ")
        if answer == '1':
            accounts_page(user)
        elif answer == '2':
            user.create_account()
        elif answer == '3':
            user.delete_account()
        elif answer == '6':
            clear()
            break


if __name__ == "__main__":
    main()

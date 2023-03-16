import os
import maskpass  # to hide the password

from client import Client


class colors:
    BLUE = '\033[94m'
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

    # get valid username
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

    # get valid password
    while True:
        password: str = get_password()

        if len(password) < 4:
            print(colors.WARNING + "Password is too short!" + colors.END)
            continue

        if password != maskpass.advpass("\n" + colors.BLUE + "Confirm Password" + colors.END + " : ").strip():
            print(colors.FAIL + "Password are different!" + colors.END)
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

    get_login = lambda: input("\n" + colors.BLUE + "Username" + colors.END + " : ").strip().lower()
    get_password = lambda: maskpass.advpass("\n" + colors.BLUE + "Password" + colors.END + " : ").strip()

    clients = Client.get_clients()
    logins = [client.login for client in clients]

    login: str = get_login()
    while login not in logins:
        print(colors.FAIL + "This username does not excists!" + colors.END)
        login = get_login()

    user: Client = next((client for client in clients if client.login == login), None)

    password: str = get_password()
    while password != user.password:
        print(colors.FAIL + "Wrong password!" + colors.END)
        password = get_password()
    return user


def accounts_page(user: Client) -> None:
    accounts = user.get_accounts()
    while True:
        clear()
        print("\n========= Accounts ==========\n")
        print("Name", "Balance", "Day oppened", sep='\t')
        print('-' * 29)
        [print(account.name, account.balance, account.date_opened, sep='\t') for account in accounts]

        print("\n[" + colors.BLUE + "1" + colors.END + "] Sort")
        print("[" + colors.BLUE + "2" + colors.END + "] Search")
        print("[" + colors.BLUE + "3" + colors.END + "] Make a Deposit")
        print("[" + colors.BLUE + "4" + colors.END + "] Back")

        answer: str = input("\nEnter Your choise : ").lower()[0]
        if answer == '4':
            return


def main():
    clear()
    print("Welcome!".center(50))
    print("\n[" + colors.BLUE + "1" + colors.END + "] Sing/In")
    print("[" + colors.BLUE + "2" + colors.END + "] Registration")

    answer: str = input("\nEnter Your choise : ")[0]
    if answer == "1":
        user: Client = sign_in_user()
    elif answer == "2":
        user: Client = register_user()
    else:
        exit()

    while True:
        clear()
        print("\n======== Home page =========\n")
        print("[" + colors.BLUE + "1" + colors.END + "] My Accounts")
        print("[" + colors.BLUE + "2" + colors.END + "] Create New Account")
        print("[" + colors.BLUE + "3" + colors.END + "] Delete Account")
        print("[" + colors.BLUE + "4" + colors.END + "] My Payments")
        print("[" + colors.BLUE + "5" + colors.END + "] New Payments")
        print("[" + colors.BLUE + "6" + colors.END + "] Exit")
        
        answer: str = input("\nEnter Your choise : ").lower()[0]
        if answer == '1':
            accounts_page(user)
        elif answer == '2':
            clear()
            user.create_account()
        elif answer == '3':
            clear()
            print("\n======== Delete Account ==========\n")
            [print("[" + colors.BLUE, i+1, colors.END + "]", account.name) for i, account in enumerate(user.get_accounts())]
            answer: str = input("\nWhich one account You want to delete : ")
        elif answer == '6':
            break


if __name__ == "__main__":
    main()

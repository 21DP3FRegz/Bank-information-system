import os
import maskpass  # to hide the password

from client import Client


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'


clear = lambda: os.system('cls')


def register_user():
    clear()
    print("\n========Create Account=========")
    name = input("Name : ").strip()

    # get username
    logins = [client.login for client in Client.get_clients()]
    while True:
        login = input("\n" + colors.BLUE + "Username" + colors.END + " : ").strip().lower()

        if len(login) < 4:
            print(colors.WARNING + "Username is too short!" + colors.END)
            continue

        if login in logins:
            print(colors.FAIL + "This username is already taken!" + colors.END)
            continue
        break

    # get password
    while True:
        # password = maskpass.advpass("\n" + colors.BLUE + "Password" + colors.END + " : ").strip()
        password = input("\n" + colors.BLUE + "Password" + colors.END + " : ").strip()

        if len(password) < 4:
            print(colors.WARNING + "Password is too short!" + colors.END)
            continue

        # if password != maskpass.advpass("Confirm Password : ").strip()
        if password != input("Confirm Password : ").strip():
            print(colors.FAIL + "Password are different!" + colors.END)
            continue
        break

    new_client = Client(
        name=name,
        login=login,
        password=password
    )

    clear()
    """
    print("\nChose sth:")
    print("[F] - Finish registration")
    print("[P] - Add phone number")
    print("[M] - Add e-mail address\n")

    answer = input().strip().lower()
    if answer[0] == 'p':
        new_client.phone = input("Phone number : ")
    elif answer[0] == 'm':
        new_client.email = input("E-mail address : ")
    """

    print("You are successfully registered!\n")
    new_client.save()


def sign_in():
    print("\n\n=========Login Page===========")
    name = input("Username : ")

    pwd = maskpass.askpass("Password : ")


def main():
    register_user()

    clients = Client.get_clients()
    print(*(client.__dict__.values() for client in clients), sep="\n")


if __name__ == "__main__":
    main()

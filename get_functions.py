from colors import Colors
import string
import maskpass  # to hide the password
from client import Client

def get_natural_number(message: str, min_value=1) -> int:
    while True:
        try:
            num = int(input(message))
        except ValueError:
            print(Colors.FAIL + "Please enter the numbers!" + Colors.END)
            continue
        if num < min_value:
            print(Colors.WARNING + "Please enter valid number!" + Colors.END)
            continue
        return num

def get_password(message: str) -> str:
    try:
        return maskpass.advpass(message).strip()
    except KeyboardInterrupt:
        pass


def get_valid_login() -> str:
    get_user_input = lambda: input("\n" + Colors.BLUE + "Username" + Colors.END + " : ").strip().lower()
    logins: list = [client.login for client in Client.get_clients()]
    while True:
        login: str = get_user_input()
        if(login in logins):
            print(Colors.WARNING + "This Username already excist! "  + Colors.END + "Please pick another one!")
            continue
        if(not set(login).isdisjoint(set(string.punctuation))):
            print(Colors.WARNING + "Please do not use special symbols!" + Colors.END)
            continue
        if len(login) < 4:
            print(Colors.WARNING + "Username must be 4 symbols or more!" + Colors.END)
            continue
        return login


def get_valid_password() -> str:
    while True:
        password: str = get_password("\n" + Colors.BLUE + "Password" + Colors.END + " : ")
        if(not set(password).isdisjoint(set(string.punctuation))):
            print(Colors.WARNING + "Please do not use special symbols!" + Colors.END)
            continue
        if len(password) < 6:
            print(Colors.WARNING + "Password must be at least 6 symbols!" + Colors.END)
            continue
        if password != get_password("\n" + Colors.BLUE + "Confirm Password" + Colors.END + " : "):
            print(Colors.FAIL + "Passwords are different!" + Colors.END)
            continue
        return password

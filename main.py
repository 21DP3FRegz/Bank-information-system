import os
from client import Client


def register_user():
    name = input("Enter your Name : ")
    print("Thank you!")

    logins = [client.login for client in Client.get_clients()]
    while True:
        login = input("\nCreate a login : ")
        if (login not in logins):
            break
        print('\033[91m' + "This username is already taken!" + '\033[0m')

    
    password = input("Create password : ")

    new_client = Client(
        name=name,
        login=login,
        password=password
    )

    # print("You can add your phone number for safe")

    print("U r successfully finished registration!!!")
    new_client.save()


def main():
    os.system('cls')
    register_user()

    clients = Client.get_clients()
    print(*(client.__dict__.values() for client in clients), sep="\n")


if __name__ == "__main__":
    main()

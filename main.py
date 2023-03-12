import sys
from client import Client


def register_user():
    name = input("Enter your Name : ")
    print("10q! Now to continue registration Create a login:")
    login = input()
    # -_-
    password = input("Create password : ")
    # password != input("Confirm password : ") -> ...
    print("U r successfully finished registration!!!")

    new_client = Client(
        name=name,
        login=login,
        password=password
    )

    # phone or email?

    new_client.save()


def main():
    register_user()

    clients = Client.get_clients()
    print(*(client.__dict__.values() for client in clients), sep="\n")


if __name__ == "__main__":
    main()

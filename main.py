from client import Client


def register_user():
    ...


def main():
    clients = Client.get_clients()
    print(*(client.__dict__.values() for client in clients), sep="\n")


if __name__ == "__main__":
    main()

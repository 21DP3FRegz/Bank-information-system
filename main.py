from client import Client
from account import Account


def main():
    client = Client("ferepas", "12346", 17120522710, "Fēlikss")
    print(client.name, client.password, client.email, sep="\t")


if __name__ == "__main__":
    main()

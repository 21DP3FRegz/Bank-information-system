from client import Client


def main():
    client = Client(
        login="admin",
        password="admin1234",
        name="Серёга",
        email="admin@rvt.lv"
    )
    client.save()


if __name__ == "__main__":
    main()

class Client:
    def __init__(self, login: str, password: str, personal_id: int, name: str) -> None:
        self.login = login
        self.password = password

        self.personal_id = personal_id
        self.name = name
        
        self.phone = None
        self.email = None

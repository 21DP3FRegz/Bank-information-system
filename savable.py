class Savable:
    def save(self, file_path) -> None:
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(":".join(str(value) for value in self.__dict__.values()) + "\n")
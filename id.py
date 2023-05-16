import random
import string


class ID:
    @staticmethod
    def create(length: int) -> str:
        return ''.join((random.choice(string.ascii_letters + string.digits) for _ in range(length)))
    
    @staticmethod
    def auto_increment(file) -> str:
        with open(file, "r", encoding="utf-8") as f:
            ids = [int(line.split(':')[0]) for line in f.readlines()]
        return max(ids) + 1

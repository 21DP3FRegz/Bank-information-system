import random
import string


class ID:
    @staticmethod
    def create(length: int) -> str:
        return ''.join((random.choice(string.ascii_letters + string.digits) for _ in range(length)))

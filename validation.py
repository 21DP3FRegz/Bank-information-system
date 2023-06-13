import bcrypt

def verify_password(input_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_float(a_string):
    try:
        float(a_string)
        return True
    except ValueError:
        return False

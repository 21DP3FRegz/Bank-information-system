def is_float(a_string):
    try:
        float(a_string)
        return True
    except ValueError:
        return False

import bcrypt


def hash_string(input_string: str) -> str:
    salt = bcrypt.gensalt()
    hashed_string = bcrypt.hashpw(input_string.encode("utf-8"), salt)
    return hashed_string.decode("utf-8")


def verify_hashed_string(plain_string: str, hashed_string: str) -> bool:
    return bcrypt.checkpw(plain_string.encode("utf-8"), hashed_string.encode("utf-8"))

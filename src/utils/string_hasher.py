import string
import bcrypt


def hash_string(input_string: str) -> str:
    salt = bcrypt.gensalt()
    hashed_string = bcrypt.hashpw(input_string.encode("utf-8"), salt)
    return hashed_string.decode("utf-8")


def verify_hashed_string(plain_string: str, hashed_string: str) -> bool:
    return bcrypt.checkpw(plain_string.encode("utf-8"), hashed_string.encode("utf-8"))


def number_to_base62(num, max_length=5):
    base62_chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
    base52_chars = string.ascii_uppercase + string.ascii_lowercase

    if max_length > 1:
        max_num = len(base52_chars) * (len(base62_chars) ** (max_length - 1)) - 1
    else:
        max_num = max_length - 1

    if num < 0:
        raise ValueError("Number must be non-negative")
    elif num > max_num:
        raise ValueError(f"Number too large, max allowed {max_length}")

    # Encode the first character using Base 52
    num, rem = divmod(num, len(base52_chars))
    result = base52_chars[rem]

    # Encode the rest of the number using Base 62
    while num > 0:
        rem = num % len(base62_chars)
        num //= len(base62_chars)
        result = base62_chars[rem] + result

    return result


if __name__ == "__main__":
    base62 = number_to_base62(158, max_length=5)
    print(base62)

import jwt
from datetime import datetime, timedelta

PRIVATE_KEY = "RANDOM"


def create_jwt_token(
    data: dict, expires_in: int, private_key: str = PRIVATE_KEY
) -> str:
    """
    Create a JWT token with given data, private key, and expiration.
    """
    expiration = datetime.utcnow() + timedelta(seconds=expires_in)
    data.update({"exp": expiration})
    return jwt.encode(data, private_key, algorithm="HS256")


def fetch_jwt_token(token: str, private_key: str = PRIVATE_KEY) -> dict:
    """
    Decode a JWT token with the given private key. If decoding fails, raise a JWTDecodeError.
    Returns:
        dict: payload
    Raises:
        jwt.ExpiredSignatureError:
        jwt.DecodeError:
        jwt.PyJWTError: otherwise

    """
    return jwt.decode(token, private_key, algorithms=["HS256"])


"""
note: RS256 works with private and public key
"""

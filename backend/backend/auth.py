
import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY is not configured.")

    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=30)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm
    )


def decode_access_token(token: str) -> dict | None:

    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY is not configured.")

    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    try:
        return jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )

    except jwt.PyJWTError:
        return None

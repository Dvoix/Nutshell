from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from backend.src.config import settings


class AuthService:
    def __init__(self) -> None:
        self.private_key: str = settings.auth_jwt.private_key_path.read_text()
        self.public_key: str = settings.auth_jwt.public_key_path.read_text()
        self.algorithm: str = settings.auth_jwt.algorithm
        self.expire_minutes: int = settings.auth_jwt.access_token_expire_minutes

    def encode_token(
        self,
        payload: dict,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)

        if expire_timedelta:
            expire = now + expire_timedelta

        else:
            expire = now + timedelta(minutes=self.expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        return jwt.encode(
            to_encode,
            self.private_key,
            self.algorithm,
        )

    def decode_token(self, token: str | bytes) -> dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
            )
        except jwt.exceptions.PyJWTError as exc:
            raise jwt.InvalidTokenError from exc

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()

        return bcrypt.hashpw(
            pwd_bytes,
            salt,
        ).decode()

    @staticmethod
    def check_password(
        password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            hashed_password.encode(),
        )

import secrets
import string

CHARACTERS = string.ascii_letters + string.digits


def generate_slug(length: int = 6) -> str:
    return ''.join(secrets.choice(CHARACTERS) for _ in range(length))

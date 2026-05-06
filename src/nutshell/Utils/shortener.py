import secrets
import string


CHARACTERS = string.ascii_letters + string.digits

def generate_short_link(length: int = 6) -> str:
    return ''.join(secrets.choice(CHARACTERS) for _ in range(length))
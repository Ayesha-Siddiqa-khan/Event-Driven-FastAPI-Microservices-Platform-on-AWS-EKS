import hashlib
import secrets

HASH_SCHEME = "pbkdf2_sha256"
HASH_ITERATIONS = 310_000


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2 with a per-password random salt."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, HASH_ITERATIONS)
    return f"{HASH_SCHEME}${HASH_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Safely verify a password against current and legacy hashes."""
    parts = password_hash.split("$")

    if len(parts) == 4 and parts[0] == HASH_SCHEME:
        _, iterations, salt_hex, expected = parts
        try:
            digest = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                bytes.fromhex(salt_hex),
                int(iterations),
            ).hex()
        except ValueError:
            return False
        return secrets.compare_digest(digest, expected)

    if len(parts) == 2:
        salt, expected = parts
        digest = hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
        return secrets.compare_digest(digest, expected)

    return False

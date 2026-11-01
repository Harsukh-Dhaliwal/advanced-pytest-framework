import os
from cryptography.fernet import Fernet

def get_encryption_key() -> bytes:
    """Extracts the encryption token from environment variables or falls back to a sandbox baseline."""
    # Production environments will supply this via GitHub Secrets or local environmental layers
    key = os.environ.get("AUTO_FRAMEWORK_KEY")
    if not key:
        # Fallback default key for local test execution workflows (Must be a 32-byte url-safe base64 string)
        return b'uX6_K_bC_Yj8XzH9L2nV1R-8M4pQ6tW1eD4cFAg7bB0='
    return key.encode()

def encrypt_value(plain_text: str) -> str:
    """Transforms a plain text parameter into a secure encrypted token string."""
    f = Fernet(get_encryption_key())
    return f.encrypt(plain_text.encode()).decode()

def decrypt_value(encrypted_text: str) -> str:
    """Decrypts an encrypted database token back into plain text string inside volatile memory."""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_text.encode()).decode()

import bcrypt
import base64

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt, and return the hashed password as a base64 encoded string.
    """
    # Convert the password to bytes and hash it
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Convert the byte hash to a base64 encoded string
    return base64.b64encode(hashed).decode('utf-8')

def check_password(hashed_password_str: str, user_password: str) -> bool:
    """
    Check a user's password against the hashed version provided as a base64 encoded string.
    """
    try:
        # Convert the base64 encoded hash back to bytes
        hashed_password = base64.b64decode(hashed_password_str)

        # Note: bcrypt.checkpw will return True if the passwords match, otherwise it will return False
        return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
    except ValueError:
        return False

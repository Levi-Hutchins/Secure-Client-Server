import bcrypt

# Hash a password using bcrypt, and return the hashed password.
def hash_password(password: str) -> bytes: return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Check provided password and hashed value
def check_password(hashed_password: bytes, user_password: str) -> bool:
    """
    Check a user's password against the hashed version.
    """
    try:
        # Note: bcrypt.checkpw will return True if the passwords match, otherwise it will return False
        return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
    except ValueError:
        return False
# To hash a password
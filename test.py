import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt, and return the hashed password.
    """
    # Convert the password to bytes and hash it
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed

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
hashed_pw = hash_password("my_secure_password")
print(hashed_pw)
hashed_pw2 = hash_password("my_secure_password ")
print(hashed_pw2)
# To check a password
if check_password(hashed_pw, "my_secure_password"):
    print("Password matches!")
else:
    print("Invalid password!")
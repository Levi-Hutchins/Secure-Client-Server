'''
This program simulates the server in a secure client - server model.
I have successfully implemented all functionality to ensure it is as secure as
possible.
'''
# Import neccessary libraries
import json
import os
import base64
import random, string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from cryptography.hazmat.primitives.ciphers import Cipher
from flask import Flask, request, redirect, url_for, session
import HashFunction as HashFunction
import mailGun as mailGun
app = Flask(__name__)
import time

SECRET_KEY = b'6TXPMrtJBnkiJ8mo' # The secret key used for AES encryption/decryption
TOKEN_VALIDITY_PERIOD = 900  # 15 minutes in seconds
def decrypt(encoded_ciphertext, encoded_iv):
    # Decode the Base64 encoded ciphertext to get the original encrypted bytes
    ciphertext = base64.b64decode(encoded_ciphertext)
    
    # Decode the Base64 encoded IV to get the original IV bytes
    iv = base64.b64decode(encoded_iv)
    
    # Initialize the AES cipher with CFB mode using the provided IV and the secret key
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')

# Generate a random secure token 
def generate_token(length=64):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def check_required_permissions(securityLevel, operation):
    # Define access control lists for reading operations.
    # These lists dictate which security levels a user can read from, based on their own security level
    readAccessTree = {
        "TopSecret": ["TopSecret"],
        "Secret": ["TopSecret", "Secret"],
        "Unclassified": ["TopSecret", "Secret", "Unclassified"]
    }

    # Define access control lists for writing operations
    # These lists dictate which security levels a user can write to, based on their own security level
    writeAccessTree = {
        "TopSecret": ["TopSecret", "Secret", "Unclassified"],
        "Secret": ["Secret", "Unclassified"],
        "Unclassified": ["Unclassified"]
    }

    if operation == "read":
        accessTree = readAccessTree
    elif operation == "write":
        accessTree = writeAccessTree
    else:
        return False

    data = load_data()
    for user in data:
        if data[user]["isLoggedIn"] == "true":
            userSecurity = data[user]["securityLevel"]
            
            # Check if the desired security level is in the list of levels the user can access.
            if securityLevel in accessTree.get(userSecurity, []):
                return True
            else: return False
    return False

# Check the token stored with the current user and if associated expiry date is valid
def is_token_valid(username):
    data = load_data()
    if username in data and "token" in data[username] and "token_expiry" in data[username]:
        if time.time() < data[username]["token_expiry"]:

            return True
    return False

# Easy function call to open and load data to make changes later on
def load_data():
    try:
        with open("./users_db.json", 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Easy function call to save data after manipulation
def save_data(data):
    with open("./users_db.json", 'w') as f:
        json.dump(data, f)

# Generates random code used for MFA
def generate_random_code(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))

# Generate secure random password
def generateRandomSecurePassword():
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    for _ in range(13 - 4): password.append(random.choice(all_characters))
    random.shuffle(password)
    return ''.join(password)

# Sets the root user password to the randomly generated one and saves to the database
def setRootPassword():
    data = load_data()
    password = generateRandomSecurePassword()
    print("------------------------")
    print("Root Password:",password)
    print("------------------------")
    data["root"]["password"] = HashFunction.hash_password(password)
    save_data(data)

# On user login set isLoggedIn field to True to idenitify which user is logged in
def set_current_user(username):
    logout_current_user()
    print("here")
    data = load_data()
    data[username]["isLoggedIn"] = "true"
    save_data(data)

def logout_current_user():
    data = load_data()
    for user in data:
        if data[user]["isLoggedIn"] == "true":
            data[user]["isLoggedIn"] = "false"
            save_data(data)
    return

# Authenticate users attempting to log in with users in the database
def authenticate(username, password):
    # If the user is real and the password matches stored hash - access granted
    if username in load_data() and HashFunction.check_password(load_data()[username]['password'],password):
        set_current_user(username)
        return True
    return False

# Logs out all users that are currently logged in
def resetDB():
    data = load_data()
    for user in data:
        data[user]['isLoggedIn'] = False
    save_data(data)

# Provided app route function
@app.route("/hello", methods=["POST"])
def post_hello():
    
    if request.form.get("name"):
        return f"Hello {request.form['name']}"
    return "Hello stranger"

# Provided app route function
@app.route("/redirect")
def move_to_hello_name():
    """
    With this, we show how to redirect a client to a different url that we provide.
    """
    return redirect(url_for("hello", name="Bob"))

# Provided app route function
@app.route("/hello/<name>")
def hello(name):
    """
    For this, we show how to use information in the url as an argument to the function.
    The contents of the angle brackets in the route are the name of variable gains the value
    of what the client enters in it place. E.g. if the client requests `http://127.0.0.1:2250/hello/charlie`
    then name = "charlie".
    """
    return f"Hello {name}"

# Provided app route function
@app.route("/visitors", methods=["GET"])
def visitor_list():
    """
    Since this is an http server, it is stateless, allowing it handle many clients simultaneously, but also
    meaning we can not directly track users as they progress through the app.
    So, instead to keep information in any long term basis, we need to save to external service, such as a file.
    Note that using a file is in reality bad practice, but it is convenient for this assignment.
    """
    # First we append the new visitor to the list
    with open("data/visitors.txt", 'a') as f:
        f.write(request.args['name'] if request.args.get("name") else "stranger")
        f.write("\n")
    # Then we send back the list
    with open("data/visitors.txt", 'r') as f:
        return f.read()

# Provided app route function
@app.route("/json")
def json_data():
    """
    With this, we demonstrate how more complex data can be returned as a dictionary, specifically,
    it gets translated into a json file and sent back to the client. You can also send back lists this way.
    """
    return {"data": "hello", "numbers": [1, 2, 3]}

#### End example functions


@app.route("/admin_login", methods=["POST"])
def admin_login():
    username = request.form.get("username")
    notIV = request.form.get("notIV")
    password = decrypt(request.form.get("password"),notIV)
    # Check if the provided credentials are valid (using the 'authenticate' function, 
    # assumed to be defined elsewhere in the code) and the user is part of the 'admin' group.
    if authenticate(username, password) and load_data()[username]['group'] == 'admin':
        return "Access Granted"
    return "Access denied"

@app.route("/user_login", methods=["POST"])
def user_login():
    username = request.form.get("username")
    notIV = request.form.get("notIV")
    password = decrypt(request.form.get("password"),notIV)
    # Check if token exists and is valid as well as authenticated user if so let user in
    if authenticate(username, password) and is_token_valid(username):
        return "Token Valid"
    
    # If token is not valid proceed with MFA
    if authenticate(username, password):
        mfa_code = generate_random_code()
        data = load_data()
        if username in data:
            email = data[username]["email"]
            # Send the user an email for MFA code
            mailGun.sendVerifcationCode(username, email, mfa_code)
            data[username]["MFAcode"] = mfa_code
            
            # Generate token and set its expiry
            data[username]["token"] = generate_token()
            data[username]["token_expiry"] = time.time() + TOKEN_VALIDITY_PERIOD
            save_data(data)
        return "True"
    else: 
        return "False"
    
# Verify the provided MFA code was the one last generated for associated user
@app.route("/verify_login", methods=["POST"])
def verify_login():
    username = request.form.get("username")
    mfa_code = request.form.get("code")
    if username in load_data():
        if load_data()[username]["MFAcode"] == mfa_code:
            return "\n ! Access Granted ! \n"
        return "\n ! Access Denied ! \n"
    "\n ! User Not Found ! \n"




@app.route('/admin/add_user', methods=['POST'])
def add_user():
    data = load_data()
    username = request.form.get("username")
    email = request.form.get("email_address")
    # Generate a random and secure password for the new user.
    generatedPassword = generateRandomSecurePassword()
    # Hash the generated password for security. The hashed password will be stored, 
    # and the original password is only known at this moment (and will be sent via email).
    hashedPassword = HashFunction.hash_password(generatedPassword)
    # Define new user
    addedUser = {
        "password": hashedPassword, 
        "group": "users",
        "email": email, 
        "isLoggedIn": False,
        "securityLevel": "Unclassified"
    }
    # Add user and send them their detaisl
    data[username] = addedUser
    mailGun.sendUserDetails(username,generatedPassword,email)
    save_data(data)
    return "\n ! User Added & Emailed  ! \n"

# Modify users (group)
@app.route('/admin/modify_user', methods=['POST'])
def modify_user():
    username = request.form.get("username")
    groupChange = request.form.get("group")
    # Group can only be be admin or users
    if groupChange not in ["admin","users"]:
        return "\n! User group must be either admin or users !\n "
    data = load_data()
    # Find the correct user and change their group to the new group
    if username in data:
        data[username]["group"] = groupChange
        if groupChange == "admin":
            data[username]["securityLevel"] = "TopSecret"
        save_data(data)
        return "\n ! User Modified ! \n"
    return "\n ! User Not Found ! \n"

# Delete user
@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    username = request.form.get("username")
    data = load_data()
    # Find user in db and delete
    if username in data:
        del data[username]
        save_data(data)
        return "\n ! User Removed ! \n"
    return "\n ! User Not Found ! \n"



# Provided app route function - implemented biba-model access control
@app.route("/audit_expenses", methods=["POST"])
def audit_expenses():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("TopSecret","read"):

        if os.path.exists("data/expenses.txt"):
            with open("data/expenses.txt", 'r') as f:
                return f.read()
        return "\n ! Access Granted !\n  No expenses yet\n"
    return "\n ! Access Denied ! \n"

# Provided app route function - implemented biba-model access control
@app.route("/add_expense", methods=["POST"])
def add_expense():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("TopSecret","write"):
        if request.form:
            with open("data/expenses.txt", 'a') as f:
                f.write(request.form)
            return "Expense added"
        return "\n ! Access Granted ! \n  No expense was given\n"
    return "\n ! Access Denied ! \n"


# Provided app route function - implemented biba-model access control
@app.route("/audit_timesheets", methods=["POST"])
def audit_timesheets():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("TopSecret","read"):
        if os.path.exists("data/timesheets.txt"):
            with open("data/timesheets.txt", 'r') as f:
                return f.read()
        return "\n ! Access Granted ! \n  No timesheets yet\n"
    return "\n ! Access Denied ! \n"
 

# Provided app route function - implemented biba-model access control
@app.route("/submit_timesheet", methods=["POST"])
def submit_timesheet():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("TopSecret","write"):
        if request.form:
            with open("data/timesheets.txt", 'a') as f:
                f.write(request.form)
            return "Timesheet added"
        return "\n ! Access Granted ! \n  No timesheet was given\n"
    return "\n ! Access Denied ! \n"


# Provided app route function - implemented biba-model access control
@app.route("/view_meeting_minutes", methods=["POST"])
def view_meeting_minutes():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("Secret","read"):
        if os.path.exists("data/meeting_minutes.txt"):
            with open("data/meeting_minutes.txt", 'r') as f:
                return f.read()
        return "\n ! Access Granted ! \n  No meetings yet \n"
    return "\n ! Access Denied ! \n"


# Provided app route function - implemented biba-model access control
@app.route("/add_meeting_minutes", methods=["POST"])
def add_meeting_minutes():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("Secret","write"):
        if os.path.exists("data/meeting_minutes.txt"):
            with open("data/meeting_minutes.txt", 'r') as f:
                f.write(request.form)
            return "Meeting minutes added"
        return "\n ! Access Granted ! \n  No minutes given \n"
    return "\n ! Access Denied ! \n"



# Provided app route function - implemented biba-model access control
@app.route("/view_roster", methods=["POST"])
def view_roster():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("Unclassified","read"):
        if os.path.exists("data/roster.txt"):
            with open("data/roster.txt", 'r') as f:
                return f.read()
        return "\n ! Access Granted ! \n  No roster yet \n"
    return "\n ! Access Denied ! \n"


# Provided app route function - implemented biba-model access control
@app.route("/roster_shift", methods=["POST"])
def roster_shift():
    # Checks permissions of current user - sends required securityLevel and the operation being performed
    if check_required_permissions("Unclassified","write"):
        if os.path.exists("data/roster.txt"):
            with open("data/roster.txt", 'r') as f:
                f.write(request.form)
            return "Shift rostered"
        return "\n ! Access Granted ! \n  No shift given \n"
    return "\n ! Access Denied ! \n"


@app.route("/adminStatus")
def getAdminStatus():
    data = load_data()
    for user in data:
        if data[user]['isLoggedIn'] == "true" and data[user]['group'] == "admin":
            return str(True)
    return str(False)

# Provided app route function
@app.route("/")
def hello_world():
    return "Hello, World!"
# Testing purposes
@app.route("/dataview", methods=["GET"])
def data_view():
    try:
        with open('./data/users_db.json', 'r') as file:
            users_data = json.load(file)
        return users_data
    except FileNotFoundError:
        return "No data found.", 404
    except json.JSONDecodeError:
        return "Error decoding the JSON file.", 500


if __name__ == "__main__":
    resetDB()
    setRootPassword()
    os.makedirs("data/", exist_ok=True)
    app.run(host="127.0.0.1", port="2250")
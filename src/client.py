# Import necessary libraries
import requests
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from cryptography.hazmat.primitives.ciphers import Cipher
import os

# Define a secret key for symmetric encryption between client and server.
SECRET_KEY = b'6TXPMrtJBnkiJ8mo'

# Function to encrypt data before sending it to the server.
def encrypt_before_transmission(encryptMe):
    # Generate a random initialization vector (IV) for AES encryption
    iv = os.urandom(16)
    
    # Initialize the AES cipher with CFB mode
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the data
    ciphertext = encryptor.update(encryptMe.encode()) + encryptor.finalize()
    
    # Encode the ciphertext and IV using base64 for safe transmission
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    encoded_iv = base64.b64encode(iv).decode('utf-8')

    return encoded_ciphertext, encoded_iv

# Function for admin login authentication
def adminLogin(password):
    # Encrypt the password
    sensitive = encrypt_before_transmission(password)
    
    # Construct the payload to be sent to the server
    loginPayload = {
        "username": "root",
        "password":  sensitive[0],
        "notIV": sensitive[1]
    }
    
    # Send a POST request to the server's admin login route
    r = requests.post("http://127.0.0.1:2250/admin_login", data=loginPayload).text
    
    # Check the server's response
    if r == "Access Granted": 
        print("\n ! Access Granted !\n")
        return True
    else: 
        print("\n ! Access Denied !\n")
        return False

# Function for user login, handling authentication, MFA, and token verification
def userLogin(user_input):
    # Encrypt the user's password
    sensitive = encrypt_before_transmission(user_input[2])
    
    # Prepare the user's data for transmission to the server
    userData = {
        "username":user_input[1],
        "password": sensitive[0],
        "notIV": sensitive[1] 
    }

    # Send the user's data to the server's user login route
    r = requests.post("http://127.0.0.1:2250/user_login",data=userData).text
    
    # Handle the server's response for MFA or token validation
    if r == "True":
        print("You were sent an email containing a verification code")
        # Handle MFA
        code_input = input(">>> ")
        userData = {"username":user_input[1],"code": code_input}
        r = requests.post("http://127.0.0.1:2250/verify_login",data=userData).text
        print(r)
        while r == "\n ! Access Denied ! \n":
            print("Incorrect Code Try Again:")
            code_input = input(">>> ")
            userData = {"username":user_input[1],"code": code_input}
            r = requests.post("http://127.0.0.1:2250/verify_login",data=userData).text
            print(r)
    if r == "Token Valid":
        print("\n ! Access Granted !\n Your Token is still valid\n")

# UI
def adminConsole():
    print("--------------------------")
    print("Admin Controls:")
    print("--------------------------")
    # These four provide real functionality
    print("Add User:     add <username> <email_address>")
    print("Modify User:  modify <username> <change_group>")
    print("Delete User:  delete <username>")
    print("Log In:       login <username> <password>")
    print("--------------------------")
    # Calls all access control calls
    print("Test Endpoint Access Control: <test>")
    print("--------------------------")
    user_input = input(">>> ").strip().split(' ', 2)
    # all required functions - send appropriate information
    if len(user_input) == 3 and user_input[0] == "add" :
        userData = {"username":user_input[1],"email_address": user_input[2]}
        r = requests.post("http://127.0.0.1:2250/admin/add_user", data=userData)
        print(r.text)
    if user_input[0] == "modify": 
        userData = {"username":user_input[1],"group": user_input[2]}
        r = requests.post("http://127.0.0.1:2250/admin/modify_user", data=userData)
        print(r.text)
    if user_input[0] == "delete": 
        userData = {"username":user_input[1]}
        r = requests.post("http://127.0.0.1:2250/admin/delete_user", data=userData)
        print(r.text)
    if user_input[0] == "login":
       userLogin(user_input)

    # Make calls to all endpoints to determine access level
    if user_input[0] == "test":
        print(requests.post("http://127.0.0.1:2250/view_roster").text)
        print(requests.post("http://127.0.0.1:2250/roster_shift").text)
        print(requests.post("http://127.0.0.1:2250/add_expense").text)
        print(requests.post("http://127.0.0.1:2250/submit_timesheet").text)
        print(requests.post("http://127.0.0.1:2250/add_meeting_minutes").text)
        print(requests.post("http://127.0.0.1:2250/audit_expenses").text)
        print(requests.post("http://127.0.0.1:2250/audit_timesheets").text)
        print(requests.post("http://127.0.0.1:2250/view_meeting_minutes").text)
        print(requests.post("http://127.0.0.1:2250/add_expense").text)

# UI
def userConsole():
    print("------------------------")
    print("User Controls:")
    print("Log In: <username> <password>")
    print("Test Endpoint Access Control: <test>")
    print("------------------------")
    user_input = input(">>> ").strip().split(' ', 2)
    if user_input[0] == "login":
       userLogin(user_input)

    # Make calls to all endpoints to determine access level
    if user_input[0] == "test":
        print(requests.post("http://127.0.0.1:2250/view_roster").text)
        print(requests.post("http://127.0.0.1:2250/roster_shift").text)
        print(requests.post("http://127.0.0.1:2250/add_expense").text)
        print(requests.post("http://127.0.0.1:2250/submit_timesheet").text)
        print(requests.post("http://127.0.0.1:2250/add_meeting_minutes").text)
        print(requests.post("http://127.0.0.1:2250/audit_expenses").text)
        print(requests.post("http://127.0.0.1:2250/audit_timesheets").text)
        print(requests.post("http://127.0.0.1:2250/view_meeting_minutes").text)
        print(requests.post("http://127.0.0.1:2250/add_expense").text)

# Determine admin status to display admin interface
def isAdmin():
    if requests.get("http://127.0.0.1:2250/adminStatus").text == "True":
        return True
    else: return False
    
# Main loop provides some error handling with the root password
loopCount = 0
if __name__ == "__main__":
    while True:
        if loopCount == 0:
            print("===============================================")
            print("Welcome to the Secure Client - Server Program !")
            print("===============================================")
            rootPassword= input("Password for Root: ") # Is printed on server start up
            while not adminLogin(rootPassword):
                print("Incorrect Password Try Again:") 
                rootPassword= input("Password for Root: ") 

        if isAdmin():
            adminConsole()
        else:
            userConsole()
        loopCount += 1
           
        
        


        


  
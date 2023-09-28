import requests


def adminLogin(password):
    loginPayload = {
        "username": "root",
        "password": password
    }

    r = requests.post("http://127.0.0.1:2250/admin_login", data=loginPayload).text
    if r == "Access Granted": 
        print("\n ! Access Granted !\n")
        return True
    else: 
        print("\n ! Access Denied !\n")
        return False
    
def adminConsole():
    print("--------------------------")
    print("Admin Controls:")
    print("Add User:     add <username> <email_address>")
    print("Modify User:  modify <username> <change_group>")
    print("Delete User:  delete <username>")
    print("Log In: <username> <password>")
    print("--------------------------")
    user_input = input(">>> ").strip().split(' ', 2)
    if user_input[0] == "add":
        userData = {"username":user_input[1],"email_address": user_input[2]}
        r = requests.post("http://127.0.0.1:2250/admin/add_user", data=userData)
        print(r.text)
    if user_input[0] == "modify": 
        userData = {"username":user_input[1],"group": user_input[2]}
        r = requests.post("http://127.0.0.1:2250/admin/modify_user", data=userData)
        print(r.text)
    if user_input[0] == "delete": 
        userData = {"username":user_input[1],}
        r = requests.post("http://127.0.0.1:2250/admin/delete_user", data=userData)
        print(r.text)
    if user_input[0] == "logout":
        print(requests.get("http://127.0.0.1:2250/logout_user").text)

def userConsole():
    print("------------------------")
    print("User Controls:")
    print("Log In: <username> <password>")
    print("------------------------")
    user_input = input(">>> ").strip().split(' ', 2)


def isAdmin():
    if requests.get("http://127.0.0.1:2250/adminStatus").text == "True":
        return True
    else: return False
    

loopCount = 0
loggedInFlag = False
# TODO: add exit option if selected logs out all users
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
           
        
        


        







    # r = requests.get("http://127.0.0.1:2250/lost_page")
    # print(r.status_code)
    # if r.status_code == 404:
    #     print("The page was not found")

    # # For more complicated responses, e.g. when the server returns a dictionary, you can use the json() method
    # # to process as a dictionary
    # r = requests.get("http://127.0.0.1:2250/json")
    # print(r.json())

    # testAdminLogin()

  


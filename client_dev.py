import requests


def adminLogin(password):
    loginnPayload = {
        "username": "root",
        "password": password
    }

    r = requests.post("http://127.0.0.1:2250/admin_console", data=loginnPayload)
    print(r.text)
    
def adminStatus():
    r = requests.get("http://127.0.0.1:2250/adminStatus")
    print(r.text)

def logOut():
    r = requests.get("http://127.0.0.1:2250/logOutUsers")
    print(r.text)


loopCount = 0
if __name__ == "__main__":
    while True:
        #if loopCount == 0:
            print("===============================================")
            print("Welcome to the Secure Client - Server Program !")
            print("===============================================")
            print("Root Login:")
            #rootUsername= input("Root Username (root): ")
            rootPassword= input("Password for Root: ") # Is printed on server start up
            adminLogin(rootPassword) 
            inp = input("log out?")
            if inp == "yes":
                 logOut()
        # print()
        # print("---------------------------------------------")
        # print("Please Select one of the options:")
        # print("NOTE: You will only be able to select on ")
        # print("<add user>")
        # print("<modify user>")
        # print("<delete user>")
        
        


        
        # loopCount += 1






    # r = requests.get("http://127.0.0.1:2250/lost_page")
    # print(r.status_code)
    # if r.status_code == 404:
    #     print("The page was not found")

    # # For more complicated responses, e.g. when the server returns a dictionary, you can use the json() method
    # # to process as a dictionary
    # r = requests.get("http://127.0.0.1:2250/json")
    # print(r.json())

    # testAdminLogin()

  


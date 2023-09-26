import requests
def adminLogin(password):
    incorrectPayload = {
        "username": "root",
        "password": "admin123"
    }
    loginPayload = {
        "username": "root",
        "password": pas
    }
    r = requests.post("http://127.0.0.1:2250/admin_console", data=incorrectPayload)
    print(r.text)
    r = requests.post("http://127.0.0.1:2250/admin_console", data=correctPayLoad)
    print(r.text)
    

if __name__ == "__main__":
    # The following shows example code requesting each of the example functions from the server
    r = requests.get("http://127.0.0.1:2250/")
    # server responses are given in the text variable shown with the following
    print(r.text)

    r = requests.post("http://127.0.0.1:2250/hello", data={"name": "Alice"})
    print(r.text)

    r = requests.post("http://127.0.0.1:2250/hello")
    print(r.text)

    r = requests.get("http://127.0.0.1:2250/redirect")
    print(r.text)

    r = requests.get("http://127.0.0.1:2250/visitors?name=Frank")
    print(r.text)

    # For some error checking, you can also check whether a request was successful by looking at the status_code
    # variable
    r = requests.get("http://127.0.0.1:2250/lost_page")
    print(r.status_code)
    if r.status_code == 404:
        print("The page was not found")

    # For more complicated responses, e.g. when the server returns a dictionary, you can use the json() method
    # to process as a dictionary
    r = requests.get("http://127.0.0.1:2250/json")
    print(r.json())

    testAdminLogin()

  


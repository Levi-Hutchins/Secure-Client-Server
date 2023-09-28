"""
This is our HTTP server, to run, just install Flask using the pip tool and run this file with `python server.py`.
In this, we provide some example functions showing what Flask can do, then the functions you should add authentication
and access control to.
"""

import os
from flask import Flask, request, redirect, url_for
app = Flask(__name__)


#### Example functions
# The following are examples of what you can do with Flask, you will probably want remove them on submission

@app.route("/")
def hello_world():
    
    return "Hello, World!"


@app.route("/hello", methods=["POST"])
def post_hello():
    """
    This shows an example of a post request, one of the types of http message.
    This allows a client to send information inside the payload part of the http
    packet, and the server can read that information in the form of the dictionary
    `request.form`.
    You can also do similar with GET requests, although the dictionary
    will then be `request.args`. Additionally, the data will be directly in the url,
    so you likely want to avoid GET if sending sensitive information such as passwords
    as we are in this assignment.
    """
    if request.form.get("name"):
        return f"Hello {request.form['name']}"
    return "Hello stranger"


@app.route("/redirect")
def move_to_hello_name():
    """
    With this, we show how to redirect a client to a different url that we provide.
    """
    return redirect(url_for("hello", name="Bob"))


@app.route("/hello/<name>")
def hello(name):
    """
    For this, we show how to use information in the url as an argument to the function.
    The contents of the angle brackets in the route are the name of variable gains the value
    of what the client enters in it place. E.g. if the client requests `http://127.0.0.1:2250/hello/charlie`
    then name = "charlie".
    """
    return f"Hello {name}"


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


@app.route("/json")
def json_data():
    """
    With this, we demonstrate how more complex data can be returned as a dictionary, specifically,
    it gets translated into a json file and sent back to the client. You can also send back lists this way.
    """
    return {"data": "hello", "numbers": [1, 2, 3]}

#### End example functions


@app.route("/admin_console", methods=["POST"])
def admin_console():
    return "Access denied"


@app.route("/audit_expenses", methods=["POST"])
def audit_expenses():
    if os.path.exists("data/expenses.txt"):
        with open("data/expenses.txt", 'r') as f:
            return f.read()
    return "No expenses yet"


@app.route("/add_expense", methods=["POST"])
def add_expense():
    if response.form:
        with open("data/expenses.txt", 'a') as f:
            f.write(response.form)
        return "Expense added"
    return "No expense was given"


@app.route("/audit_timesheets", methods=["POST"])
def audit_timesheets():
    if os.path.exists("data/timesheets.txt"):
        with open("data/timesheets.txt", 'r') as f:
            return f.read()
    return "No timesheets yet"


@app.route("/submit_timesheet", methods=["POST"])
def submit_timesheet():
    if response.form:
        with open("data/timesheets.txt", 'a') as f:
            f.write(response.form)
        return "Timesheet added"
    return "No timesheet was given"


@app.route("/view_meeting_minutes", methods=["POST"])
def view_meeting_minutes():
    if os.path.exists("data/meeting_minutes.txt"):
        with open("data/meeting_minutes.txt", 'r') as f:
            return f.read()
    return "No meeting minutes yet"


@app.route("/add_meeting_minutes", methods=["POST"])
def add_meeting_minutes():
    if os.path.exists("data/meeting_minutes.txt"):
        with open("data/meeting_minutes.txt", 'r') as f:
            f.write(response.form)
        return "Meeting minutes added"
    return "No meeting minutes given"


@app.route("/view_roster", methods=["POST"])
def view_roster():
    if os.path.exists("data/roster.txt"):
        with open("data/roster.txt", 'r') as f:
            return f.read()
    return "No roster yet"


@app.route("/roster_shift", methods=["POST"])
def roster_shift():
    if os.path.exists("data/roster.txt"):
        with open("data/roster.txt", 'r') as f:
            f.write(response.form)
        return "Shift rostered"
    return "No shift given"


if __name__ == "__main__":
    
    os.makedirs("data/", exist_ok=True)
    app.run(host="127.0.0.1", port="2250")
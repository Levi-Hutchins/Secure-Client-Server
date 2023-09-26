from flask import Flask

app = Flask(__name__)

# Global variable
counter = 0

@app.route('/increment')
def increment():
    global counter
    counter += 1
    return f"Counter is now {counter}"

@app.route('/get')
def get_value():
    return f"Counter is {counter}"

if __name__ == "__main__":
    app.run(debug=True)

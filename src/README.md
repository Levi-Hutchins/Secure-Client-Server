# Adding Access Control and Authentication to an HTTP Server

For this task you will modify a http server program to provide authentication and access control for its various services.


## Setup

To run these programs you will need to install a recent version of python3, preferably version 3.7
or higher.

Next you will need to install the required libraries using the pip tool included with python, run the following
in a terminal in this folder:

```sh
pip install -r requirements.txt
```

Sometimes you may get an error saying pip is not found despite having python installed, in that case you need to
run `python -m pip install -r requirements.txt` instead.

Now you're ready to run the programs.


## Running the programs

First we need to start the server with the following:

```sh
python3 server.py
```

It will say that is running on http://127.0.0.1:2250, which means you are ready to start the client with:

```sh
python3 client.py
```

The client goes through and tests each of the example endpoints of the server.

# Your Task

You will add an authentication mechanism and access control to the server as specified in the assignment specs.
You will also extend the client program, to test each possible responses from the server.
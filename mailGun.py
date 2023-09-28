import requests
# Utilises the Mailgun API in order to send the created user their details
def sendUserDetails(username, password, email):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox74dfba5af7c34e2091e3a846c771a53b.mailgun.org/messages",
		auth=("api", "a487497d74cc494deb702431126b5ba8-db137ccd-10c7f37e"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox74dfba5af7c34e2091e3a846c771a53b.mailgun.org>",
			"to": str(email),
			"subject": "Find User Details Below",
			"text": f"Hello {username},\nHere is your username and password.\nUsername: {username}\nPassword: {password}"})

def sendVerifcationCode(username, email, code):
	return requests.post(
			"https://api.mailgun.net/v3/sandbox74dfba5af7c34e2091e3a846c771a53b.mailgun.org/messages",
			auth=("api", "a487497d74cc494deb702431126b5ba8-db137ccd-10c7f37e"),
			data={"from": "Mailgun Sandbox <postmaster@sandbox74dfba5af7c34e2091e3a846c771a53b.mailgun.org>",
				"to": str(email),
				"subject": "Find User Details Below",
				"text": f"Hello {username},\nHere is your Verification Code: {code}"})
def add_user(username, email):
    if username not in users:
        password = 'RANDOMLY_GENERATED_PASSWORD'  # Replace with a function to generate a password
        users[username] = {
            'password': password,
            'group': 'user',
            'email': email
        }
        # TODO: Send email with credentials to user
        return True
    return False

def modify_user(username, group):
    if username in users:
        users[username]['group'] = group
        return True
    return False

def delete_user(username):
    if username in users:
        del users[username]
        return True
    return False

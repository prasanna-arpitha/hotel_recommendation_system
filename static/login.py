import json
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

def signup(username,email,password,cpass):
    users = load_users()
    if username in users:
        print("Username already exists. Please choose a different one.")
        return
    if email in users:
        print("email already registered.")
        return
    if password == cpass:
        users[username] = password
        save_users(users)
        print("Signup successful. You can now login.")


def login(username,password):
    users = load_users()
    
    if username not in users:
        print("Username not found. Please sign up first.")
        return False

    if users[username] == password:
        print("Login successful. Welcome back, ", username)
        return True
    else:
        print("Incorrect password. Please try again.")
        return False
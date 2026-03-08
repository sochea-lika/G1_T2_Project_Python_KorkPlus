def login(system):
    users = system.load_users()
    attempt = 3
    while attempt > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username not in users or password != users[username]:
            attempt -= 1
            print(f"Invalid credentials. You have {attempt} attempts left.")
        else:
            print(f"Login successful! Welcome, {username}")
            return User(username, password)
        if attempt == 0:
            print("Too many failed attempts. Access blocked.")
            return None
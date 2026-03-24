import msvcrt
import sys

def get_password_with_dots(prompt="Enter password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        char = msvcrt.getch().decode('utf-8')
        
        if char == '\r' or char == '\n':  
            print()
            return password
        elif char == '\b':  
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += char
            sys.stdout.write('•') # Show a dot instead of the letter
            sys.stdout.flush()
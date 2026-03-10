import msvcrt
import sys

def get_password_with_dots(prompt="Enter password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        # Get a single character without showing it
        char = msvcrt.getch().decode('utf-8')
        
        if char == '\r' or char == '\n':  # Enter key
            print()
            return password
        elif char == '\b':  # Backspace key
            if len(password) > 0:
                password = password[:-1]
                # Erase the last dot from the screen
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += char
            sys.stdout.write('•') # Show a dot instead of the letter
            sys.stdout.flush()